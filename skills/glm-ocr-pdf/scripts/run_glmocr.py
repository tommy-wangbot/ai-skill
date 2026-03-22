#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_ROOT = Path(
    os.environ.get("GLMOCR_ROOT", "/Users/tommy/Documents/codex/GLM-OCR")
).expanduser()
DEFAULT_PORT = int(os.environ.get("GLMOCR_MLX_PORT", "18080"))


def is_healthy(port: int) -> bool:
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/health", timeout=5
        ) as response:
            return response.status == 200
    except (OSError, urllib.error.URLError):
        return False


def wait_for_health(port: int, timeout_seconds: int) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if is_healthy(port):
            return
        time.sleep(2)
    raise TimeoutError(
        f"Timed out waiting for MLX server on http://127.0.0.1:{port}/health"
    )


def start_mlx_server(root: Path, port: int, log_file: Path) -> int:
    mlx_python = root / ".venv-mlx" / "bin" / "python"
    server_script = root / "start_mlx_server.py"
    if not mlx_python.is_file():
        raise FileNotFoundError(f"Missing MLX Python: {mlx_python}")
    if not server_script.is_file():
        raise FileNotFoundError(f"Missing MLX server launcher: {server_script}")

    log_file.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.setdefault("HF_HUB_DISABLE_XET", "1")

    with log_file.open("ab") as handle:
        process = subprocess.Popen(
            [
                str(mlx_python),
                str(server_script),
                "--trust-remote-code",
                "--port",
                str(port),
            ],
            cwd=root,
            env=env,
            stdout=handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    return process.pid


def run_glmocr(root: Path, input_path: Path, config_path: Path, output_dir: Path) -> int:
    glmocr_bin = root / ".venv-sdk" / "bin" / "glmocr"
    if not glmocr_bin.is_file():
        raise FileNotFoundError(f"Missing glmocr CLI: {glmocr_bin}")
    if not config_path.is_file():
        raise FileNotFoundError(f"Missing config file: {config_path}")
    if not input_path.exists():
        raise FileNotFoundError(f"Input path not found: {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        str(glmocr_bin),
        "parse",
        str(input_path),
        "--config",
        str(config_path),
        "--output",
        str(output_dir),
    ]
    return subprocess.run(command, cwd=root, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the local Apple Silicon GLM-OCR installation."
    )
    parser.add_argument("input_path", help="Absolute or relative path to a PDF/image")
    parser.add_argument(
        "--output-dir",
        default=str(Path.cwd() / "glmocr-output"),
        help="Directory where GLM-OCR should write results",
    )
    parser.add_argument(
        "--root",
        default=str(DEFAULT_ROOT),
        help="Root of the local GLM-OCR checkout",
    )
    parser.add_argument(
        "--config",
        default="config.mlx.local.yaml",
        help="Config path, relative to --root unless absolute",
    )
    parser.add_argument(
        "--mlx-port",
        type=int,
        default=DEFAULT_PORT,
        help="Port used by the local mlx-vlm server",
    )
    parser.add_argument(
        "--wait-seconds",
        type=int,
        default=600,
        help="Maximum wait time for MLX health",
    )
    parser.add_argument(
        "--mlx-log-file",
        default=str(Path.home() / ".codex" / "logs" / "glm-ocr-mlx.log"),
        help="Log file used when the wrapper starts mlx-vlm",
    )
    parser.add_argument(
        "--no-start-mlx",
        action="store_true",
        help="Fail instead of starting mlx-vlm when it is not already healthy",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    input_path = Path(args.input_path).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    config_path = Path(args.config).expanduser()
    if not config_path.is_absolute():
        config_path = (root / config_path).resolve()
    log_file = Path(args.mlx_log_file).expanduser().resolve()

    if not is_healthy(args.mlx_port):
        if args.no_start_mlx:
            print(
                f"MLX server is not healthy on port {args.mlx_port}. "
                "Start it first or omit --no-start-mlx.",
                file=sys.stderr,
            )
            return 2
        pid = start_mlx_server(root, args.mlx_port, log_file)
        print(f"Started mlx-vlm server (pid={pid}), waiting for health...")
        wait_for_health(args.mlx_port, args.wait_seconds)

    exit_code = run_glmocr(root, input_path, config_path, output_dir)
    if exit_code != 0:
        return exit_code

    stem = input_path.stem
    result_dir = output_dir / stem
    print(f"Results directory: {result_dir}")
    for suffix in (".md", ".json"):
        candidate = result_dir / f"{stem}{suffix}"
        if candidate.exists():
            print(candidate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

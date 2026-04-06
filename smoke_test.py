from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"
BACKEND_URL = "http://127.0.0.1:8001"
FRONTEND_URL = "http://127.0.0.1:3000"


def _wait_for_http(url: str, timeout_seconds: int) -> requests.Response | None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            response = requests.get(url, timeout=2)
            return response
        except Exception:
            time.sleep(0.5)
    return None


def _terminate(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def main() -> int:
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "server:app", "--host", "127.0.0.1", "--port", "8001"],
        cwd=str(BACKEND_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    frontend_env = os.environ.copy()
    frontend_env["BROWSER"] = "none"
    frontend_env["REACT_APP_BACKEND_URL"] = BACKEND_URL
    frontend = subprocess.Popen(
        ["npm.cmd", "start"],
        cwd=str(FRONTEND_DIR),
        env=frontend_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    report: dict[str, Any] = {
        "backend": {"ready": False, "logs": []},
        "frontend": {"ready": False, "logs": []},
        "api": {},
        "seed_user": None,
    }

    try:
        backend_response = _wait_for_http(f"{BACKEND_URL}/api/health", timeout_seconds=45)
        report["backend"]["ready"] = backend_response is not None and backend_response.status_code == 200
        if not report["backend"]["ready"]:
            for _ in range(20):
                if backend.stdout is None:
                    break
                line = backend.stdout.readline()
                if not line:
                    break
                report["backend"]["logs"].append(line.rstrip())
            print(json.dumps(report, indent=2))
            return 1

        timestamp = int(time.time())
        email = f"smoke_{timestamp}@example.com"
        password = "Password@12345!"
        report["seed_user"] = {"email": email, "password": password}

        session = requests.Session()
        report["api"]["health"] = session.get(f"{BACKEND_URL}/api/health", timeout=5).json()
        report["api"]["root"] = session.get(f"{BACKEND_URL}/api", timeout=5).json()

        register = session.post(
            f"{BACKEND_URL}/api/auth/register",
            json={"email": email, "password": password, "name": "Smoke Test"},
            timeout=10,
        )
        report["api"]["register_status"] = register.status_code
        report["api"]["register"] = register.json()

        login = session.post(
            f"{BACKEND_URL}/api/auth/login",
            json={"email": email, "password": password},
            timeout=10,
        )
        report["api"]["login_status"] = login.status_code
        report["api"]["login"] = login.json()

        token = report["api"]["login"]["token"]
        refresh_token = report["api"]["login"]["refresh_token"]
        headers = {"Authorization": f"Bearer {token}"}

        me = session.get(f"{BACKEND_URL}/api/auth/me", headers=headers, timeout=10)
        report["api"]["me_status"] = me.status_code
        report["api"]["me"] = me.json()

        command = session.post(
            f"{BACKEND_URL}/api/command",
            headers=headers,
            json={"command": "weather in Mumbai", "type": "text"},
            timeout=15,
        )
        report["api"]["command_status"] = command.status_code
        report["api"]["command"] = command.json()

        logout = session.post(
            f"{BACKEND_URL}/api/auth/logout",
            headers={**headers, "x-refresh-token": refresh_token},
            timeout=10,
        )
        report["api"]["logout_status"] = logout.status_code
        report["api"]["logout"] = logout.json()

        frontend_response = _wait_for_http(FRONTEND_URL, timeout_seconds=90)
        report["frontend"]["ready"] = frontend_response is not None and frontend_response.status_code == 200
        if frontend_response is not None:
            report["frontend"]["status"] = frontend_response.status_code
            report["frontend"]["contains_root"] = '<div id="root"></div>' in frontend_response.text
            scripts = re.findall(r'<script[^>]+src="([^"]+)"', frontend_response.text)
            bundle_has_backend_url = False
            for script in scripts:
                if not script.startswith("/"):
                    continue
                try:
                    bundle = requests.get(f"{FRONTEND_URL}{script}", timeout=5).text
                except Exception:
                    continue
                if BACKEND_URL in bundle:
                    bundle_has_backend_url = True
                    break
            report["frontend"]["bundle_has_backend_url"] = bundle_has_backend_url

        print(json.dumps(report, indent=2))
        return 0
    finally:
        _terminate(frontend)
        _terminate(backend)


if __name__ == "__main__":
    raise SystemExit(main())

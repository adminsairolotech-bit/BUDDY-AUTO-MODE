from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class UltimateV5Config:
    max_cycles: int = 5
    error_repeat_limit: int = 2
    max_pipeline_run: int = 5
    project_root: str = "."
    memory_dir: str = ".ai_memory"


class UltimateV5Runner:
    """
    Implements ULTIMATE AI SYSTEM v5 execution loop:
    - MAX_CYCLES
    - ERROR_REPEAT_LIMIT
    - MAX_PIPELINE_RUN
    - learning logs in .ai_memory/errors.log and .ai_memory/solutions.log
    """

    def __init__(self, config: UltimateV5Config | None = None) -> None:
        self.config = config or UltimateV5Config()
        self.project_root = Path(self.config.project_root).resolve()
        self.memory_dir = self.project_root / self.config.memory_dir
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.error_log_path = self.memory_dir / "errors.log"
        self.solution_log_path = self.memory_dir / "solutions.log"

    def run(self) -> dict[str, Any]:
        pipeline_runs = 0
        cycles_used = 0
        last_error = ""
        repeat_count = 0
        typecheck_pass = False
        tests_pass = False
        status = "FAILED"
        failure_reason = ""

        for cycle in range(1, self.config.max_cycles + 1):
            cycles_used = cycle
            pipeline_runs += 1
            if pipeline_runs > self.config.max_pipeline_run:
                failure_reason = "pipeline_run_limit_exceeded"
                break

            prereq_node = self._run_cmd(["node", "-v"])
            prereq_npm = self._run_cmd(["npm", "-v"])
            if prereq_node["returncode"] != 0 or prereq_npm["returncode"] != 0:
                failure_reason = "node_or_npm_missing"
                self._append_error_log("prereq_error", "Node or npm missing", {"node": prereq_node, "npm": prereq_npm})
                break

            install = self._run_cmd(["npm", "install"])
            if install["returncode"] != 0:
                error_text = self._normalize_error((install.get("stderr") or install.get("stdout") or "").strip() or "npm install failed")
                self._append_error_log("npm_install_failed", error_text, {"cycle": cycle})
                if error_text == last_error:
                    repeat_count += 1
                else:
                    repeat_count = 0
                    last_error = error_text
                if repeat_count >= self.config.error_repeat_limit:
                    failure_reason = "repeated_error_limit_reached"
                    break
                continue

            typecheck = self._run_cmd(["npm", "run", "typecheck"])
            self._append_to_local_error_file(typecheck)
            typecheck_pass = typecheck["returncode"] == 0

            tests = self._run_cmd(["npm", "test"])
            self._append_to_local_error_file(tests)
            tests_pass = tests["returncode"] == 0

            if typecheck_pass and tests_pass:
                status = "SUCCESS"
                self._append_solution_log(
                    "validation_passed",
                    {"cycle": cycle, "typecheck": "PASS", "tests": "PASS"},
                    worked=True,
                )
                break

            current_error = self._normalize_error(self._last_error_lines(20))
            self._append_error_log(
                "validation_failed",
                current_error or "typecheck_or_test_failed",
                {"cycle": cycle, "typecheck_pass": typecheck_pass, "tests_pass": tests_pass},
            )

            if current_error == last_error:
                repeat_count += 1
            else:
                repeat_count = 0
                last_error = current_error

            if repeat_count >= self.config.error_repeat_limit:
                failure_reason = "repeated_error_limit_reached"
                break

        if status != "SUCCESS" and not failure_reason:
            failure_reason = "max_cycles_reached"

        report = {
            "STATUS": status,
            "CYCLES_USED": cycles_used,
            "TYPECHECK": "PASS" if typecheck_pass else "FAIL",
            "TESTS": "PASS" if tests_pass else "FAIL",
            "VERIFIED": int(typecheck_pass) + int(tests_pass),
            "FILES_CHANGED": self._count_changed_files(),
            "COMMIT": self._git_commit_hash(),
            "FAILURE_REASON": failure_reason if status == "FAILED" else None,
        }
        return report

    def _run_cmd(self, command: list[str]) -> dict[str, Any]:
        try:
            proc = subprocess.run(
                command,
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=1200,
                check=False,
            )
            return {
                "command": " ".join(command),
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
            }
        except Exception as exc:
            return {
                "command": " ".join(command),
                "returncode": 1,
                "stdout": "",
                "stderr": str(exc),
            }

    def _append_to_local_error_file(self, cmd_result: dict[str, Any]) -> None:
        output = (cmd_result.get("stderr") or "") + "\n" + (cmd_result.get("stdout") or "")
        output = output.strip()
        if not output:
            return
        with open(self.error_log_path, "a", encoding="utf-8") as f:
            f.write(output + "\n")

    def _last_error_lines(self, n: int) -> str:
        if not self.error_log_path.exists():
            return ""
        with open(self.error_log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return "".join(lines[-n:]).strip()

    def _normalize_error(self, error: str) -> str:
        text = error or ""
        text = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}", "[TIMESTAMP]", text)
        text = re.sub(r"[a-f0-9]{24,}", "[ID]", text)
        text = re.sub(r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", "[UUID]", text)
        text = re.sub(r"line \d+", "line [N]", text, flags=re.IGNORECASE)
        return text.strip()

    def _append_error_log(self, error_type: str, message: str, context: dict[str, Any] | None = None) -> None:
        payload = {
            "error_type": error_type,
            "error_message": message,
            "normalized_error": self._normalize_error(message),
            "context": context or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        with open(self.error_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, default=str) + "\n")

    def _append_solution_log(self, error_pattern: str, solution: dict[str, Any], worked: bool) -> None:
        payload = {
            "error_pattern": error_pattern,
            "solution": solution,
            "worked": worked,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        with open(self.solution_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, default=str) + "\n")

    def _count_changed_files(self) -> int:
        result = self._run_cmd(["git", "diff", "--name-only"])
        if result["returncode"] != 0:
            return 0
        lines = [ln.strip() for ln in (result.get("stdout") or "").splitlines() if ln.strip()]
        return len(lines)

    def _git_commit_hash(self) -> str:
        result = self._run_cmd(["git", "rev-parse", "--short", "HEAD"])
        if result["returncode"] != 0:
            return "N/A"
        return (result.get("stdout") or "").strip() or "N/A"


def build_config_from_env(project_root: str = ".") -> UltimateV5Config:
    return UltimateV5Config(
        max_cycles=int(os.getenv("ULTIMATE_MAX_CYCLES", "5")),
        error_repeat_limit=int(os.getenv("ULTIMATE_ERROR_REPEAT_LIMIT", "2")),
        max_pipeline_run=int(os.getenv("ULTIMATE_MAX_PIPELINE_RUN", "5")),
        project_root=project_root,
        memory_dir=os.getenv("ULTIMATE_MEMORY_DIR", ".ai_memory"),
    )

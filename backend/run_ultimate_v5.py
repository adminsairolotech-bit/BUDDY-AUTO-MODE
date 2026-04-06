from __future__ import annotations

import argparse
import json
from pathlib import Path

from core.ultimate_v5_runner import UltimateV5Runner, build_config_from_env


def main() -> None:
    parser = argparse.ArgumentParser(description="Run ULTIMATE AI SYSTEM v5 validation loop.")
    parser.add_argument("--project-root", default=".", help="Project root where npm commands should run")
    args = parser.parse_args()

    root = str(Path(args.project_root).resolve())
    config = build_config_from_env(project_root=root)
    runner = UltimateV5Runner(config=config)
    report = runner.run()

    print("---REPORT START---")
    print(json.dumps(report, indent=2))
    print("---REPORT END---")


if __name__ == "__main__":
    main()

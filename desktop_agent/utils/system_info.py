from __future__ import annotations

import platform

import psutil


def get_system_info() -> dict:
    disk_root = "C:\\" if platform.system().lower().startswith("win") else "/"
    battery = psutil.sensors_battery()
    return {
        "platform": platform.platform(),
        "hostname": platform.node(),
        "cpu_percent": psutil.cpu_percent(interval=0.2),
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent,
        },
        "disk": {
            "total": psutil.disk_usage(disk_root).total,
            "free": psutil.disk_usage(disk_root).free,
            "percent": psutil.disk_usage(disk_root).percent,
        },
        "battery": battery._asdict() if battery else None,
    }

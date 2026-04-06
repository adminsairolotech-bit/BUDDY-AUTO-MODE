"""
Build Desktop Agent as standalone .exe
"""

import PyInstaller.__main__


PyInstaller.__main__.run(
    [
        "agent.py",
        "--onefile",
        "--windowed",
        "--name=OpenClawAgent",
        "--icon=icon.ico",
        "--add-data=config.json;.",
        "--hidden-import=websocket",
        "--hidden-import=pyautogui",
        "--hidden-import=pygetwindow",
        "--hidden-import=pyperclip",
        "--hidden-import=psutil",
        "--hidden-import=PIL",
    ]
)

print("Build complete! Check dist/OpenClawAgent.exe")

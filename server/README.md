# Steps from .py 2 .exe

    pyarmor gen -O dist main.py
    pyinstaller --onefile --hidden-import=json dist/main.py

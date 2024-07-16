# **Steps from** `.py 2 .exe`

    pip install pyinstaller pyarmor
    pyarmor gen -O dist main.py
    pyinstaller --onefile --hidden-import=json --icon=icon.ico dist/main.py

![image](https://github.com/user-attachments/assets/4d259b58-59d4-4804-a048-8424e3258a59)

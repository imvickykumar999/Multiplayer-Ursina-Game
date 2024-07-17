# **Steps from** `.py 2 .exe`

    pip install pyinstaller pyarmor
    pyarmor gen -O dist main.py
    pyinstaller --onefile --hidden-import=art --hidden-import=json --icon=icon.ico main.py

    cd dist
    file main
    chmod +x main
    ./main

![image](https://github.com/user-attachments/assets/9e781451-001b-4e54-877b-39038873a553)
![image](https://github.com/user-attachments/assets/4d259b58-59d4-4804-a048-8424e3258a59)

# `.py 2 .exe`

    pip install pyinstaller pyarmor
    pyarmor gen -O dist main.py
    pyinstaller --onefile --hidden-import=art --hidden-import=json --icon=icon.ico main.py

![image](https://github.com/user-attachments/assets/99962b82-4e9d-40a5-b900-5f88a7eb6bae)

    # UBUNTU
    
    cd dist
    file main
    chmod +x main
    ./main

![image](https://github.com/user-attachments/assets/9e781451-001b-4e54-877b-39038873a553)

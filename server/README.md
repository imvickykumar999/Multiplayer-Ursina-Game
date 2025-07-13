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

### Client EXE

```bash
pyinstaller main.py --onefile --noconsole ^
--add-data "assets;assets" ^
--collect-all panda3d ^
--collect-all ursina ^
--hidden-import bullet ^
--hidden-import enemy ^
--hidden-import floor ^
--hidden-import map ^
--hidden-import network ^
--hidden-import player ^
--name "clickNplayGame" ^
--icon=icon.ico

pyinstaller clickNplayGame.spec
```

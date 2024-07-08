# `server.exe`

### Step-by-Step Guide:

1. **Open Terminal (Command Prompt)**:

   - Open your terminal or command prompt application on your computer. You'll use this to run commands and navigate directories.

2. **Navigate to Your Project Directory**:

   - Use the `cd` command to change directory to where your `server.py` script is located. For example, if your script is in a directory named `server_project`, you would type:
     ```
     cd path/to/server_project
     ```
     Replace `path/to/server_project` with the actual path where your `server.py` script resides.

3. **Verify PyInstaller Installation**:

   - Before proceeding, ensure that PyInstaller is installed in your Python environment. You can check by running:
     ```
     pyinstaller --version
     ```
     If PyInstaller is installed, you'll see its version number. If not, you'll need to install it using `pip`. You can install PyInstaller with:
     ```
     pip install pyinstaller
     ```

4. **Create a `main.spec` File**:

   - In your project directory (`server_project`), create a file named `main.spec`. You can create this file using any text editor like Notepad, Atom, VS Code, etc.

5. **Edit `main.spec` File**:

   - Copy and paste the following content into your `main.spec` file:
     ```python
     # -*- mode: python ; coding: utf-8 -*-

     block_cipher = None

     a = Analysis(
         ['server.py'],  # Replace 'server.py' with the actual name of your server script
         pathex=['.'],
         binaries=[],
         datas=[],
         hiddenimports=[],
         hookspath=[],
         hooksconfig={},
         runtime_hooks=[],
         excludes=[],
         noarchive=False,
         optimize=0,
     )
     pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

     exe = EXE(
         pyz,
         a.scripts,
         [],
         exclude_binaries=True,
         name='myserver',  # Specify your server executable name here
         debug=False,
         bootloader_ignore_signals=False,
         strip=False,
         upx=True,
         upx_exclude=[],
         runtime_tmpdir=None,
         console=True,  # Set to True to keep a console window open for server logging
         disable_windowed_traceback=False,
         argv_emulation=False,
         target_arch=None,
         codesign_identity=None,
         entitlements_file=None,
     )
     ```
     - Replace `'server.py'` with the actual filename of your server script if it differs.

6. **Save `main.spec` File**:

   - Save the `main.spec` file in the same directory where your `server.py` script is located (`server_project`).

7. **Run PyInstaller**:

   - In your terminal or command prompt, while still in the `server_project` directory, run PyInstaller with your `main.spec` file:
     ```
     pyinstaller main.spec
     ```

8. **Build Process**:

   - PyInstaller will start analyzing your script (`server.py`), resolving dependencies, and bundling everything into a standalone executable.

9. **Locate Executable**:

   - After the build completes successfully, navigate to the `dist` directory within your `server_project` directory. You should find your executable file named `myserver` (or `myserver.exe` on Windows).

10. **Testing**:

    - Run the generated executable (`myserver` or `myserver.exe`) to test your server application. It should start and listen for connections as configured in your `server.py` script.

11. **Graceful Shutdown**:

    - Ensure your server script handles exits gracefully, such as by catching `KeyboardInterrupt` (`Ctrl + C` in the terminal) to allow for clean shutdown of the server.

By following these steps, you'll have successfully created a standalone executable for your server script using PyInstaller, making it easier to distribute and run your server application on different systems.

# `server.exe`

To build an executable (`exe` file) for your `main.py` script using PyInstaller with specific options (`--onefile`, `--windowed`, `--name`), follow these steps:

### Step-by-Step Guide:

1. **Open Terminal (Command Prompt)**:

   - Open your terminal or command prompt application on your computer. You'll use this to run commands and navigate directories.

2. **Navigate to Your Project Directory**:

   - Use the `cd` command to change directory to where your `main.py` script is located. For example, if your script is in a directory named `game_project`, you would type:
     ```
     cd path/to/game_project
     ```
     Replace `path/to/game_project` with the actual path where your `main.py` script resides.

3. **Verify PyInstaller Installation**:

   - Before proceeding, ensure that PyInstaller is installed in your Python environment. You can check by running:
     ```
     pyinstaller --version
     ```
     If PyInstaller is installed, you'll see its version number. If not, you'll need to install it using `pip`. You can install PyInstaller with:
     ```
     pip install pyinstaller
     ```

4. **Run PyInstaller Command**:

   - Once in your project directory (`game_project`), run the following command to build your executable:

     ```bash
     pyinstaller main.py --onefile --name=mygame
     ```

     - `main.py`: Replace with the actual filename of your Python script if it differs.
     - `--onefile`: This option bundles everything into a single executable file.
     - `--windowed`: This option hides the console window, suitable for GUI applications.
     - `--name=mygame`: Specifies the name of the executable (`mygame.exe` on Windows, `mygame` on Unix-like systems).

5. **Build Process**:

   - PyInstaller will start analyzing your `main.py` script, resolving dependencies, and bundling everything into a standalone executable.

6. **Locate Executable**:

   - After the build completes successfully, navigate to the `dist` directory within your `game_project` directory. You should find your executable file named `mygame` (or `mygame.exe` on Windows).

7. **Testing**:

   - Run the generated executable (`mygame` or `mygame.exe`) to test your application. It should launch as a standalone windowed application, as configured by the `--windowed` option.

8. **Distribution**:

   - You can now distribute the generated executable (`mygame` or `mygame.exe`) to others. They can run it without needing Python or any dependencies installed separately.

By following these steps, you'll have successfully created a standalone executable for your Python script (`main.py`) using PyInstaller, configured to be a single-file, windowed application named `mygame`. Adjust the options (`--onefile`, `--windowed`, `--name`) according to your specific needs and preferences.

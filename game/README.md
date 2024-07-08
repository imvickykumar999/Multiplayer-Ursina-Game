
# `client.exe`

To handle the situation where your `main.py` takes input from the user and ensure all assets are included in the executable, you need to ensure the `PyInstaller` configuration includes all necessary files and handles user inputs correctly.

Here’s a step-by-step guide to creating an executable with `PyInstaller` for a script that takes user input and includes additional assets:

1. **Install PyInstaller**:
   Make sure `PyInstaller` is installed:

   ```sh
   pip install pyinstaller
   ```

2. **Organize Your Project**:
   Ensure your project directory is structured like this:

   ```
   your_project/
   ├── assets/
   │   ├── bullet.mp3
   │   ├── file2
   │   ├── file3
   │   └── file4
   ├── bullet.py
   ├── enemy.py
   ├── floor.py
   ├── main.py
   ├── map.py
   ├── network.py
   ├── player.py
   └── setup.py
   ```

3. **Create a Spec File**:
   First, generate a default spec file:

   ```sh
   pyinstaller main.py --onefile --windowed --name=mygame
   ```

4. **Edit the Spec File**:
   Edit the generated `mygame.spec` file to include your assets. Locate the `Analysis` section and add your assets to the `datas` list:

   ```spec
   # mygame.spec
   # -*- mode: python ; coding: utf-8 -*-
   
   block_cipher = None
   
   a = Analysis(
       ['main.py'],
       pathex=['.'],
       binaries=[],
       datas=[
           ('assets/bullet.mp3', 'assets'),
           ('assets/floor.png', 'assets'),
           ('assets/sky.png', 'assets'),
           ('assets/wall.png', 'assets')
       ],
       hiddenimports=['tkinter', 'ursina'],
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
       a.binaries,
       a.zipfiles,
       a.datas,
       [],
       name='mygame',
       debug=False,
       bootloader_ignore_signals=False,
       strip=False,
       upx=True,
       upx_exclude=[],
       runtime_tmpdir=None,
       console=False,  # Set to True if you need a console window for debugging
       disable_windowed_traceback=False,
       argv_emulation=False,  # Set to False as it's not needed for a GUI app without a console
       target_arch=None,
       codesign_identity=None,
       entitlements_file=None,
   )
   ```

5. **Handle User Input**:
   Ensure your `main.py` script correctly handles user input. For example:

   ```python
   from ursina import Ursina, Vec3
   from player import Player
   from network import Network
   import tkinter as tk
   from tkinter import simpledialog
   
   def get_user_input():
       root = tk.Tk()
       root.withdraw()
       
       # Define custom font
       custom_font = tk.font.Font(family="Helvetica", size=14, weight="bold")
       
       # Prompt for username
       username_dialog = tk.Toplevel(root)
       username_dialog.geometry("300x150")
       username_dialog.title("Enter Username")
       
       username_label = tk.Label(username_dialog, text="Enter your username:", font=custom_font)
       username_label.pack(pady=10)
       
       username_var = tk.StringVar()
       username_entry = tk.Entry(username_dialog, textvariable=username_var, font=custom_font, width=20)
       username_entry.pack(pady=5)
       username_entry.focus_set()
       
       def on_username_ok():
           username_dialog.destroy()
       
       ok_button = tk.Button(username_dialog, text="OK", command=on_username_ok, font=custom_font)
       ok_button.pack(pady=10)
       
       root.wait_window(username_dialog)
       
       username = username_var.get() or "default"
       
       # Prompt for server address
       server_dialog = tk.Toplevel(root)
       server_dialog.geometry("300x150")
       server_dialog.title("Enter Server Address")
       
       server_label = tk.Label(server_dialog, text="Enter server address:", font=custom_font)
       server_label.pack(pady=10)
       
       server_var = tk.StringVar()
       server_entry = tk.Entry(server_dialog, textvariable=server_var, font=custom_font, width=20)
       server_entry.pack(pady=5)
       server_entry.focus_set()
       
       def on_server_ok():
           server_dialog.destroy()
       
       ok_button = tk.Button(server_dialog, text="OK", command=on_server_ok, font=custom_font)
       ok_button.pack(pady=10)
       
       root.wait_window(server_dialog)
       
       server_addr = server_var.get()
       
       return username, server_addr
   
   def main():
       app = Ursina()
   
       username, server_addr = get_user_input()
       
       if server_addr:
           network = Network(server_addr, 12345, username)  # Example port number
           player = Player(position=Vec3(0, 1, 0), network=network)
           app.run()
       else:
           print("Server address input was canceled or not completed correctly")
   
   if __name__ == "__main__":
       main()
   ```

6. **Build the Executable**:
   Run `PyInstaller` with the spec file:

   ```sh
   pyinstaller mygame.spec
   ```

7. **Locate the Executable**:
   The executable will be created in the `dist` directory inside your project folder.

With this setup, your `main.py` script will prompt the user for input when the executable is run, and `PyInstaller` will package all required assets into the executable.

## ✅ 1. **Project Structure**

Ensure your folder looks like:

```
project_folder/
│
├── assets/               # All your game assets like textures, mp3, images
│   ├── background.jpg
│   ├── music.mp3
│   └── ...
├── bullet.py
├── enemy.py
├── floor.py
├── map.py
├── network.py
├── player.py
├── main.py               # Your main script
├── icon.ico              # Game icon (optional)
├── clickNplayGame.spec   # Custom PyInstaller spec
```

---

### ✅ 2. **Install Required Packages**

```bash
pip install pyinstaller pyarmor ursina panda3d psutil pillow pygame
```

---

### ✅ 3. **Generate Encrypted Version (Optional, for security)**

To obfuscate your source using **PyArmor**:

```bash
pyarmor gen -O dist main.py
```

Then use the generated file in `dist/main.py` as your main source.

---

### ✅ 4. **Create `.spec` File (already provided)**

Make sure `clickNplayGame.spec` includes:

* Your modules in `hiddenimports`
* `assets` folder as `datas`
* Ursina and Panda3D collected correctly
* Proper icon and output settings

✔ You're already doing this:

```python
icon='icon.ico',
console=False,  # You can set this to True during debugging
name='clickNplayGame',
```

---

### ✅ 5. **Build the Executable**

You can do it in two ways:

#### 👉 A. Build directly from `.py`:

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
```

#### 👉 B. (Recommended) Build using `.spec` file:

```bash
pyinstaller clickNplayGame.spec
```

This gives better control and ensures assets and imports are handled exactly as defined.

---

### ✅ 6. **Test the Executable**

After build, your `dist/clickNplayGame.exe` should run **without showing the console** and launch the fullscreen game GUI.

Check that:

* Music plays
* Background shows correctly
* Network connection works
* All imports are intact

---

### ✅ 7. **Optional: Shrink Size**

Use `UPX` to compress the executable size:

* Install: [https://upx.github.io/](https://upx.github.io/)
* Add `--upx-dir` in PyInstaller command, or leave `upx=True` in `.spec`

---

### ✅ 8. **Distribute**

Once built:

* Share `dist/clickNplayGame.exe` to others
* They can join your server using `vicks.imvickykumar999.online` and port `11923`

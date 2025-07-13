## 🐍 Convert Python Script to EXE (Windows + Linux) using PyInstaller & PyArmor

If you've ever made a Python app or game and wanted to **share it without exposing your code**, this guide is for you. We'll cover how to convert a Python `.py` file into a standalone `.exe` on Windows—and also make it executable on Linux (Ubuntu).

> ✅ **Bonus**: We'll protect the source code with [PyArmor](https://pyarmor.readthedocs.io/en/latest/).

---

## 📦 Step 1: Install Requirements

First, install the tools:

```bash
pip install pyinstaller pyarmor
```

---

## 🔒 Step 2: Protect the Script with PyArmor (optional)

To encrypt your `main.py` file:

```bash
pyarmor gen -O dist main.py
```

This will generate a protected version inside `dist/main.py`.

You can now use this protected script instead of the original when building the `.exe`.

---

## 🛠️ Step 3: Create EXE with PyInstaller

Basic command:

```bash
pyinstaller --onefile main.py
```

But we can go further. For example, include:

* Hidden imports like `art`, `json`, etc.
* A custom icon for branding

```bash
pyinstaller --onefile ^
--hidden-import=art ^
--hidden-import=json ^
--icon=icon.ico ^
main.py
```

> 🖼️ Replace `icon.ico` with your custom icon file.

Once complete, you’ll find the final `.exe` in the `dist/` folder.

---

## 📂 Step 4: Run the Executable

Go to the output folder:

```bash
cd dist
./main.exe
```

Or just double-click it from File Explorer in Windows.

---

## 🐧 BONUS: Make It Work on Ubuntu/Linux

If you're on Linux and want to run the protected file:

```bash
cd dist
file main      # Check architecture
chmod +x main  # Make it executable
./main         # Run it
```

> Make sure your Linux Python environment has the required dependencies.

---

## 📸 Screenshots

**Windows EXE output:**

![Windows EXE Output](https://github.com/user-attachments/assets/99962b82-4e9d-40a5-b900-5f88a7eb6bae)

---

**Ubuntu Executable:**

![Ubuntu Output](https://github.com/user-attachments/assets/9e781451-001b-4e54-877b-39038873a553)

---

## ✅ Summary

| Tool          | Purpose                     |
| ------------- | --------------------------- |
| `pyinstaller` | Convert `.py` to `.exe`     |
| `pyarmor`     | Encrypt/protect your script |
| `icon.ico`    | Add a professional look     |

---

### 🔗 Ready to Share!

Once built, you can upload your EXE to:

* Google Drive
* itch.io
* Your own website (like `imvickykumar999.online`)
* Or send it directly via WhatsApp/Telegram

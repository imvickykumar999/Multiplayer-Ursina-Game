# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Collect all data, binaries, and imports for panda3d and ursina
datas = [('assets', 'assets')]
binaries = []
hiddenimports = ['bullet', 'enemy', 'floor', 'map', 'network', 'player']

# Panda3D
panda3d_data = collect_all('panda3d')
datas += panda3d_data[0]
binaries += panda3d_data[1]
hiddenimports += panda3d_data[2]

# Ursina
ursina_data = collect_all('ursina')
datas += ursina_data[0]
binaries += ursina_data[1]
hiddenimports += ursina_data[2]

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='clickNplayGame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set True if you want console output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Optional: Your game icon
)

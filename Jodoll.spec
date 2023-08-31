# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['E:\\Dev\\ppython\\Jodoll\\designer.py', 
    'E:\\Dev\\ppython\\Jodoll\\Ui_once.py', 
    'E:\\Dev\\ppython\\Jodoll\\oracle_long_conn.py'],
    pathex=[],
    binaries=[],
    datas=[('E:\\Dev\\ppython\\Jodoll', './')],
    hiddenimports=[],
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
    name='Jodoll',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='E:\\Dev\\ppython\\Jodoll\\32tool.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

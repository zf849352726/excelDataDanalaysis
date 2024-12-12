# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py', 'config.py', 'D:\\python_learn\\excel_data\\final_cal\\Calculator.py','D:\\python_learn\\excel_data\\final_cal\\ExcelProcessor.py','D:\\python_learn\\excel_data\\final_cal\\FileManager.py','D:\\python_learn\\excel_data\\final_cal\\FilterStrategy.py','D:\\python_learn\\excel_data\\final_cal\\ReportGenerator.py','D:\\python_learn\\excel_data\\final_cal\\settings.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\python_learn\\excel_data\\assets','assets'),('D:\\python_learn\\excel_data\\price','price'),('D:\\python_learn\\excel_data\\ui','ui')],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['data/gui.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data')],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'reportlab',
        'TikTokLive',
        'tkinter',
        'PIL',
        'reportlab.lib',
        'reportlab.platypus',
        'reportlab.lib.styles',
        'reportlab.lib.colors',
        'reportlab.lib.pagesizes',
        'reportlab.lib.units',
    ],
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
    name='TikTokLiveMonitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Masquer la console pour GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)


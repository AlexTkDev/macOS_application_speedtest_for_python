# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['speedtest_app/alexs_speedtest.py'],
    pathex=[],
    binaries=[],
    datas=[('test_history.json', '.')],
    hiddenimports=[
        'speedtest_cli',
        'speedtest_app.network_adapter_information',
        'matplotlib',
        'tkinter',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.figure'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='alexs_speedtest',
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
    icon=['speedtest.icns'],
)
app = BUNDLE(
    exe,
    name='Alex_SpeedTest.app',
    icon='speedtest.icns',
    bundle_identifier='org.AlexTkDev.speedtest',
    version='3.0.0',
)
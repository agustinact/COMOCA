# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(
    ['Main.py', 'App.py', 'Login.py'],
    pathex=['C:\\Users\\fliacarbajal\\Desktop\\APP'],
    binaries=[],
    datas=[
        ('nuevaDB.sqlite', '.'),
        ('Auxiliares/*.py', 'Auxiliares'),
        ('Tablas/*.py', 'Tablas'),
        ('Tabs/*.py', 'Tabs'),
        ('images/*.png', 'images'),
        ('remitos/*.xlsx', 'remitos'),
        ('Reportes/Ingresos/*.xlsx', 'Reportes/Ingresos'),
        ('Reportes/Salidas/*.xlsx', 'Reportes/Salidas'),
        ('Reportes/Romaneos/*.xlsx', 'Reportes/Romaneos')
    ],
    hiddenimports=[
        'babel.numbers',
        'babel.dates',
        'babel.localedata',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='COMOCA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Change to False if you don't want a console window
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='COMOCA',
)

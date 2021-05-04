import PyInstaller.__main__

from environment import environment

PyInstaller.__main__.run([
    'src/main.py',
    '--name',
    'mer.io_v{0}'.format(environment['version']),
    '--specpath',
    'src/spec',
    '--distpath',
    'src/dist',
    '--onedir',
    '--windowed',
    '--noconfirm',
])
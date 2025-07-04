import os
from pathlib import Path

def configurar_startup(ativar):
    startup_dir = Path(os.getenv('APPDATA')) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    atalho = startup_dir / "AutoStarter.bat"
    caminho = Path(__file__).resolve().parents[1] / "main.py"

    if ativar:
        with open(atalho, "w") as f:
            f.write(f'@echo off\npython "{caminho}"\n')
    else:
        if atalho.exists():
            atalho.unlink()

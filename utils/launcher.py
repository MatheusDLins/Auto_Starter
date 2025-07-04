import webbrowser
import subprocess

def abrir_itens(config):
    for site in config.get("sites", []):
        webbrowser.open(site)
    for app in config.get("apps", []):
        try:
            subprocess.Popen(app)
        except Exception as e:
            print(f"Erro ao abrir {app}: {e}")

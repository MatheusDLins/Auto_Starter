import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from utils.launcher import abrir_itens
from utils.autostart import configurar_startup

CONFIG_PATH = "config.json"

def carregar_config():
    if not os.path.exists(CONFIG_PATH):
        return {"sites": [], "apps": [], "auto_start": False}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def salvar_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def adicionar_item(tipo):
    entrada = simpledialog.askstring("Novo item", f"Digite o {'URL' if tipo == 'site' else 'caminho do aplicativo'}:")
    if entrada:
        config[tipo + "s"].append(entrada)
        salvar_config(config)
        atualizar_lista()

def remover_item():
    selecionado = lista.curselection()
    if not selecionado:
        return
    index = selecionado[0]
    todos = config["sites"] + config["apps"]
    item = todos[index]
    if item in config["sites"]:
        config["sites"].remove(item)
    else:
        config["apps"].remove(item)
    salvar_config(config)
    atualizar_lista()

def atualizar_lista():
    lista.delete(0, tk.END)
    for site in config["sites"]:
        lista.insert(tk.END, f"[Site] {site}")
    for app in config["apps"]:
        lista.insert(tk.END, f"[App] {app}")

def executar_itens():
    abrir_itens(config)

def toggle_auto_start():
    config["auto_start"] = not config["auto_start"]
    salvar_config(config)
    configurar_startup(config["auto_start"])
    status = "ativado" if config["auto_start"] else "desativado"
    messagebox.showinfo("Inicialização automática", f"Inicialização automática {status}.")

# Interface
config = carregar_config()
root = tk.Tk()
root.title("Auto Starter")

lista = tk.Listbox(root, width=70)
lista.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Adicionar Site", command=lambda: adicionar_item("site")).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Adicionar App", command=lambda: adicionar_item("app")).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Remover", command=remover_item).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Executar Todos", command=executar_itens).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Auto Start", command=toggle_auto_start).grid(row=0, column=4, padx=5)

atualizar_lista()
root.mainloop()

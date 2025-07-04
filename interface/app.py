import customtkinter as ctk
import json
import os
from tkinter import messagebox
from utils.launcher import abrir_itens

CONFIG_PATH = "config.json"

class AutoStarterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Auto Starter")
        self.geometry("700x550")
        self.config = self.carregar_config()

        ctk.set_appearance_mode(self.config.get("tema", "System"))
        ctk.set_default_color_theme("blue")

        self.menu = ctk.CTkSegmentedButton(self, values=["Início", "Configurações"], command=self.trocar_pagina)
        self.menu.pack(pady=10)

        self.frame_inicio = self.criar_pagina_inicio()
        self.frame_config = self.criar_pagina_config()
        self.frame_inicio.pack(fill="both", expand=True)

    def carregar_config(self):
        if not os.path.exists(CONFIG_PATH):
            return {"sites": [], "tema": "System"}
        with open(CONFIG_PATH, "r") as f:
            dados = json.load(f)

        if isinstance(dados.get("sites", [])[0], str):
            dados["sites"] = [{"nome": url, "caminho": url} for url in dados["sites"]]

        if "tema" not in dados:
            dados["tema"] = "System"

        return dados

    def salvar_config(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=4)

    def trocar_pagina(self, valor):
        self.frame_inicio.pack_forget()
        self.frame_config.pack_forget()
        if valor == "Início":
            self.frame_inicio.pack(fill="both", expand=True)
        else:
            self.frame_config.pack(fill="both", expand=True)

    def criar_pagina_inicio(self):
        frame = ctk.CTkFrame(self)

        self.entry_busca = ctk.CTkEntry(frame, placeholder_text="Buscar site...")
        self.entry_busca.pack(padx=10, pady=(10, 5), fill="x")
        self.entry_busca.bind("<KeyRelease>", self.filtrar_lista)

        btns = ctk.CTkFrame(frame)
        btns.pack(pady=5)

        ctk.CTkButton(btns, text="Adicionar Site", command=self.adicionar_site).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btns,text="Executar Todos",command=self.executar_sites,fg_color="#28a745",hover_color="#218838").grid(row=0, column=1, padx=5)

        ctk.CTkButton(btns, text="Excluir Todos", command=self.confirmar_excluir_todos).grid(row=0, column=2, padx=5)

        self.scroll_frame = ctk.CTkScrollableFrame(frame, height=400)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.atualizar_lista()
        return frame

    def criar_pagina_config(self):
        frame = ctk.CTkFrame(self)
        ctk.CTkLabel(frame, text="Tema: ").pack(pady=10)
        self.tema_menu = ctk.CTkOptionMenu(frame, values=["Light", "Dark", "System"], command=self.alterar_tema)
        self.tema_menu.set(self.config.get("tema", "System"))
        self.tema_menu.pack()
        return frame

    def alterar_tema(self, novo_tema):
        ctk.set_appearance_mode(novo_tema)
        self.config["tema"] = novo_tema
        self.salvar_config()

    def atualizar_lista(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        busca = self.entry_busca.get().lower()
        for item in self.config["sites"]:
            if busca in item["nome"].lower():
                linha = ctk.CTkFrame(self.scroll_frame)
                linha.pack(fill="x", padx=5, pady=2)

                label = ctk.CTkLabel(linha, text=f"[Site] {item['nome']}", anchor="w")
                label.pack(side="left", expand=True, padx=5)

                ctk.CTkButton(linha, text="Editar", width=70, command=lambda i=item: self.editar_item(i)).pack(side="right", padx=2)
                ctk.CTkButton(linha, text="Excluir", width=70, command=lambda i=item: self.confirmar_excluir_individual(i)).pack(side="right", padx=2)

    def adicionar_site(self):
        self.abrir_janela_edicao()

    def editar_item(self, antigo):
        self.abrir_janela_edicao(antigo)

    def abrir_janela_edicao(self, item=None):
        janela = ctk.CTkToplevel(self)
        janela.title("Editar Site" if item else "Novo Site")
        janela.geometry("300x280")
        janela.grab_set()

        ctk.CTkLabel(janela, text="Nome:").pack(pady=(10, 0))
        entry_nome = ctk.CTkEntry(janela)
        entry_nome.pack(padx=10, pady=5, fill="x")

        ctk.CTkLabel(janela, text="URL:").pack(pady=(10, 0))
        entry_url = ctk.CTkEntry(janela)
        entry_url.pack(padx=10, pady=5, fill="x")

        if item:
            entry_nome.insert(0, item["nome"])
            entry_url.insert(0, item["caminho"])

        def salvar():
            nome = entry_nome.get().strip()
            url = entry_url.get().strip()
            if nome and url:
                if item:
                    index = self.config["sites"].index(item)
                    self.config["sites"][index] = {"nome": nome, "caminho": url}
                else:
                    self.config["sites"].append({"nome": nome, "caminho": url})
                self.salvar_config()
                self.atualizar_lista()
                janela.destroy()
            else:
                messagebox.showwarning("Aviso", "Preencha todos os campos.")

        ctk.CTkButton(janela, text="Salvar", command=salvar).pack(pady=10)

    def confirmar_excluir_individual(self, item):
        if messagebox.askyesno("Confirmação", f"Deseja realmente excluir '{item['nome']}'?"):
            self.config["sites"].remove(item)
            self.salvar_config()
            self.atualizar_lista()

    def confirmar_excluir_todos(self):
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir todos os sites?"):
            self.config = {"sites": [], "tema": self.config.get("tema", "System")}
            self.salvar_config()
            self.atualizar_lista()

    def executar_sites(self):
        import webbrowser
        for item in self.config["sites"]:
            try:
                webbrowser.open(item["caminho"])
            except Exception as e:
                print(f"Erro ao abrir {item['nome']}: {e}")

    def filtrar_lista(self, event=None):
        self.atualizar_lista()

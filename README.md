# 🚀 Auto Starter GUI

Aplicativo com interface gráfica feito em Python, que permite cadastrar sites personalizados para abrir com um clique. Ideal para quem deseja automatizar o início das tarefas diárias no PC, como abrir o e-mail, YouTube, ou qualquer URL específica.

---

### ✅ O que o Auto Starter faz?

- Permite **cadastrar sites** com nomes personalizados
- Executa todos os sites com 1 clique
- Permite editar, excluir e pesquisar sites da lista
- Possui **modo claro/escuro**
- Interface moderna e leve.

---

### 📦 Como rodar o projeto localmente?

#### 1. Clone o repositório

- git clone https://github.com/MatheusDLins/Auto_Starter.git
- cd Auto_Starter

#### 2. Crie um ambiente virtual (opcional)

- python -m venv venv
- venv\\Scripts\\activate    (Windows)


#### 3. Instale as dependências

- pip install -r requirements.txt


#### 4. Execute o app

- python main.py


### 📁 Estrutura do projeto

```bash
Auto_Starter/
├── main.py                 # Arquivo principal
├── config.json             # Configurações salvas e sites/programas cadastrados (gerado em tempo de execução)
├── interface/
│   └── app.py              # Interface com CustomTkinter
└── README.md

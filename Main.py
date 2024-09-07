import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3

# Função para conectar ao banco de dados SQLite
def connect_to_db():
    return sqlite3.connect('estoque.db')

# Criar tabelas se não existirem
def create_tables():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER DEFAULT 0,
            preco REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close()

# Chama a função para criar tabelas quando o aplicativo é iniciado
create_tables()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Controle de Estoque")
        self.geometry("1280x720")
        self.config(bg="#f0f0f0")

        # Criar todos os frames
        self.home_frame = HomeFrame(self)
        self.cadastro_frame = CadastroFrame(self)
        self.gerenciamento_frame = GerenciamentoFrame(self)
        self.procurar_frame = ProcurarFrame(self)

        # Colocar todos os frames na mesma posição
        for frame in (self.home_frame, self.cadastro_frame, self.gerenciamento_frame, self.procurar_frame):
            frame.place(relwidth=1, relheight=1)

        # Mostrar a tela principal por padrão
        self.show_frame(self.home_frame)

    def show_frame(self, frame):
        frame.tkraise()

class HomeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.parent = parent

        # Título do aplicativo
        title_label = tk.Label(self, text="Sistema de Controle de Estoque", font=('Arial', 24, 'bold'), bg="#f0f0f0")
        title_label.pack(pady=20)

        # Descrição do aplicativo
        desc_label = tk.Label(self, text="Escolha uma das opções abaixo para gerenciar o seu estoque.", font=('Arial', 14), bg="#f0f0f0")
        desc_label.pack(pady=10)

        # Botões da página inicial
        btn_style = {'width': 40, 'height': 3, 'font': ('Arial', 14, 'bold'), 'bg': '#007BFF', 'fg': 'white'}

        btn_cadastrar = tk.Button(self, text="Cadastrar Produto", **btn_style, command=self.show_cadastro)
        btn_cadastrar.pack(pady=10)

        btn_estoque = tk.Button(self, text="Gerenciar Estoque", **btn_style, command=self.show_gerenciamento)
        btn_estoque.pack(pady=10)

        btn_procurar = tk.Button(self, text="Procurar Produto no Estoque", **btn_style, command=self.show_procurar)
        btn_procurar.pack(pady=10)

    def show_cadastro(self):
        self.parent.show_frame(self.parent.cadastro_frame)

    def show_gerenciamento(self):
        self.parent.show_frame(self.parent.gerenciamento_frame)

    def show_procurar(self):
        self.parent.show_frame(self.parent.procurar_frame)

class CadastroFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.parent = parent

        label = tk.Label(self, text="Cadastro de Produto", font=('Arial', 24, 'bold'), bg="#f0f0f0")
        label.pack(pady=20)

        tk.Label(self, text="Nome do Produto:", font=('Arial', 14), bg="#f0f0f0").pack(pady=5)
        self.nome_entry = tk.Entry(self, font=('Arial', 14))
        self.nome_entry.pack(pady=5)

        tk.Label(self, text="Quantidade:", font=('Arial', 14), bg="#f0f0f0").pack(pady=5)
        self.quantidade_entry = tk.Entry(self, font=('Arial', 14))
        self.quantidade_entry.pack(pady=5)

        tk.Label(self, text="Preço:", font=('Arial', 14), bg="#f0f0f0").pack(pady=5)
        self.preco_entry = tk.Entry(self, font=('Arial', 14))
        self.preco_entry.pack(pady=5)

        tk.Button(self, text="Salvar", font=('Arial', 14, 'bold'), bg="#28a745", fg="white", command=self.salvar_produto).pack(pady=10)

        btn_back = tk.Button(self, text="Voltar", font=('Arial', 14, 'bold'), command=self.voltar)
        btn_back.pack(pady=10)

    def salvar_produto(self):
        nome_produto = self.nome_entry.get().strip()
        quantidade = self.quantidade_entry.get().strip()
        preco = self.preco_entry.get().strip()

        if not nome_produto:
            messagebox.showwarning("Cadastro de Produto", "O nome do produto não pode estar vazio.")
            return

        if not quantidade.isdigit():
            messagebox.showwarning("Cadastro de Produto", "A quantidade deve ser um número inteiro válido.")
            return

        if not preco.replace('.', '', 1).isdigit():
            messagebox.showwarning("Cadastro de Produto", "O preço deve ser um número decimal válido.")
            return

        quantidade = int(quantidade)
        preco = float(preco)

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            query = "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)"
            cursor.execute(query, (nome_produto, quantidade, preco))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Cadastro de Produto", f"Produto '{nome_produto}' cadastrado com sucesso!")
            self.nome_entry.delete(0, tk.END)
            self.quantidade_entry.delete(0, tk.END)
            self.preco_entry.delete(0, tk.END)
        except sqlite3.Error as err:
            messagebox.showerror("Erro", f"Erro ao cadastrar produto: {err}")

    def voltar(self):
        self.parent.show_frame(self.parent.home_frame)

class GerenciamentoFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.parent = parent

        label = tk.Label(self, text="Gerenciamento de Estoque", font=('Arial', 24, 'bold'), bg="#f0f0f0")
        label.pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("id", "nome", "quantidade", "preco"), show='headings')
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("quantidade", text="Quantidade")
        self.tree.heading("preco", text="Preço")
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        btn_refresh = tk.Button(self, text="Atualizar Dados", font=('Arial', 14, 'bold'), command=self.carregar_dados)
        btn_refresh.pack(pady=10)

        btn_back = tk.Button(self, text="Voltar", font=('Arial', 14, 'bold'), command=self.voltar)
        btn_back.pack(pady=10)

        self.carregar_dados()

        self.tree.bind("<Double-1>", self.editar_produto)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            query = "SELECT id, nome, quantidade, preco FROM produtos"
            cursor.execute(query)
            for row in cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
            cursor.close()
            conn.close()
        except sqlite3.Error as err:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {err}")

    def editar_produto(self, event):
        item = self.tree.selection()[0]
        produto_id = self.tree.item(item, 'values')[0]

        nome = simpledialog.askstring("Editar Produto", "Novo nome do produto:", initialvalue=self.tree.item(item, 'values')[1])
        if nome is None: return

        quantidade = simpledialog.askinteger("Editar Produto", "Nova quantidade:", initialvalue=self.tree.item(item, 'values')[2])
        if quantidade is None: return

        preco = simpledialog.askfloat("Editar Produto", "Novo preço:", initialvalue=self.tree.item(item, 'values')[3])
        if preco is None: return

        if not nome:
            messagebox.showwarning("Editar Produto", "O nome do produto não pode estar vazio.")
            return

        if quantidade is None or quantidade < 0:
            messagebox.showwarning("Editar Produto", "A quantidade deve ser um número inteiro não negativo.")
            return

        if preco is None or preco < 0:
            messagebox.showwarning("Editar Produto", "O preço deve ser um número decimal não negativo.")
            return

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            query = "UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?"
            cursor.execute(query, (nome, quantidade, preco, produto_id))
            conn.commit()
            cursor.close()
            conn.close()
            self.carregar_dados()
            messagebox.showinfo("Editar Produto", "Produto atualizado com sucesso!")
        except sqlite3.Error as err:
            messagebox.showerror("Erro", f"Erro ao atualizar produto: {err}")

    def voltar(self):
        self.parent.show_frame(self.parent.home_frame)

class ProcurarFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.parent = parent

        label = tk.Label(self, text="Procurar Produto", font=('Arial', 24, 'bold'), bg="#f0f0f0")
        label.pack(pady=20)

        tk.Label(self, text="Nome do Produto:", font=('Arial', 14), bg="#f0f0f0").pack(pady=5)
        self.nome_entry = tk.Entry(self, font=('Arial', 14))
        self.nome_entry.pack(pady=5)

        tk.Button(self, text="Buscar", font=('Arial', 14, 'bold'), command=self.buscar_produto).pack(pady=10)

        self.resultado_texto = tk.Label(self, text="", font=('Arial', 14), bg="#f0f0f0")
        self.resultado_texto.pack(pady=20)

        btn_back = tk.Button(self, text="Voltar", font=('Arial', 14, 'bold'), command=self.voltar)
        btn_back.pack(pady=10)

    def buscar_produto(self):
        nome_produto = self.nome_entry.get().strip()
        if nome_produto:
            try:
                conn = connect_to_db()
                cursor = conn.cursor()
                query = "SELECT nome, quantidade, preco FROM produtos WHERE nome LIKE ?"
                cursor.execute(query, ('%' + nome_produto + '%',))
                resultados = cursor.fetchall()
                if resultados:
                    texto_resultado = "\n".join([f"Nome: {r[0]}, Quantidade: {r[1]}, Preço: R${r[2]:.2f}" for r in resultados])
                else:
                    texto_resultado = "Nenhum produto encontrado."
                self.resultado_texto.config(text=texto_resultado)
                cursor.close()
                conn.close()
            except sqlite3.Error as err:
                messagebox.showerror("Erro", f"Erro ao buscar produto: {err}")
        else:
            messagebox.showwarning("Busca de Produto", "Por favor, digite um nome de produto.")

    def voltar(self):
        self.parent.show_frame(self.parent.home_frame)

if __name__ == "__main__":
    app = App()
    app.mainloop()

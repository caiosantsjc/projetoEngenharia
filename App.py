import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3


# Função para conectar ao banco de dados SQLite
def connect_to_db():
    return sqlite3.connect('mantimentos.db')


# Criar tabelas se não existirem
def create_tables():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mantimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade REAL DEFAULT 0.0,
            unidade TEXT DEFAULT 'unidade',
            categoria TEXT DEFAULT 'Outros',
            preco REAL DEFAULT 0.0,
            validade TEXT DEFAULT ''
        )
    ''')
    conn.commit()
    conn.close()


# Chama a função para criar tabelas quando o aplicativo é iniciado
create_tables()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Mantimentos do Lar")
        self.geometry("1280x720")
        self.config(bg="#f0f0f0")

        # Frames principais
        self.frames = {}
        for FrameClass in (HomeFrame, CadastroFrame, GerenciamentoFrame, ProcurarFrame):
            frame = FrameClass(self)
            self.frames[FrameClass] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(HomeFrame)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()


class HomeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.parent = parent

        # Título
        tk.Label(self, text="Gerenciador de Mantimentos do Lar", font=('Arial', 24, 'bold'), bg="#f0f0f0").pack(pady=20)

        # Descrição
        tk.Label(self, text="Organize seus alimentos e evite desperdícios.", font=('Arial', 14), bg="#f0f0f0").pack(pady=10)

        # Botões de navegação
        btn_style = {'width': 30, 'height': 2, 'font': ('Arial', 14, 'bold'), 'bg': '#007BFF', 'fg': 'white'}
        tk.Button(self, text="Cadastrar Mantimento", **btn_style, command=lambda: parent.show_frame(CadastroFrame)).pack(pady=10)
        tk.Button(self, text="Gerenciar Mantimentos", **btn_style, command=lambda: parent.show_frame(GerenciamentoFrame)).pack(pady=10)
        tk.Button(self, text="Procurar Mantimento", **btn_style, command=lambda: parent.show_frame(ProcurarFrame)).pack(pady=10)


class CadastroFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.parent = parent

        tk.Label(self, text="Cadastro de Mantimento", font=('Arial', 24, 'bold'), bg="#f0f0f0").pack(pady=20)

        # Campos de entrada
        self.nome_entry = self.create_input("Nome do Mantimento:")
        self.quantidade_entry = self.create_input("Quantidade:")
        self.unidade_entry = self.create_input("Unidade (ex: kg, L):")
        self.categoria_entry = self.create_input("Categoria (ex: Grãos, Laticínios):")
        self.preco_entry = self.create_input("Preço (opcional):")
        self.validade_entry = self.create_input("Validade (opcional, ex: 2024-12-31):")

        # Botão de salvar
        tk.Button(self, text="Salvar", font=('Arial', 14, 'bold'), bg="#28a745", fg="white", command=self.salvar_mantimento).pack(pady=10)

        # Botão de voltar
        tk.Button(self, text="Voltar", font=('Arial', 14, 'bold'), command=lambda: parent.show_frame(HomeFrame)).pack(pady=10)

    def create_input(self, label_text):
        tk.Label(self, text=label_text, font=('Arial', 14), bg="#f0f0f0").pack(pady=5)
        entry = tk.Entry(self, font=('Arial', 14))
        entry.pack(pady=5)
        return entry

    def salvar_mantimento(self):
        nome = self.nome_entry.get().strip()
        quantidade = self.quantidade_entry.get().strip()
        unidade = self.unidade_entry.get().strip() or "unidade"
        categoria = self.categoria_entry.get().strip() or "Outros"
        preco = self.preco_entry.get().strip()
        validade = self.validade_entry.get().strip()

        if not nome:
            messagebox.showwarning("Erro", "O nome do mantimento não pode estar vazio.")
            return
        if not quantidade.replace('.', '', 1).isdigit() or float(quantidade) < 0:
            messagebox.showwarning("Erro", "A quantidade deve ser um número válido.")
            return

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO mantimentos (nome, quantidade, unidade, categoria, preco, validade)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, float(quantidade), unidade, categoria, float(preco or 0.0), validade))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Mantimento cadastrado com sucesso!")
            self.limpar_campos()
        except sqlite3.Error as err:
            messagebox.showerror("Erro", f"Erro ao salvar mantimento: {err}")

    def limpar_campos(self):
        for entry in (self.nome_entry, self.quantidade_entry, self.unidade_entry, self.categoria_entry, self.preco_entry, self.validade_entry):
            entry.delete(0, tk.END)


class GerenciamentoFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.parent = parent

        tk.Label(self, text="Gerenciamento de Mantimentos", font=('Arial', 24, 'bold'), bg="#f0f0f0").pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "Quantidade", "Unidade", "Categoria", "Preço", "Validade"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=150)
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        # Botões
        tk.Button(self, text="Atualizar Dados", font=('Arial', 14, 'bold'), command=self.carregar_dados).pack(pady=10)
        tk.Button(self, text="Voltar", font=('Arial', 14, 'bold'), command=lambda: parent.show_frame(HomeFrame)).pack(pady=10)

        self.carregar_dados()

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, quantidade, unidade, categoria, preco, validade FROM mantimentos")
            for row in cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
            conn.close()
        except sqlite3.Error as err:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {err}")


class ProcurarFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.parent = parent

        tk.Label(self, text="Procurar Mantimento", font=('Arial', 24, 'bold'), bg="#f0f0f0").pack(pady=20)

        self.nome_entry = self.create_input("Nome do Mantimento:")
        tk.Button(self, text="Buscar", font=('Arial', 14, 'bold'), command=self.buscar_mantimento).pack(pady=10)

        self.resultado_label = tk.Label(self, text="", font=('Arial', 14), bg="#f0f0f0", wraplength=800)
        self.resultado_label.pack(pady=20)

        tk.Button(self, text="Voltar", font=('Arial', 14, 'bold'), command=lambda: parent.show_frame(HomeFrame)).pack(pady=10)

    def create_input(self, label_text):
        tk.Label(self, text=label_text, font=('Arial', 14), bg="#f0f0f0").pack(pady=5)
        entry = tk.Entry(self, font=('Arial', 14))
        entry.pack(pady=5)
        return entry

    def buscar_mantimento(self):
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showwarning("Busca de Mantimento", "Digite um nome para busca.")
            return
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nome, quantidade, unidade, categoria, preco, validade FROM mantimentos WHERE nome LIKE ?", ('%' + nome + '%',))
            resultados = cursor.fetchall()
            conn.close()

            if resultados:
                resultado_texto = "\n".join([
                    f"Nome: {r[0]}, Quantidade: {r[1]} {r[2]}, Categoria: {r[3]}, Preço: R${r[4]:.2f}, Validade: {r[5]}"
                    for r in resultados
                ])
            else:
                resultado_texto = "Nenhum mantimento encontrado."
            self.resultado_label.config(text=resultado_texto)
        except sqlite3.Error as err:
            messagebox.showerror("Erro", f"Erro ao buscar mantimento: {err}")


if __name__ == "__main__":
    app = App()
    app.mainloop()

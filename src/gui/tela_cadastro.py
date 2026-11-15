import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from src.dominio.cliente import Cliente


class TelaCadastro(tk.Toplevel):
    # busca cpf ou cadastra um novo

    def __init__(self, master, clientes: dict, ao_finalizar_cadastro):
        super().__init__(master)
        self.title("SmartGas - Cadastro")
        self.geometry("600x400")
        self.clientes = clientes
        self.ao_finalizar_cadastro = ao_finalizar_cadastro
        self.janela_principal = master

        # Garante que o menu volte se o usuário fechar a janela no "X"
        self.protocol("WM_DELETE_WINDOW", self._voltar)

        titulo = tk.Label(self, text="Identificação do Cliente", font=("Arial", 14, "bold"))
        titulo.pack(side="top", pady=10)

        painel = tk.Frame(self)

        rotulo_cpf = tk.Label(painel, text="CPF:")
        rotulo_cpf.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.campo_cpf = tk.Entry(painel, width=20)
        self.campo_cpf.grid(row=0, column=1, padx=5, pady=5)
        self.campo_cpf.focus()

        self.botao_buscar = tk.Button(painel, text="Buscar", command=self._ao_clicar_buscar)
        self.botao_buscar.grid(row=0, column=2, padx=5, pady=5)

        rotulo_nome = tk.Label(painel, text="Nome:")
        rotulo_nome.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.campo_nome = tk.Entry(painel, width=20, state="disabled")
        self.campo_nome.grid(row=1, column=1, padx=5, pady=5)

        rotulo_nascimento = tk.Label(painel, text="Nascimento:")
        rotulo_nascimento.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.campo_nascimento = tk.Entry(painel, width=20, state="disabled")
        self.campo_nascimento.grid(row=2, column=1, padx=5, pady=5)

        painel.pack(expand=True)

        self.campo_cpf.bind("<Down>", lambda evento: self.campo_nome.focus())
        self.campo_nome.bind("<Up>", lambda evento: self.campo_cpf.focus())
        self.campo_nome.bind("<Down>", lambda evento: self.campo_nascimento.focus())
        self.campo_nascimento.bind("<Up>", lambda evento: self.campo_nome.focus())
        self.bind("<Return>", lambda evento: self._ao_pressionar_enter())

        painel_botoes = tk.Frame(self)
        self.botao_cadastrar = tk.Button(
            painel_botoes, text="Cadastrar", state="disabled", command=self._ao_clicar_cadastrar
        )
        self.botao_cadastrar.grid(row=0, column=0, padx=5, pady=5)

        self.botao_voltar = tk.Button(painel_botoes, text="Voltar", command=self._voltar)
        self.botao_voltar.grid(row=0, column=1, padx=5, pady=5)
        painel_botoes.pack(side="bottom", pady=10)

    def _voltar(self):
        self.janela_principal.deiconify()
        self.destroy()

    def _ao_pressionar_enter(self):
        if str(self.botao_cadastrar["state"]) == "disabled":
            self._ao_clicar_buscar()
        else:
            self._ao_clicar_cadastrar()

    def _ao_clicar_buscar(self):
        try:
            cpf = self.campo_cpf.get().strip()
            if not cpf or not cpf.isdigit():
                self.campo_cpf.delete(0, tk.END)
                self.campo_cpf.focus()
                raise ValueError("Digite um CPF válido.")

            if cpf in self.clientes:
                cliente = self.clientes[cpf]
                messagebox.showinfo("Cliente encontrado", f"Olá, {cliente.nome}!", parent=self)
                self.destroy()
                self.ao_finalizar_cadastro(cliente)
            else:
                messagebox.showinfo(
                    "Novo cadastro", "CPF não encontrado. Preencha Nome e Nascimento.", parent=self
                )
                self.campo_nome.config(state="normal")
                self.campo_nascimento.config(state="normal")
                self.botao_cadastrar.config(state="normal")
                self.campo_nome.focus()

        except ValueError as erro:
            messagebox.showerror("Dados inválidos", str(erro), parent=self)

    def _ao_clicar_cadastrar(self):
        try:
            cpf = self.campo_cpf.get().strip()
            nome = self.campo_nome.get().strip()
            nascimento_texto = self.campo_nascimento.get().strip()

            if not cpf or not cpf.isdigit():
                self.campo_cpf.delete(0, tk.END)
                self.campo_cpf.focus()
                raise ValueError("Digite um CPF válido.")
            if not nome:
                self.campo_nome.focus()
                raise ValueError("O nome é obrigatório.")

            try:
                nascimento = datetime.strptime(nascimento_texto, "%d/%m/%Y")
            except ValueError:
                self.campo_nascimento.delete(0, tk.END)
                self.campo_nascimento.focus()
                raise ValueError("Data inválida. Use o formato dd/mm/aaaa.")

            cliente = Cliente(nome, nascimento, cpf)
            self.clientes[cpf] = cliente

            messagebox.showinfo("Sucesso", f"Cliente {cliente.nome} cadastrado!", parent=self)
            self.destroy()
            self.ao_finalizar_cadastro(cliente)

        except ValueError as erro:
            messagebox.showerror("Dados inválidos", str(erro), parent=self)

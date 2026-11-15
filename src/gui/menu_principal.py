import tkinter as tk
from tkinter import messagebox
from src.Gui.tela_cadastro import JanelaCadastro


class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartGas - AutoPosto")
        self.clientes = {}
        self._montar_menu()

    def _montar_menu(self):
        tk.Label(self, text="Bem-vindo ao SmartGas AutoPosto", font=("Arial", 12, "bold")).grid(
            row=0, column=0, padx=20, pady=15
        )

        tk.Button(self, text="1 - Abastecimento", width=25, command=self._opcao_1).grid(
            row=1, column=0, padx=20, pady=5
        )

        tk.Button(self, text="2 - Manutenção", width=25, command=self._opcao_2).grid(
            row=2, column=0, padx=20, pady=5
        )

        tk.Button(self, text="3 - Sair", width=25, command=self.destroy).grid(
            row=3, column=0, padx=20, pady=15
        )

    def _opcao_1(self):
        JanelaCadastro(self, self.clientes, self._depois_do_cadastro)
        messagebox.showinfo("Abastecimento", "Aqui abrirá a tela de cadastro!")

    def _depois_do_cadastro(self, cliente):
        messagebox.showinfo(
            "Próxima etapa",
            f"Cliente {cliente.nome} (CPF: {cliente.cpf}) pronto para escolher o combustível!",
        )

    def _opcao_2(self):
        messagebox.showinfo("Manutenção", "Tela 2")


if __name__ == "__main__":
    JanelaPrincipal().mainloop()

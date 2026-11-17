import tkinter as tk
from tkinter import messagebox
from src.gui.tela_cadastro import TelaCadastro


class TelaMenuPrincipal(tk.Tk):

    def __init__(self, bomba, clientes, combustiveis, transacoes):
        super().__init__()
        self.bomba = bomba
        self.clientes = clientes
        self.combustiveis = combustiveis
        self.transacoes = transacoes
        self.title("SmartGas - AutoPosto")
        self.geometry("600x400")
        self.clientes = {}


        titulo = tk.Label(self, text="SmartGas - AutoPosto", font=("Arial", 14, "bold"))
        titulo.pack(side="top", pady=15)

        painel = tk.Frame(self)

        self.botao_abastecer = tk.Button(
            painel,
            text="1 - Abastecimento",
            width=22,
            command=self._ao_clicar_opcao_1,
        )
        self.botao_abastecer.grid(row=0, column=0, padx=5, pady=8)

        self.botao_manutencao = tk.Button(
            painel,
            text="2 - Manutenção",
            width=22,
            command=self._ao_clicar_opcao_2,
        )
        self.botao_manutencao.grid(row=1, column=0, padx=5, pady=8)

        painel.pack(expand=True)

        # Botão Sair na parte inferior
        self.botao_sair = tk.Button(self, text="3 - Sair", width=15, command=self.destroy)
        self.botao_sair.pack(side="bottom", pady=15)

    def _ao_clicar_opcao_1(self):
        self.withdraw() # esconde o menu enquanto o cadastro estiver aberto
        TelaCadastro(self, self.clientes, self._depois_do_cadastro)

    def _depois_do_cadastro(self, cliente):
        self.deiconify() # volta e segue direto para o próximo passo
        messagebox.showinfo(
            "Próxima etapa",
            f"Cliente {cliente.nome} (CPF: {cliente.cpf}) pronto para abastecer!", parent=self
        )

    def _ao_clicar_opcao_2(self):
        self.withdraw() 
        tela_manutencao(self, self.bomba, self.combustiveis, self.transacoes)


if __name__ == "__main__":
    tela = TelaMenuPrincipal()
    tela.mainloop()

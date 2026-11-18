import tkinter as tk
from src.gui.utils import centralizar
from src.dominio.bomba import BombaCombustivel
from src.dominio.combustivel import Diesel, Gasolina, Etanol
from src.gui.tela_cadastro import TelaCadastro
from src.gui.tela_abastecimento import TelaAbastecimento
from src.gui.pagamento import TelaPagamento  
from src.gui.tela_manutencao import tela_manutencao


class TelaMenuPrincipal(tk.Tk):

    def __init__(self, bomba, clientes, combustiveis, transacoes):
        super().__init__()
        self.bomba = bomba
        self.clientes = clientes
        self.combustiveis = combustiveis
        self.transacoes = transacoes
        self.title("SmartGas - AutoPosto")
        centralizar(self, 600, 450)

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

        self.botao_sair = tk.Button(self, text="3 - Sair", width=15, command=self.destroy)
        self.botao_sair.pack(side="bottom", pady=15)

    def _ao_clicar_opcao_1(self):
        self.withdraw()
        TelaCadastro(self, self.clientes, self._depois_do_cadastro)

    def _depois_do_cadastro(self, cliente):
        TelaAbastecimento(
            self,
            cliente,
            self.bomba,
            self.combustiveis,
            self._depois_do_abastecimento,
        )

    def _depois_do_abastecimento(self, transacao, numero_combustivel, litros):
        TelaPagamento(
            self,
            transacao,
            lambda: self._concluir_pagamento(transacao, numero_combustivel, litros),
        )

    def _concluir_pagamento(self, transacao, numero_combustivel, litros):
        self.bomba.abastecer(numero_combustivel, litros)
        self.transacoes.append(transacao)
        self.deiconify()

    def _ao_clicar_opcao_2(self):
        self.withdraw()
        tela_manutencao(self, self.bomba, self.combustiveis, self.transacoes)


if __name__ == "__main__":
    tela = TelaMenuPrincipal(
        BombaCombustivel(),
        {},
        {1: Diesel(), 2: Gasolina(), 3: Etanol()},
        [],
    )
    tela.mainloop()

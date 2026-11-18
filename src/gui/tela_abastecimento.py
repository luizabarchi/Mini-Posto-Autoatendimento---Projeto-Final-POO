import tkinter as tk
from tkinter import messagebox
from src.dominio.transacao import Transacao

class TelaAbastecimento(tk.Toplevel):
    def __init__(self, master, cliente, bomba, combustiveis: dict, ao_finalizar_abastecimento):
        super().__init__(master)
        self.title("SmartGas - Abastecimento")
        self.geometry("600x600")
        self.janela_principal = master
        self.cliente = cliente
        self.bomba = bomba
        self.combustiveis = combustiveis
        self.ao_finalizar_abastecimento = ao_finalizar_abastecimento

        self.protocol("WM_DELETE_WINDOW", self._voltar)

        titulo = tk.Label(self, text="Escolha do Combustível", font=("Arial", 14, "bold"))
        titulo.pack(side="top", pady=10)

        painel = tk.Frame(self)

        rotulo_cliente = tk.Label(painel, text="Cliente:")
        rotulo_cliente.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        valor_cliente = tk.Label(painel, text=f"{self.cliente.nome} (CPF: {self.cliente.cpf})")
        valor_cliente.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        rotulo_combustivel = tk.Label(painel, text="Combustível:")
        rotulo_combustivel.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.mapa_opcao = {}
        opcoes_texto = []
        for numero, comb in self.combustiveis.items():
            texto = f"{numero} - {comb.nome} (R$ {comb.preco_litro:.2f}/L)"
            self.mapa_opcao[texto] = numero
            opcoes_texto.append(texto)

        self.combustivel_selecionado = tk.StringVar(self, value=opcoes_texto[0])
        self.menu_combustivel = tk.OptionMenu(painel, self.combustivel_selecionado, *opcoes_texto, command=lambda _:self._atualizar_valor_estimado())
        self.menu_combustivel.config(width=28)
        self.menu_combustivel.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        rotulo_litros = tk.Label(painel, text="Litros (Máx.70L)")
        rotulo_litros.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.campo_litros = tk.Entry(painel, width=15)
        self.campo_litros.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.campo_litros.focus()
        self.campo_litros.bind("<KeyRelease>", lambda evento: self._atualizar_valor_estimado())

        rotulo_total = tk.Label(painel, text="Valor Estimado:")
        rotulo_total.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.valor_estimado = tk.Label(painel, text="R$ 0.00", font=("Arial", 10, "bold"))
        self.valor_estimado.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        painel.pack(expand=True)

        self.bind("<Return>", lambda evento: self._ao_clicar_confirmar())

        painel_botoes = tk.Frame(self)
        self.botao_confirmar = tk.Button(painel_botoes, text="Ir para Pagamento", command=self._ao_clicar_confirmar)
        self.botao_confirmar.grid(row=0, column=0, padx=5, pady=5)

        self.botao_voltar = tk.Button(painel_botoes, text="Voltar", command=self._voltar)
        self.botao_voltar.grid(row=0, column=1, padx=5, pady=5)
        painel_botoes.pack(side="bottom", pady=10)

    def _voltar(self):
        self.janela_principal.deiconify()
        self.destroy()

    def _atualizar_valor_estimado(self):
        texto = self.campo_litros.get().strip().replace(",",".")
        try:
            litros = float(texto)
            if litros <= 0:
                self.valor_estimado.config(text="R$ 0.00")
                return
            numero = self.mapa_opcao[self.combustivel_selecionado.get()]
            combustivel = self.combustiveis[numero]
            total = combustivel.calcular_preco_final(litros)
            self.valor_estimado.config(text=f"R$ {total:.2f}")
        except ValueError:
            self.valor_estimado.config(text="R$ 0.00")

    def _ao_clicar_confirmar(self):
        try:
            texto_litros = self.campo_litros.get().strip().replace(",",".")
            try:
                litros = float(texto_litros)
            except ValueError:
                self.campo_litros.delete(0, tk.END)
                self.campo_litros.focus()
                raise ValueError("Digite uma quantidade de litros válida.")

            numero_combustivel = self.mapa_opcao[self.combustivel_selecionado.get()]

            self.bomba.validar_abastecimento(numero_combustivel, litros)

            combustivel = self.combustiveis[numero_combustivel]
            transacao = Transacao(self.cliente.cpf, combustivel, litros)

            self.destroy()
            self.ao_finalizar_abastecimento(transacao, numero_combustivel, litros)

        except ValueError as erro:
            messagebox.showerror("Dados inválidos", str(erro).strip(), parent=self)

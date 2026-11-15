
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import tkinter as tk
from tkinter import messagebox

from src.dominio.combustivel import Gasolina
from src.dominio.pagamento import PagamentoCredito, PagamentoDebito, PagamentoPIX
from src.dominio.transacao import Transacao

class TelaPagamento (tk.Tk):
    def __init__(self, transacao: Transacao):
        super().__init__()
        self.title("SmartGas - Pagamento")
        self.geometry("600x400")
        self.transacao = transacao

        titulo = tk.Label(self, text = "Pagamento e emissão da nota fiscal")
        titulo.pack(side="top", pady=10)


        painel_botoes = tk.Frame(self)
        
        self.botao_pagar = tk.Button(painel_botoes, text="PAGAR", command=self.pagar)
        self.botao_pagar.pack(side="left", padx=5)

        self.botao_nota = tk.Button(painel_botoes, text="Emitir Nota Fiscal", state="disabled", command=self.emitir_nota)
        self.botao_nota.pack(side="left", padx=5)

        painel_botoes.pack(side = "bottom", pady=12)

        painel = tk.Frame(self)

        rotulo_cpf = tk.Label(painel, text = "CPF do Cliente:")
        rotulo_cpf.grid(row=0,column=0,sticky="w",padx=5,pady=5)
        valor_cpf = tk.Label(painel, text = self.transacao.cpf_cliente)
        valor_cpf.grid(row=0,column=1,sticky="e",padx=5,pady=5)

        rotulo_combustivel = tk.Label(painel, text = "Combustível:")
        rotulo_combustivel.grid(row=1,column=0,sticky="w",padx=5,pady=5)
        combustivel=f"{self.transacao.combustivel.nome} ({self.transacao.litros:.2f}L)"
        valor_combustivel = tk.Label(painel, text = combustivel)
        valor_combustivel.grid(row=1, column=1, sticky="e", padx=5, pady=5)

        rotulo_valorTotal = tk.Label(painel, text = "Valor total a pagar:")
        rotulo_valorTotal.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        valor = f"R${self.transacao.valor_total:.2f}"
        valor_total = tk.Label(painel, text = valor)
        valor_total.grid(row=2, column=1, sticky="e", padx=5, pady=5)

        rotulo_metodoPagamento = tk.Label(painel, text="Método de Pagamento:")
        rotulo_metodoPagamento.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.metodo = tk.StringVar(value="")
        self.menuMetodo = tk.OptionMenu(
            painel, self.metodo,
            "Pix", "Cartão de Débito", "Cartão de Crédito",
            command = self.mudar_metodo,
        )

        self.menuMetodo.config(width=18)
        self.menuMetodo.grid(row=3,column=1,sticky="w",padx=5,pady=5)

        self.rotulo_pix = tk.Label(painel, text = "Chave Pix: smartgas@pix.com")

        self.rotulo_cartao = tk.Label(painel,text="Número do Cartão:")
        self.campo_cartao = tk.Entry(painel, width=20)

        self.rotulo_parcelas = tk.Label(painel, text="Parcelas:")
        self.campo_parcelas = tk.Entry(painel, width=20)
        self.campo_parcelas.insert(0,"1")

        rotulo_nota = tk.Label(painel, text="Nota fiscal:")
        rotulo_nota.grid(row=6, column=0, sticky="w", padx=5,pady=5)

        self.texto_nota = tk.Text(painel, width=38, height=12, state="disabled")
        self.texto_nota.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        
        self.rotulo_status = tk.Label(painel, text="", fg="green")
        self.rotulo_status.grid(row=8, column=0, columnspan=2, pady=5)
        
        painel.pack(expand=True)

    def mudar_metodo(self, opcao_escolhida):
        #exibir apenas os campos necessários para a forma de pagamento escolhida
        self.rotulo_pix.grid_remove()
        self.rotulo_cartao.grid_remove()
        self.campo_cartao.grid_remove()
        self.rotulo_parcelas.grid_remove()
        self.campo_parcelas.grid_remove() 

        if opcao_escolhida == "Pix":
            self.rotulo_pix.grid(row=4, column=0, columnspan=2, pady=5)
        elif opcao_escolhida == "Cartão de Crédito":
            self.rotulo_cartao.grid(row=4, column=0, sticky="w", padx=5, pady=5)
            self.campo_cartao.grid(row=4, column=1, sticky="w", padx=5, pady=5)
            self.rotulo_parcelas.grid(row=5, column=0, sticky="w", padx=5, pady=5)
            self.campo_parcelas.grid(row=5, column=1, sticky="w", padx=5, pady=5)            

    def pagar(self):
        escolha = self.metodo.get()
        valor = self.transacao.valor_total

        if escolha == "":
            messagebox.showwarning("Atenção!", "Escolha um método de pagamento antes de pagar")
            return

        if escolha == "Pix":
            pagamento = PagamentoPIX(valor)
        elif escolha == "Cartão de Débito":
            pagamento = PagamentoDebito(valor)
        elif escolha == "Cartão de Crédito":
            numero_cartao = self.campo_cartao.get().strip()
            try:
                parcelas = int(self.campo_parcelas.get())
                if not numero_cartao.isdigit() or parcelas < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Dados do cartão inválidos!")
                return
            
            pagamento = PagamentoCredito(valor, numero_cartao, parcelas)

        if self.transacao.registrar_pagamento(pagamento):
            messagebox.showinfo("Sucesso", "Pagamento aprovado! A bomba está liberada.")
            self.rotulo_status.config(text="Obrigado pela preferência!")
            self.emitir_nota()
            self.botao_pagar.config(state = "disabled")
            self.botao_nota.config(state="normal")

        else:
            messagebox.showerror("Erro", "Pagamento não efetuado")

    def emitir_nota(self):
        notinha = self.transacao.gerar_nota_fiscal()

        self.texto_nota.config(state="normal")
        self.texto_nota.delete("1.0", "end")
        self.texto_nota.insert("1.0", notinha)
        self.texto_nota.config(state="disabled")


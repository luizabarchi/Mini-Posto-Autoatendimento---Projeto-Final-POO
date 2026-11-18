import tkinter as tk
from tkinter import ttk, messagebox
from src.dominio.menu import MenuExibicao

#janela = tk.Tk()
#janela.title("SmartGas")
#janela.geometry("400x300")
#janela.mainloop()

class tela_manutencao(tk.Toplevel):
    def __init__(self, menu_principal, bomba, combustiveis, transacoes): #atributos
        super().__init__(menu_principal)
        self.menu_principal = menu_principal #tela principal para voltar
        self.bomba = bomba
        self.combustiveis = combustiveis
        self.transacoes = transacoes
        self.title("SmartGas Autoposto")
        self.geometry("600x600")
        self.protocol("WM_DELETE_WINDOW", self._voltar) #o x da janela também volta para o menu
        titulo_manutencao = tk.Label(self, text = "SmartGas - Manutenção", font = ("Arial", 18))
        titulo_manutencao.pack(side = "top") 

        self.__tela_senha()
        self.__tela_opcoes()
        self.frame_senha.pack(expand = True) 

    def __tela_senha(self):
        self.frame_senha = tk.Frame(self)

        titulo_senha = tk.Label(self.frame_senha, text = "Digite a senha de acesso", font = ("Arial", 14))
        titulo_senha.pack(pady = 10)

        self.entrada_senha = tk.Entry(self.frame_senha, show = "*", width = 25, font = ("Arial", 12))
        self.entrada_senha.pack(pady = 10)
        self.entrada_senha.focus_set() #recebe dados do teclado
        self.entrada_senha.bind("<Return>", lambda evento: self.verificar_senha()) #enter também confirma

        painel_botoes = tk.Frame(self.frame_senha) 
        botao_entrar = tk.Button(painel_botoes, text = "Entrar", width = 12, command = self.verificar_senha)
        botao_entrar.grid(row=0, column =0 ,padx=5 ,pady=10)

        botao_voltar = tk.Button(painel_botoes, text="Voltar", width=12, command=self._voltar)
        botao_voltar.grid(row=0, column= 1, padx=5, pady=10) # botao voltar caso alguem clice sem querer
        painel_botoes.pack()

    def verificar_senha(self):
        senha_digitada = self.entrada_senha.get() #digitada
        self.entrada_senha.delete(0, tk.END) #limpa o pady 

        if senha_digitada == MenuExibicao.SENHA:
            self.frame_senha.pack_forget() #esconde a tela atuaç
            self.frame_botoes.pack(expand = True) #mostra a tela de opções
        else:
            messagebox.showerror("Acesso Negado", "Senha Incorreta!", parent = self)
            self.entrada_senha.focus_set() 

    def __tela_opcoes(self):
        self.frame_botoes = tk.Frame(self) #caixa dos botões

        #botões
        self.botao_ver_niveis = tk.Button(self.frame_botoes, text = "Consultar Níveis", width = 25, command = self.ver_niveis) #comand mostra a ação que o botão fará
        self.botao_alterar_preco = tk.Button(self.frame_botoes, text = "Alterar Preço", width = 25, command = self.alterar_preco)
        self.botao_repor_reservatorio = tk.Button(self.frame_botoes, text = "Repor Reservatório", width = 25, command = self.repor_reservatorio)
        self.botao_historico_transacao = tk.Button(self.frame_botoes, text = "Histórico de Transações", width = 25, command = self.historico_transacao)
        self.botao_voltar = tk.Button(self.frame_botoes, text="Voltar", width = 25, command=self._voltar)

        for botao in (self.botao_ver_niveis, self.botao_alterar_preco, self.botao_repor_reservatorio, self.botao_historico_transacao, self.botao_voltar):
            botao.pack(pady = 18, fill = "x")  #pady = espaço externo vertifical, x cresce na horizontal
    
    def __abrir_janela(self, titulo):
        janela = tk.Toplevel(self)  #janela secundária
        janela.title(titulo)
        janela.geometry("600x600")
        janela.transient(self) #fica na frente da tela anterior
        titulo_manutencao = tk.Label(janela, text = titulo, font = ("Arial", 18))
        titulo_manutencao.pack(side = "top")
        return janela #para ser usado na construção dos textos 

    def _selecionar_combustivel(self, janela): #__escolher_combustivel
        opcoes = [f"{num} - {c.nome} " for num, c in self.combustiveis.items()]
        seletor = ttk.Combobox(janela, values = opcoes, state = "readonly", width = 25)
        seletor.current(0)
        seletor.pack(pady = 10)
        return seletor

    def _numero_selecionado(self, seletor):
        return list(self.combustiveis.keys())[seletor.current()]

    def _validar_numero(self, texto, janela): #mesma função do terminal
        try:
            return float(texto.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido", parent = janela)
            return None

   
    def ver_niveis(self):
        janela = self.__abrir_janela("Consultar Níveis")

        for numero, combustivel in self.combustiveis.items():
            texto = f"{combustivel.nome}: {self.bomba.nivel(numero):.2f} L" #retirado da parte do terminal
            tk.Label(janela, text = texto, font = ("Arial", 14)).pack(pady = 5)


    def alterar_preco(self):
        janela = self.__abrir_janela("Alterar Preço")
        seletor = self._selecionar_combustivel(janela)

        tk.Label(janela, text = "Digite o novo preço por L em R$:").pack()
        entrada = tk.Entry(janela, width = 15)
        entrada.pack(pady = 5)

        def confirmar():
            novo_preco = self._validar_numero(entrada.get(), janela)

            if novo_preco is None:
                return
            numero = self._numero_selecionado(seletor)
            try:
                self.combustiveis[numero].preco_litro = novo_preco
                messagebox.showinfo("Sucesso", "Preço atualizado!", parent = janela)
                entrada.delete(0, tk.END)
            except ValueError as erro:
                messagebox.showerror("Erro", str(erro), parent=janela)

        tk.Button(janela, text = "Confirmar", width = 15, command = confirmar).pack(pady=10)

    def repor_reservatorio(self):
        janela = self.__abrir_janela("Repor Reservatório")
        seletor = self._selecionar_combustivel(janela)

        tk.Label(janela, text = "Digite a quantidade de litros:").pack()
        entrada = tk.Entry(janela, width = 15)
        entrada.pack(pady = 5)

        def confirmar():
            litros = self._validar_numero(entrada.get(), janela)
            if litros is None:
                return
            numero = self._numero_selecionado(seletor)
            try:
                self.bomba.repor(numero, litros)
                messagebox.showinfo("Sucesso!", "Reservatório reabastecido!", parent=janela)
                entrada.delete(0, tk.END)
            except ValueError as erro:
                messagebox.showerror("Erro", str(erro), parent=janela)

        tk.Button(janela, text = "Confirmar", width = 15, command = confirmar).pack(pady=10)

    def historico_transacao(self):
        janela = self.__abrir_janela("Histórico de Transações")

        if not self.transacoes:
            tk.Label(janela, text = "Nenhuma transação foi registrada ainda.").pack(pady=15)
            return

        caixa = tk.Text(janela, wrap = "none")
        barra = tk.Scrollbar(janela, command = caixa.yview)
        caixa.configure(yscrollcommand = barra.set)
        barra.pack(side = "right", fill = "y")
        caixa.pack(fill = "both", expand = True, padx = 10, pady = 10)

        for t in self.transacoes:
            caixa.insert(
                tk.END,
                f"#{t.id_transacao} - {t.data_hora.strftime('%d/%m/%Y %H:%M')} | "
                f"CPF {t.cpf_cliente} - {t.combustivel.nome} - {t.litros:.2f} L | "
                f"R$ {t.valor_total:.2f} - {t.pagamento.descricao_pagamento}\n"
            )
        caixa.configure(state="disabled")  # só leitura

    def _voltar(self):
        self.menu_principal.deiconify() #mostra o menu
        self.destroy() #fecha a manutenção

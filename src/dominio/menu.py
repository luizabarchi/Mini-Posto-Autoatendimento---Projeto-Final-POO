class MenuExibicao():

    SENHA = "manutencaosmartgas"

    def __init__(self, bomba, clientes, combustiveis):
        self.__bomba = bomba
        self.__clientes = clientes #dicionário com os cpf's dos clientes
        self.__combustiveis = combustiveis 
        self.__transacoes = []

    def __opcoes_iniciais(self):
        print("Bem vindo ao SmartGas AutoPosto\n")
        print("1 - Abastecimento")
        print("2 - Manutenção")
        print("0 - Sair")

    def executar(self):
        while True:
            self.__opcoes_iniciais()
            try:
                opcao = int(input("Escolha uma opção\n"))
            except ValueError:
                print("Opção Inválida\n")
                continue

            if opcao == 0:
                print("Obrigado pela preferência. Volte sempre!")
                break
            elif opcao == 1:
                self.__abastecimento()
            elif opcao == 2:
                self.__manutencao()
            else:
                print("Opção Inválida\n")

    def __validar_numero(self, mensagem):
        try:
            return float(input(mensagem).replace(",","."))
        except ValueError:
            print("Erro! Digite um número válido\n")
            return None

    def __escolher_combustivel(self):
        for numero, combustivel in self.__combustiveis.items():
            print(f"{numero} - {combustivel.nome} (R$ {combustivel.preco_litro:.2f}/L)")

        try:
             opcao = int(input("Escolha o combustível: "))
        except ValueError:
            opcao = None

        if opcao not in self.__combustiveis:
            print("Opção Inválida\n")
            return None
        return opcao
        

    def __abastecimento(self):
        cpf = input("Digite seu CPF(apenas números): ")

        if cpf in self.__clientes:
            print(f"Olá {self.__clientes[cpf].nome}!\n")
        elif not self.__cadastrar_cliente(cpf):
            return

        opcao = self.__escolher_combustivel()
        if opcao is None:
            return


        litros = self.__validar_numero("Digite a quantidade de litros: \n")
        if litros is None:
            return

        try: #Verifica a quantidade de litros digitada
            self.__bomba.validar_abastecimento(opcao, litros)
        except ValueError as erro:
            print(erro)
            return 

        transacao = Transacao(cpf, self.__combustiveis[opcao], litros)
        print(f"Valor Total: R$ {transacao.valor_total: .2f}\n")

        pagamento = self.__escolher_pagamento(transacao.valor_total)
        if pagamento is None or not transacao.registrar_pagamento(pagamento):
            print("Pagamento não realizado. Abastecimento cancelado.\n")
            return

        self.__bomba.abastecer(opcao, litros)
        self.__transacoes.append(transacao)
        print("Pagamento confirmado!\n")
        print(transacao.gerar_nota_fiscal())
        print()

    def __cadastrar_cliente(self, cpf):
            print("CPF não cadastrado. Por favor, insira os dados abaixo: ")
            nome = input("Nome completo: ").strip()
            if not nome:
                print("O nome é obrigatório\n")
                return False

            try:
                nascimento = datetime.strptime(input("Data de Nascimento (dd/mm/aaaa): "), "%d/%m/%Y")

            except ValueError:
                print("Data Inválida\n")
                return False

            self.__clientes[cpf] = Cliente(nome, nascimento, cpf)
            print("Cadastro realizado!\n")
            return True

    def __escolher_pagamento(self, valor):
        print("1 - Pix")
        print("2 - Cartão de Débito")
        print("3 - Cartão de Crédito")

        try:
            forma_pagamento = int(input("Escolha a forma de pagamento: "))
            if forma_pagamento == 1:
                return PagamentoPIX(valor)
            elif forma_pagamento == 2:
                return PagamentoDebito(valor)
            elif forma_pagamento == 3:
                numero = input("Digite o número do cartão: \n").strip()
                parcelas = int(input("Digite o número de parcelas: \n"))
                if not numero.isdigit() or parcelas < 1:
                    raise ValueError
                return PagamentoCredito(valor, numero, parcelas)

        except ValueError:
            print("Forma de pagamento inválida\n")
            return None


    def __manutencao(self):
        if getpass("Digite a senha da manutenção: \n") == self.SENHA:
            self.__menu_manutencao()
            return
        print("Senha incorreta!\n")



    def __menu_manutencao(self):

        while True:
            print("1 - Consultar Níveis dos reservatórios")
            print("2 - Alterar preço")
            print("3 - Repor reservatório")
            print("4 - Histórico de Transações")
            print("0 - Voltar")


            try:
                opcao = int(input("Escolha uma opção: \n"))
            except ValueError:
                print("Opção Inválida!\n")
                continue

            if opcao == 0:
                break
            elif opcao == 1:
                self.__ver_niveis()
            elif opcao == 2:
                self.__alterar_preco()
            elif opcao == 3:
                self.__repor_reservatorio()
            elif opcao == 4:
                self.__ver_historico()
            else:
                print("Opção Inválida\n")

    def __ver_niveis(self):
        print()
        for numero, combustivel in self.__combustiveis.items():
            print(f"{combustivel.nome}: {self.__bomba.nivel(numero): .2f} L\n")

    def __alterar_preco(self):
        opcao = self.__escolher_combustivel()
        if opcao is None:
            return
 
        novo_preco = self.__validar_numero("Digite o novo preço: \n")
        if novo_preco is None:
            return
 
        try:
            self.__combustiveis[opcao].preco_litro = novo_preco
            print("Preço atualizado!\n")
        except ValueError as erro:
            print(erro)
 
    def __repor_reservatorio(self):
        opcao = self.__escolher_combustivel()
        if opcao is None:
            return
 
        litros = self.__validar_numero("Digite a quantidade de litros: ")
        if litros is None:
            return
 
        try:
            self.__bomba.repor(opcao, litros)
            print("Reservatório reabastecido!\n")
        except ValueError as erro:
            print(erro)
 
    def __ver_historico(self):
        if not self.__transacoes:
            print("\nNenhuma transação registrada ainda.")
            return
        print()
        for t in self.__transacoes:
            print(f"#{t.id_transacao} - {t.data_hora.strftime('%d/%m/%Y %H:%M')} | "
                  f"CPF {t.cpf_cliente} - {t.combustivel.nome} - {t.litros:.2f} L | "
                  f"R$ {t.valor_total:.2f} - {t.pagamento.descricao_pagamento}")

#Mini Posto Autoatendimento: SmartGas

from abc import ABC, abstractmethod
from datetime import datetime
from getpass import getpass

class Combustivel(ABC):
    
    def __init__(self, nome: str, preco_litro: float):
        self.__nome = nome
        self.__preco_litro = preco_litro
        
    @property
    def nome(self) -> str:
        return self.__nome
    
    @property
    def preco_litro(self) -> float:
        return self.__preco_litro
    
    @preco_litro.setter
    def preco_litro(self, novo_preco: float) -> None:
        if novo_preco > 0:
            self.__preco_litro = novo_preco
            
    @abstractmethod
    def calcular_preco_final(self, litros: float) -> float:
        # mas poderia colocar como herança também
        pass
     
class Gasolina(Combustivel):
    def __init__(self, nome: str = "Gasolina Comum", preco_litro: float = 6.73):
        super().__init__(nome, preco_litro)
        
    def calcular_preco_final(self, litros: float) -> float:
        # Polimorfismo: Cálculo base do valor da gasolina
        return litros * self.preco_litro
    
class Diesel(Combustivel):
    def __init__(self, nome: str = "Diesel S10", preco_litro: float = 7.59): 
        super().__init__(nome, preco_litro)
        
    def calcular_preco_final(self, litros: float) -> float:
        return litros * self.preco_litro    
    
class Etanol(Combustivel):
    def __init__(self, nome: str = "Etanol", preco_litro: float = 4.36):
        super().__init__(nome, preco_litro)
        
    def calcular_preco_final(self, litros: float) -> float:
        # Polimorfismo: Concede 5% de desconto para abastecimentos a partir de 30L
        total = litros * self.preco_litro
        if litros >= 30.0:
            total *= 0.95
        return total

#LUIZA
class Pagamento(ABC): 
    #Classe abstrata pois ninguém realiza um pagamento sem especificar (pix/débito/crédito)
    def __init__(self, valor:float): 
        self._valor = valor
        self._confirmado = False
        self._data_hora = datetime.now()
        self._descricao_pagamento = self.descricao_pagamento
        #hora e data específicas do pagamento

    @property #encapsulamento
    def valor(self):
        return self._valor

    @property
    def confirmado(self):
        return self._confirmado

    #definir a descricao do pagamento para facilitar a exibição na nota fiscal
    @property
    @abstractmethod
    def descricao_pagamento(self):
        pass

    @abstractmethod #polimorfismo
    def processar_pagamento(self):
        pass

class PagamentoPIX(Pagamento):
    def __init__(self, valor: float, chave_pix: str = "smartgas@pix.com"):
        super().__init__(valor) #chama a classe Pagamento
        self._chave_pix = chave_pix

    @property #encapsulamento
    def chave_pix(self):
        return self._chave_pix

    @property
    def descricao_pagamento(self):
        return "Pix"

    def processar_pagamento(self): #Altera o atributo privado de False para True, liberando a bomba
        self._confirmado = True 
        return True 

class PagamentoDebito(Pagamento):

    @property
    def descricao_pagamento(self):
        return "Cartão de Débito"

    def processar_pagamento(self):
        self._confirmado = True
        return True
    
class PagamentoCredito(Pagamento):
    def __init__(self, valor: float, numero_cartao: str, parcelas: int = 1):
        super().__init__(valor)
        self._parcelas = parcelas 

    @property 
    def parcelas(self):
        return self._parcelas
        
    @property
    def descricao_pagamento(self):
        return "Cartão de Crédito"

    def processar_pagamento(self):
        self._confirmado = True
        return True 

class Transacao:
    _id_contador = 1 #número do recibo
    def __init__(self, cpf_cliente: str, combustivel, litros: float):
        self._id_transacao = Transacao._id_contador #Atribui o número do código atual a esta transação específica
        Transacao._id_contador += 1

        self._cpf_cliente = cpf_cliente
        self._combustivel = combustivel
        self._litros = litros
        self._valor_total = self._combustivel.calcular_preco_final(self._litros) #pega 
        self._pagamento = None  #o pagamento começa como pendente
        self._data_hora = datetime.now()

    @property
    def id_transacao(self):
        return self._id_transacao
    
    @property
    def cpf_cliente(self):
        return self._cpf_cliente 

    @property
    def combustivel(self):
        return self._combustivel

    @property
    def litros(self):
        return self._litros
    
    @property
    def valor_total(self):
        return self._valor_total

    @property
    def pagamento(self):
        return self._pagamento

    @property 
    def data_hora(self):
        return self._data_hora 

    def registrar_pagamento(self, pagamento):
        if pagamento.valor < self._valor_total: 
        #confere se o valor fornecido no pagamento cobre o custo total
            return False

        sucesso = pagamento.processar_pagamento()
        if sucesso:
            self._pagamento = pagamento
        return sucesso

    def gerar_nota_fiscal(self):
        #validação se o pagamento realmente foi realizado
        if not self._pagamento or not self._pagamento.confirmado:
            return "Erro: Pagamento não efetuado/pendente."

        #definir a hora que a notinha foi exibida/impressa
        data_str = self._data_hora.strftime("%d/%m/%Y %H:%M:%S")

        linhas= [
            "AUTOPOSTO SmartGas - NOTA FISCAL",
            "----------------------------------",
            f"Transação ID: {self._id_transacao}",
            f"Data/Hora: {data_str}",
            f"CPF Cliente: {self._cpf_cliente}",
            "----------------------------------",
            f"Combustível: {self._combustivel.nome}",
            f"Litros: {self._litros:.2f}L",
            "----------------------------------",
            f"VALOR TOTAL: R$ {self._valor_total:.2f}",
            f"Forma de pagamento: {self._pagamento.descricao_pagamento}",
        ]

        linhas.append("----------------------------------")

        #retorna o texto formatado
        return "\n".join(linhas)

class BombaCombustivel:
    tipos_combustivel = {1: "diesel", 2: "gasolina", 3: "etanol"}
    def __init__(self):
        self.__reservatorios = {tipo: 5000 for tipo in self.tipos_combustivel.values()}
        
    def __validar_combustivel(self, combustivel):
        if combustivel not in self.tipos_combustivel:
         raise ValueError("Opção Inválida\n")
        return self.tipos_combustivel[combustivel]
    
    def nivel(self, combustivel):#retorna o nível de combustível disponível no reservatório(como o reservatório é privado, o nível mostra o valor para os exteriores)
        tipo = self.__validar_combustivel(combustivel)
        return self.__reservatorios[tipo]

    def validar_abastecimento(self, combustivel, litros):
        tipo = self.__validar_combustivel(combustivel)
        if litros <=0 or litros > 70:#70 limite máximo de abastecimento
            raise ValueError("Quantidade inválida\n")

        if litros > self.__reservatorios[tipo]:#se o reservatório tem litros suficiente
            raise ValueError("Combustível insuficiente no reservatório\n")

        return tipo
        
    def abastecer(self, combustivel, litros):
        tipo = self.validar_abastecimento(combustivel, litros)
          
        self.__reservatorios[tipo] -= litros
        return litros#Conferir a necessidade com a classe de pagamento

    def repor(self, combustivel, litros):
        tipo = self.__validar_combustivel(combustivel)
        espaco = 5000 - self.__reservatorios[tipo]

        if litros <= 0 or litros > espaco:
            raise ValueError(f"Quantidade inválida. Espaço disponível: {espaco:.2f} L\n")

        self.__reservatorios[tipo] += litros
class Cliente:
    def __init__(self, nome: str, data_nascimento: datetime, cpf: str):
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        self.__cpf = cpf
 
    @property
    def nome(self) -> str:
        return self.__nome
 
    @property
    def data_nascimento(self) -> datetime:
        return self.__data_nascimento
 
    @property
    def cpf(self) -> str:
        return self.__cpf
#MENU
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
            print("CPF não cadastrado. Por favor, insiera os dados abaixo: ")
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
 


if __name__ == "__main__":
    combustiveis = {1: Diesel(), 2: Gasolina(), 3: Etanol()} #bomba
    menu = MenuExibicao(BombaCombustivel(), {}, combustiveis)
    menu.executar()

#Mini Posto Autoatendimento: SmartGas

from abc import ABC, abstractmethod
from datetime import datetime

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

#MARIA
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
    
    def abastecer(self, combustivel, litros):
        tipo = self.__validar_combustivel(combustivel)
        
        if litros <=0 or litros > 70:#70 limite máximo de abastecimento
            raise ValueError("Quantidade inválida\n")

        if litros > self.__reservatorios[tipo]:#se o reservatório tem litros suficiente
            raise ValueError("Combustível insuficiente no reservatório\n")
            
        self.__reservatorios[tipo] -= litros
        return self.__reservatorios#Conferir a necessidade com a classe de pagamento

#MENU
class MenuExibicao():
    pass

if __name__ == "__main__":
    menu = MenuExibicao()
    menu.executar()

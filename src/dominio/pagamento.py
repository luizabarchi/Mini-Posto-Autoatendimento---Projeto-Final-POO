from abc import ABC, abstractmethod
from datetime import datetime

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


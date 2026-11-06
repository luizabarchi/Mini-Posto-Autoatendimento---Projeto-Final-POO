from abc import ABC, abstractmethod

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
        """Método abstrato implementado obrigatoriamente pelas subclasses."""
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
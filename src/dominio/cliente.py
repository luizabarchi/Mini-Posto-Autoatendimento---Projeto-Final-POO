
from datetime import datetime

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

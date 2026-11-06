#Mini Posto Autoatendimento

from abc import ABC, abstractmethod
from datetime import date, timedelta

#LEONARDO
class Combustivel (ABC):
    pass

class Gasolina(Combustivel):
    pass

class Diesel(Combustivel):
    pass

class Etanol(Combustivel):
    pass

#LUIZA
class Transacao:
    pass

#MARIA
class BombaCombustivel:
    pass

#MENU
class MenuExibicao:
    pass

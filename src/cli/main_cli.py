from src.dominio.combustivel import Gasolina, Diesel, Etanol
from src.dominio.pagamento import PagamentoPIX, PagamentoDebito, PagamentoCredito
from src.dominio.transacao import Transacao
from src.dominio.bomba import BombaCombustivel
from src.dominio.menu import MenuExibicao

def iniciar_cli():
    combustiveis = {1: Diesel(), 2: Gasolina(), 3: Etanol()} #bomba
    menu = MenuExibicao(BombaCombustivel(), {}, combustiveis)
    menu.executar()

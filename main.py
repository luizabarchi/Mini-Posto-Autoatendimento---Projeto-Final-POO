from src.cli.main_cli import iniciar_cli
from src.gui.menu_principal import TelaMenuPrincipal
from src.dominio.combustivel import Gasolina, Diesel, Etanol
from src.dominio.bomba import BombaCombustivel

if __name__ == "__main__":
    modo = input("Escolha o modo (1 - Terminal | 2 - Interface Gráfica): ").strip()
    if modo == "1":
        iniciar_cli()
    else:
        combustiveis = {1: Diesel(), 2: Gasolina(), 3: Etanol()} 
        bomba = BombaCombustivel() #criação da bomba
        clientes = {} #dicionário para armazenar os clientes
        transacoes = [] #para exibição do histórico
        TelaMenuPrincipal(bomba, clientes, combustiveis, transacoes).mainloop() 

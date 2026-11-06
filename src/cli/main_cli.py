# Importa o seu código (Leonardo)
from src.dominio.combustivel import Gasolina, Diesel, Etanol

# Importa o código da Maria
from src.dominio.bomba import BombaCombustivel

def iniciar_cli():
    # Instanciando as bombas com os seus combustíveis
    bomba_gasolina = BombaCombustivel(1, Gasolina(preco_litro=6.73))
    bomba_diesel = BombaCombustivel(2, Diesel(preco_litro=7.59))
    bomba_etanol = BombaCombustivel(3, Etanol(preco_litro=4.36))

    print("Posto configurado e pronto para operar!")
    # Lógica do menu com while, input e print...

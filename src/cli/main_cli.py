from src.dominio.combustivel import Gasolina, Diesel, Etanol
from src.dominio.pagamento import PagamentoPIX, PagamentoDebito, PagamentoCredito
from src.dominio.transacao import Transacao
from src.dominio.bomba import BombaCombustivel

def iniciar_cli():
    bomba = BombaCombustivel()
    comb = Etanol()
    t = Transacao("123.456.789-00", comb, 40)
    pg = PagamentoPIX(t.valor_total)
    if t.registrar_pagamento(pg):
        bomba.abastecer(3, 40)
        print(t.gerar_nota_fiscal())

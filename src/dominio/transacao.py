from datetime import datetime

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

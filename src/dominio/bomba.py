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

    def validar_abastecimento(self, combustivel, litros):
        tipo = self.__validar_combustivel(combustivel)
        if litros <=0 or litros > 70:#70 limite máximo de abastecimento
            raise ValueError("Quantidade inválida\n")

        if litros > self.__reservatorios[tipo]:#se o reservatório tem litros suficiente
            raise ValueError("Combustível insuficiente no reservatório\n")

        return tipo
        
    def abastecer(self, combustivel, litros):
        tipo = self.validar_abastecimento(combustivel, litros)
          
        self.__reservatorios[tipo] -= litros
        return litros#Conferir a necessidade com a classe de pagamento

    def repor(self, combustivel, litros):
        tipo = self.__validar_combustivel(combustivel)
        espaco = 5000 - self.__reservatorios[tipo]

        if litros <= 0 or litros > espaco:
            raise ValueError(f"Quantidade inválida. Espaço disponível: {espaco:.2f} L\n")

        self.__reservatorios[tipo] += litros

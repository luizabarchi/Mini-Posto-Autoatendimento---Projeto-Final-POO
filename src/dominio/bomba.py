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
    
    def abastecer(self, combustivel, litros):
        tipo = self.__validar_combustivel(combustivel)
        
        if litros <=0 or litros > 70:#70 limite máximo de abastecimento
            raise ValueError("Quantidade inválida\n")

        if litros > self.__reservatorios[tipo]:#se o reservatório tem litros suficiente
            raise ValueError("Combustível insuficiente no reservatório\n")
            
        self.__reservatorios[tipo] -= litros
        return self.__reservatorios#Conferir a necessidade com a classe de pagamento

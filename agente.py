class AgenteTemperatura:
    def __init__(self, potencia):
        self.potencia = potencia

    def perceber ( self , ambiente ):
        print(f"A temperatura é de: {ambiente}°C")
        return ambiente

    def decidir ( self , percepcao ):
        if percepcao >= 30:
            temp = percepcao - self.agir(3)
            return temp
        if percepcao <= 30:
            temp = percepcao + self.agir(3)
            return temp

    def agir ( self , ajuste ):
        return ajuste

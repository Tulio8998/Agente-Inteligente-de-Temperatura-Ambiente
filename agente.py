TEMP_MIN = 30
TEMP_MAX = 30

POTEN_MIN = 30
POTEN_MAX = 200

class AgenteTemperatura:
    def __init__(self, estado, potencia):
        self.potencia = potencia
        self.estado = estado

    def perceber ( self , ambiente ):
        print(f"A temperatura é de: {ambiente}°C")

        if ambiente < 20:
            modo = "Frio"
        elif ambiente <= 25:
            modo = "Ambiente"
        else:
            modo = "Quente"
        print(f"Está no modo: {modo}")

        return ambiente

    def decidir ( self , percepcao ):
        if not self.estado:
            print("Sistema inativo.")
            return percepcao

        if percepcao >= TEMP_MAX:
            temp = percepcao - self.agir(3, POTEN_MIN)
            return temp
        if percepcao <= TEMP_MIN:
            temp = percepcao + self.agir(3, POTEN_MAX)
            return temp

    def agir ( self , ajuste, potencia):
        if (potencia > self.potencia):
            print(f"Houve um estouro de potencia: {potencia}W")
            self.estado = False
            return 0
        else:
            self.potencia-=potencia
            print(f"Potencia atual: {self.potencia}W")
            return ajuste

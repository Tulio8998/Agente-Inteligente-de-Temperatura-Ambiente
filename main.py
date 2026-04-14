from agente import AgenteTemperatura

POTENCIA = 450
agente = AgenteTemperatura(POTENCIA)

cenarios = {
        "Oscilação": [24.9 , 25.1 , 24.8 , 25.2],
        "Calor": [30 , 32 , 35],
        "Resfriamento": [28 , 27 , 26 , 25 , 24]
    }

if __name__ == "__main__":
    for nome, temps in cenarios.items():
        print(f"\n--- {nome} ---")
        for t in temps:
            p = agente.perceber(t)
            acao = agente.decidir(p)
            print(f"Temperatura atual: {acao}")
from agente import AgenteTemperatura

POTENCIA = 450
agente = AgenteTemperatura(True, POTENCIA)

cenarios = {
        "Oscilação": [24.9 , 25.1 , 24.8 , 25.2],
        "Calor": [30 , 32 , 35],
        "Resfriamento": [28 , 27 , 26 , 25 , 24]
    }

if __name__ == "__main__":
    print(("Sistema ativado"))
    for nome, temps in cenarios.items():
        if not agente.estado:
            print("O sistema foi desativado por segurança")
            break
        print(f"\n--- {nome} ---")
        for t in temps:
            p = agente.perceber(t)
            acao = agente.decidir(p)
            print(f"Temperatura atual: {acao}\n")
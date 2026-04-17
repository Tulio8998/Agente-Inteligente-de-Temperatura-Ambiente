from collections import deque

class AgenteTermicoV2:
    def __init__(self):
        self.resetar_estado()

    def resetar_estado(self):
        self.estado_ligado = False
        self.memoria = deque(maxlen=5)
        self.ticks_ligado = 0
        self.temp_quando_ligou = None
        self.tempo_atual = 0

    def perceber_e_agir(self, temp_atual, pessoas=1, contexto="Normal", bloqueio_ar=False, modo="Auto", temp_manual=24.0):
        self.tempo_atual += 1
        self.memoria.append(temp_atual)

        # 1. Definição da Meta (Manual vs Automático/Contexto)
        if modo == "Manual":
            temp_alvo = float(temp_manual)
        else:
            metas = {
                "Normal": 24.0,
                "Dormindo": 23.0,
                "Estudando": 22.0
            }
            temp_alvo = metas.get(contexto, 24.0)

        # 2. Histerese Térmica
        limite_sup = temp_alvo + 1.0
        limite_inf = temp_alvo - 0.5

        # 3. Modelagem Preditiva (apenas para exibição se estiver no modo manual)
        projecao_calor = (pessoas - 1) * 0.2
        temp_prevista = temp_atual + projecao_calor

        # 4. Detecção de Anomalias (Diagnóstico FDD)
        anomalia = False
        msg_alerta = ""
        if self.estado_ligado:
            self.ticks_ligado += 1
            if self.ticks_ligado >= 3 and temp_atual >= self.temp_quando_ligou:
                anomalia = True
                msg_alerta = "⚠️ ANOMALIA: Ar ligado, mas temp não cai. Janela aberta ou falha!"
        else:
            self.ticks_ligado = 0

        # Regra Soberana de Segurança
        if bloqueio_ar:
            self.estado_ligado = False
            return self._gerar_log("Desligado (Segurança)", False, temp_atual, temp_alvo, limite_sup, limite_inf, temp_prevista, "ALERTA: Obstrução de ar! Motor cortado.", True)

        acao_tomada = "Manter"
        msg_acao = msg_alerta if anomalia else "Operação estabilizada."

        # Lógica de Ação
        if not self.estado_ligado:
            if temp_prevista > limite_sup:
                self.estado_ligado = True
                self.temp_quando_ligou = temp_atual
                
                if temp_atual <= limite_sup:
                    acao_tomada = "Ligar (Antecipado)"
                    msg_acao = f"Previsão de {round(temp_prevista, 1)}°C devido a ocupação. Ligando antecipadamente."
                else:
                    acao_tomada = "Ligar (Reativo)"
                    msg_acao = "Limite superior excedido. Iniciando resfriamento."

        else: # Sistema ligado
            if temp_atual <= limite_inf:
                self.estado_ligado = False
                acao_tomada = "Desligar"
                msg_acao = f"Meta inferior ({limite_inf}°C) atingida. Poupando energia."
                self.ticks_ligado = 0

        return self._gerar_log(acao_tomada, self.estado_ligado, temp_atual, temp_alvo, limite_sup, limite_inf, temp_prevista, msg_acao, anomalia)

    def _gerar_log(self, acao, estado, atual, alvo, lim_sup, lim_inf, prevista, msg, anomalia):
        return {
            "tempo": self.tempo_atual, "acao": acao, "estado": estado,
            "temp_atual": atual, "temp_alvo": alvo,
            "limite_sup": round(lim_sup, 2), "limite_inf": round(lim_inf, 2),
            "temp_prevista": round(prevista, 2), "msg": msg,
            "anomalia": anomalia, "memoria": list(self.memoria)
        }
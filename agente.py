import math
import statistics
from collections import deque

class AgenteTermico:
    def __init__(self, temp_desejada=24.0):
        self.resetar_estado(temp_desejada)
        
    def resetar_estado(self, temp_desejada=24.0):
        self.temp_desejada = temp_desejada
        self.estado_ligado = False
        self.memoria = deque(maxlen=5)
        self.taxas_decaimento = []
        self.taxas_elevacao = []
        self.tempo_espera = 0
        self.constante_fallback_k = 2
        self.tempo_atual = 0
        self.inicio_episodio_temp = None
        self.inicio_episodio_tempo = 0
        self.historico_acoes = []

    def calcular_limite_l(self):
        if len(self.memoria) < 2:
            desvio = 0.5
        else:
            desvio = statistics.stdev(self.memoria)
        return self.temp_desejada + (3 * desvio)

    def calcular_custo_j(self, temp_atual):
        custo_energia = 5 if self.estado_ligado else 0
        return abs(temp_atual - self.temp_desejada) + custo_energia

    def atualizar_aprendizado(self, temp_atual):
        if self.inicio_episodio_temp is None: return
        tempo_gasto = self.tempo_atual - self.inicio_episodio_tempo
        if tempo_gasto <= 0: return

        taxa = abs(self.temp_desejada - self.inicio_episodio_temp) / tempo_gasto
        if self.estado_ligado:
            self.taxas_decaimento.append(taxa)
        else:
            self.taxas_elevacao.append(taxa)

    def calcular_tempo_espera(self, temp_atual):
        if self.estado_ligado:
            media = statistics.mean(self.taxas_decaimento) if self.taxas_decaimento else 0
            if media > 0:
                return math.ceil(max(0, temp_atual - self.temp_desejada) / media)
            return math.ceil(self.constante_fallback_k * max(0, temp_atual - self.temp_desejada))
        else:
            media = statistics.mean(self.taxas_elevacao) if self.taxas_elevacao else 0
            if media > 0:
                return math.ceil(max(0, self.temp_desejada - temp_atual) / media)
            return math.ceil(self.constante_fallback_k * max(0, self.temp_desejada - temp_atual))

    def perceber_e_agir(self, temp_atual, pessoas=1, bloqueio_ar=False, energia_critica=False):
        self.tempo_atual += 1
        mensagem = ""

        # Espera
        if self.tempo_espera > 0:
            self.tempo_espera -= 1
            return {
                "tempo": self.tempo_atual, "acao": "Aguardando", "estado": self.estado_ligado,
                "temp_atual": temp_atual, "temp_desejada": self.temp_desejada, "limite_l": None,
                "msg": f"Esperando... ({self.tempo_espera} ticks restantes)"
            }

        self.memoria.append(temp_atual)
        limite_l = self.calcular_limite_l()
        custo_j = self.calcular_custo_j(temp_atual)

        # Regras
        if bloqueio_ar:
            self.estado_ligado = False
            return {
                "tempo": self.tempo_atual, "acao": "Desligado (Segurança)", "estado": False,
                "temp_atual": temp_atual, "temp_desejada": self.temp_desejada, "limite_l": round(limite_l, 2),
                "msg": "ALERTA: Obstrução detectada. Motor desligado."
            }
        
        if energia_critica and self.estado_ligado:
            self.temp_desejada += 2
            mensagem += "Modo econômico ativado. "

        if pessoas >= 10:
            self.temp_desejada -= 1
            mensagem += "Muitas pessoas, meta reduzida. "

        # Decisão Principal
        acao_tomada = "Manter"
        
        if temp_atual > limite_l and not self.estado_ligado:
            self.atualizar_aprendizado(temp_atual)
            self.estado_ligado = True
            acao_tomada = "Ligar"
            self.inicio_episodio_temp = temp_atual
            self.inicio_episodio_tempo = self.tempo_atual

        elif temp_atual <= limite_l and self.estado_ligado:
            self.atualizar_aprendizado(temp_atual)
            self.estado_ligado = False
            acao_tomada = "Desligar"
            self.inicio_episodio_temp = temp_atual
            self.inicio_episodio_tempo = self.tempo_atual

        self.tempo_espera = self.calcular_tempo_espera(temp_atual)

        log = {
            "tempo": self.tempo_atual, "acao": acao_tomada, "estado": self.estado_ligado,
            "temp_atual": temp_atual, "temp_desejada": self.temp_desejada,
            "limite_l": round(limite_l, 2), "custo_j": round(custo_j, 2),
            "prox_espera": self.tempo_espera, "msg": mensagem + "Operação normal."
        }
        self.historico_acoes.append(log)
        return log
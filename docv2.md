# Documentação Oficial: Agente Térmico Inteligente (Versão 2.1)

O **Agente Térmico Inteligente V2.1** representa a evolução de um sistema puramente reativo (V1) para um **Agente Baseado em Conhecimento com Capacidade Preditiva**. Enquanto a primeira versão "olhava para o passado" para reagir ao desconforto, esta nova arquitetura "projeta o futuro" para garantir conforto térmico contínuo e proteger a integridade física do próprio hardware (o motor do ar-condicionado).

---

## 1. Evolução do Paradigma (V1 vs V2.1)

A transição entre as versões resolveu o problema do *short-cycling* (liga/desliga frenético) e adicionou consciência espacial e diagnóstica ao sistema.

| Característica | V1.0 (Agente Reativo Simples) | V2.1 (Agente Preditivo e Contextual) |
| :--- | :--- | :--- |
| **Gatilho de Ação** | Baseado no Desvio Padrão. Reagia apenas *após* o ambiente esquentar. | **Preditivo.** Antecipa o calor humano e liga o motor *antes* da temperatura subir. |
| **Estabilidade** | Alta oscilação na borda da meta (efeito ping-pong). | **Histerese Térmica.** Cria uma banda de tolerância (liga em +1.0°C, desliga em -0.5°C). |
| **Meta Térmica** | Única e estática (ex: 24°C para tudo). | **Dinâmica por Contexto.** Variável conforme a utilidade (Estudo, Sono, Normal). |
| **Diagnóstico** | Cego. Se o ar não gelasse, o motor rodaria ao infinito. | **FDD (Detecção de Falhas).** Detecta anomalias (ex: janela aberta) após 3 ciclos sem queda térmica. |
| **Controle Humano** | Sistema 100% autônomo (caixa preta). | **Modo Override.** O usuário pode forçar o controle manual, suspendendo a IA. |

---

## 2. Arquitetura do Sistema: O Loop Percepção-Ação

O cérebro do sistema (`agente.py`) processa os dados de forma discreta, onde a passagem do tempo é medida em **Ticks** (ciclos de processamento). A cada Tick executado, o agente percorre as quatro fases clássicas da Inteligência Artificial:

### Fase 1: Percepção (Leitura do Ambiente)
O agente recebe um pacote de dados espaciais simulando a leitura de sensores:
* **Termômetro:** A temperatura atual real (ex: 25.5°C).
* **Sensor de Ocupação:** A quantidade de corpos exotérmicos (pessoas).
* **Sensor de Obstrução:** Booleano (True/False) indicando se há bloqueio físico na saída de ar.
* **Interface (IHM):** Parâmetros ditados pelo usuário, como o Modo (Auto/Manual) e o Contexto de Uso.

### Fase 2: Atualização do Estado Interno (Memória)
Antes de raciocinar, a IA atualiza o que sabe sobre o mundo:
* **Fila FIFO:** A temperatura lida entra numa fila restrita às 5 últimas leituras (`deque(maxlen=5)`), descartando a mais antiga.
* **Relógio Interno:** Incrementa o `tempo_atual` (+1 Tick) e o tempo de atividade do compressor (`ticks_ligado`).

### Fase 3: Raciocínio e Regras (O "Cérebro")
Esta é a fase de processamento lógico. O agente submete as percepções a uma hierarquia de regras estrita, da mais crítica para a menos crítica:

**Prioridade 1: Segurança Máxima (Interrupção Absoluta)**
Se o *Sensor de Obstrução* registrar um bloqueio, o agente aborta todo o raciocínio. A ordem imediata é **Desligar** para proteger o motor contra superaquecimento, ignorando o calor da sala ou a vontade do usuário.

**Prioridade 2: Definição da Meta (Resolução de Conflitos)**
A IA define qual é a temperatura alvo naquele momento:
* No **Modo Manual**, atua como um termostato comum (adota o número digitado).
* No **Modo Automático**, consulta sua base de utilidade: *Estudar* exige 22°C (foco), *Dormir* exige 23°C (metabolismo baixo), e uso *Normal* fixa-se em 24°C.

**Prioridade 3: Histerese Térmica (A Banda Morta)**
Para evitar o desgaste mecânico, a IA não usa a Meta como uma linha divisória rígida. Ela calcula dois limites ao redor do alvo:
* **Limite Superior ($L_{sup}$):** Meta + 1.0°C.
* **Limite Inferior ($L_{inf}$):** Meta - 0.5°C.
* *Efeito prático:* A sala pode oscilar livremente dentro dessa banda de 1.5°C sem disparar o motor, economizando energia.

**Prioridade 4: Modelagem Preditiva (Inércia Exotérmica)**
Em vez de esperar o calor, a IA prevê o futuro. Sabendo que cada humano emite calor:
* Subtrai-se a "pessoa base" e multiplica-se os excedentes por 0.2°C.
* Exemplo: Se há 10 pessoas num ambiente a 24.5°C, o agente calcula um salto iminente de +1.8°C. A **Temperatura Prevista** passa a ser 26.3°C. O agente decide resfriar *antes* do calor real chegar ao termômetro.

**Prioridade 5: Diagnóstico FDD (Consciência de Falha)**
A IA vigia a sua própria eficiência perguntando-se: *"Estou com o motor ligado há 3 Ticks ou mais? A temperatura atual é maior ou igual à de quando eu liguei?"* Se sim, ela deduz que o ambiente está vazando (janela aberta) ou falta gás no motor, e dispara o **Alerta de Anomalia** na tela.

### Fase 4: Ação (Decisão Final)
Com todos os cálculos prontos, a árvore de decisão atua sobre o ambiente:
* **Se DESLIGADO:** Compara a *Temp. Prevista* com o *$L_{sup}$*. Se maior, aciona **Ligar**.
* **Se LIGADO:** Compara a *Temp. Atual* com o *$L_{inf}$*. Se atingiu o resfriamento profundo, aciona **Desligar**.
* **Em outros casos:** A ação é **Manter** o estado atual.

---

## 3. Roteiro de Validação (Testes)

Para demonstrar a eficácia do algoritmo aos avaliadores, utilize a aba **"Rodar Testes"** na interface e execute os três cenários exigidos pela atividade original:

---

### 🔹 Cenário 1: Oscilação de Ruído

**Array:** `[24.9, 25.1, 24.8, 25.2]`

O motor permanecerá **DESLIGADO** em todos os *ticks*. Isso prova que a matemática da *histerese* funciona perfeitamente, absorvendo variações de centésimos de grau sem acionar o compressor desnecessariamente.

---

### 🔹 Cenário 2: Calor Extremo

**Array:** `[30, 32, 35]`

O agente acionará a ordem **LIGAR** no primeiro instante e se manterá ativado. Caso o array fosse estendido para *ticks* futuros mantendo temperaturas altas, o sistema dispararia o *alerta de anomalia*, provando a capacidade diagnóstica do agente.

---

### 🔹 Cenário 3: Resfriamento Gradual

**Array:** `[28, 27, 26, 25, 24, 23.5]`

O motor permanecerá **LIGADO** acompanhando a queda térmica. Ele passará pela meta (24.0°C) e só emitirá a ordem **DESLIGAR** no *tick* final (23.5°C), provando que o agente obedeceu ao *L<sub>inf</sub>* para garantir a inércia térmica do ambiente.

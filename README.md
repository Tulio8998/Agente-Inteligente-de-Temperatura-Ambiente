# Agente Inteligente de Temperatura Ambiente
Projetar, implementar e analisar um agente racional capaz de controlar a temperatura de um ambiente, com base nos conceitos de agentes inteligentes apresentados no AIMA.


# Documentação do Projeto:
**Desenvolvido por:** Emerson Caetano , Túlio Vilela e Ithan de Paula 
**Disciplina:** Inteligência Artificial (CSI457) - UFOP

## 1. Percepções
As informações disponíveis ao agente para a tomada de decisão incluem variáveis do ambiente e do estado interno do sistema:

* **Temperatura Atual:** Valor captado pelo sensor no ambiente.
* **Temperatura Desejada (Set-point):** O alvo térmico definido (30.0°C no código).
* **Estado do Sistema:** Indica se o agente está `Ativo` ou `Inativo`.
* **Nível de Potência:** Monitoramento da energia disponível para evitar sobrecarga (estouro de potência).
* **Variáveis Externas (Planejadas):** Presença de usuários (corpos exotérmicos), obstrução de ar e condições climáticas externas.

## 2. Ações
O conjunto de ações que o agente pode executar sobre o ambiente e sobre si mesmo é:

$A = \{ligar, desligar, manter, aumentar\_potencia, diminuir\_potencia\}$

*No código, essas ações refletem-se em aumentar ou diminuir a temperatura ambiente de acordo com o consumo de potência (POTEN_MIN ou POTEN_MAX).*

## 3. Função do Agente
A função do agente $f: P^* \rightarrow A$ mapeia a sequência de percepções para uma ação específica baseada na seguinte lógica:

### Regras Utilizadas:
* **Se** Temperatura Atual $\geq$ 30°C: O agente decide **Resfriar** (diminuir temperatura).
* **Se** Temperatura Atual $<$ 30°C: O agente decide **Aquecer** (aumentar temperatura).
* **Segurança Crítica:** Antes de qualquer ação, o agente verifica se a potência necessária é maior que a potência disponível. Se sim, a ação é abortada e o sistema é desligado (`self.estado = False`).

### Uso de Memória:
O agente utiliza memória para manter seu **estado interno**, acompanhando o consumo acumulado de potência e o seu estado de ativação. Além disso, as anotações preveem o armazenamento de um histórico de picos de temperatura para aprendizado de comportamento.

### Resposta a Cenários:
* **Oscilação:** O agente mantém a temperatura estável próximo ao set-point.
* **Calor/Frio Extremo:** O agente atua de forma contínua até que o equilíbrio seja atingido ou a energia se esgote.
* **Presença Humana:** O agente identifica variações bruscas causadas por "corpos exotérmicos" e ajusta a intensidade da ventilação.

## 4. Critério de Racionalidade
O comportamento do agente é considerado racional pois suas ações são selecionadas para maximizar o sucesso conforme os seguintes critérios:

* **Homeostase Térmica:** O agente busca manter a temperatura sempre em torno de 30°C, conforme definido no projeto.
* **Gestão de Recursos:** O sistema prioriza a economia ao usar `POTEN_MIN` para resfriamento e protege o hardware através do desligamento automático em caso de falta de potência.
* **Integridade do Sistema:** Evita o funcionamento em condições de erro (como obstrução de ar ou estouro de energia), garantindo a longevidade do equipamento controlado.
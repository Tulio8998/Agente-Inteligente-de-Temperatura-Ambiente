# Agente Térmico Inteligente

Este projeto é a implementação de um **Agente Racional** para controle autônomo de temperatura de ambientes. Ele foi desenvolvido como requisito avaliativo para as disciplinas de Inteligência Artificial (CSI457 e CSI701) da **Universidade Federal de Ouro Preto (UFOP)**, sob a orientação do Prof. Talles Medeiros.

## 🎯 Objetivo da Atividade

O objetivo principal desta atividade é projetar, implementar e analisar um agente inteligente capaz de otimizar o conforto térmico de um ambiente enquanto minimiza o consumo de energia e protege a integridade do hardware (compressor do ar-condicionado). 

O projeto aplica na prática os conceitos teóricos do livro *Artificial Intelligence: A Modern Approach (AIMA)*, evoluindo de um modelo puramente reativo para um modelo preditivo baseado em conhecimento.

## 🚀 Evolução da Arquitetura (V1 -> V2.1)

O desenvolvimento foi dividido em duas fases arquiteturais para demonstrar o refinamento do comportamento do agente:

* **Versão 1.0 (Agente Reativo):** Utilizava uma memória FIFO e cálculo de desvio padrão ($\sigma$) para criar limites estatísticos de tolerância. Sofria com limitações reativas, aguardando o ambiente esquentar para tomar decisões.
* **Versão 2.1 (Agente Preditivo e Contextual):** O estado da arte do projeto. Implementa inteligências avançadas de automação predial:
  * **Histerese Térmica:** Criação de bandas mortas assimétricas (+1.0°C para ligar, -0.5°C para desligar) para evitar o desgaste mecânico (*short-cycling*).
  * **Modelagem Preditiva:** O agente calcula a inércia exotérmica baseada na quantidade de pessoas no ambiente, ligando o motor *antes* do calor real atingir o termômetro.
  * **Função de Utilidade:** Adaptação da meta térmica baseada no contexto humano (ex: Dormir exige 23°C, Estudar exige 22°C).
  * **Diagnóstico de Falhas (FDD):** O agente vigia sua própria eficiência. Se o motor operar por 3 ciclos (ticks) consecutivos sem redução de temperatura, a IA aciona um alerta de anomalia (ex: janela aberta ou falha mecânica).

## 🛠️ Tecnologias Utilizadas

O ecossistema foi construído para simular o loop de Percepção-Ação em um ambiente isolado:
* **Python 3:** Lógica de Inteligência Artificial (`agente.py`).
* **Flask:** Servidor Web REST e roteamento (`app.py`).
* **HTML5 / CSS3:** Interface (IHM) simulando um *Dashboard* de automação industrial.
* **Chart.js:** Renderização do gráfico de comportamento térmico em tempo real.

## Como rodar?

1. Certifique-se de ter o **Python** instalado em sua máquina.
2. Baixe e extraia os arquivos do projeto em uma pasta.
3. Abra o terminal (ou prompt de comando) dentro da pasta raiz do projeto.
4. Instale a biblioteca do servidor (Flask) executando o comando:
5. Inicie o sistema executando:
   ```bash
   python app.py
   ```
6. Abra o seu navegador de internet e acesse o endereço local:
   `http://127.0.0.1:5000`



## 📁 Estrutura do Projeto

```text
agente_termico/
├── app.py                 # Servidor Flask e rotas da API
├── agente.py              # Cérebro da IA (Regras, Histerese, Previsão)
├── templates/
│   └── index.html         # Dashboard interativo e ambiente de testes
└── static/
    └── style.css          # Estilização da interface
# Documentação do Agente Térmico Inteligente



Esta documentação descreve o processo de instalação e a arquitetura lógica do Agente Térmico Inteligente, desenvolvido em Python (Flask) e HTML/CSS/JS.

## Parte 1: Como Rodar o Sistema

Para executar este projeto em sua máquina de forma isolada, siga os passos abaixo:

**Pré-requisitos:**
* Ter o **Python** instalado no seu computador.
* Ter um editor de código (como VS Code) ou apenas o Bloco de Notas e Terminal.

**Passo a passo:**
1.  Crie uma pasta no seu computador chamada `agente_termico`.
2.  Dentro desta pasta, crie a seguinte estrutura exata:
    * Um arquivo `app.py`
    * Um arquivo `agente.py`
    * Uma pasta chamada `templates` (dentro dela, crie o arquivo `index.html`)
    * Uma pasta chamada `static` (dentro dela, crie o arquivo `style.css`)
3.  Cole os respectivos códigos (fornecidos na resposta anterior) dentro de cada arquivo.
4.  Abra o Terminal (ou Prompt de Comando) e navegue até a pasta `agente_termico`.
5.  Instale o servidor web Flask digitando o comando:
    `pip install Flask`
6.  Inicie o sistema digitando o comando:
    `python app.py`
7.  O terminal mostrará uma mensagem dizendo que o servidor está rodando. Abra o seu navegador de internet (Chrome, Edge, etc.) e acesse o endereço: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

A interface profissional será carregada e o sistema estará pronto para uso.

---

## Parte 2: Como o Sistema Funciona (Arquitetura do Agente)

O sistema foi modelado usando o conceito clássico de Agentes Inteligentes (Percepção $\rightarrow$ Raciocínio/Estado $\rightarrow$ Ação). O "cérebro" do sistema está no arquivo `agente.py`.

### 1. Percepção (Sensores)
A cada clique no botão ou envio de array nos testes, o agente recebe um pacote de dados do ambiente:
* Temperatura atual
* Temperatura desejada (Meta)
* Quantidade de pessoas (Sensor de presença)
* Obstrução de ar (Sensor físico)
* Estado da energia

### 2. Memória e Aprendizado
* **Fila FIFO (First-In, First-Out):** O agente guarda as últimas 5 temperaturas lidas. Quando a 6ª temperatura entra, a mais antiga é descartada.
* **Episódio Térmico:** Quando o agente liga o ar, ele anota a temperatura inicial e o tempo inicial. Quando a meta é atingida, ele pega a temperatura final e o tempo final, e calcula a velocidade média que aquele ambiente demorou para gelar (Taxa de Decaimento). Ele guarda isso para ficar mais inteligente no futuro.

### 3. Raciocínio e Regras (O Cálculo do Limite)
Antes de agir, o agente toma decisões baseadas em regras de proteção e matemática:
* **Regra de Bloqueio:** Se algo tampar o ar, ele desliga imediatamente por segurança, ignorando todo o resto.
* **Cálculo do Limite (L):** O agente não obedece cegamente a meta. Ele calcula um limite de tolerância usando o Desvio Padrão da sua memória: `Limite = Meta + (3 * Desvio Padrão)`. Se a temperatura atual cruzar essa linha, ele age.

### 4. Ação e Espera (Atuadores)
* Se a temperatura for maior que o limite, ele aciona a ação **Ligar**.
* Para evitar ler os sensores o tempo todo gastando processamento à toa, após ligar, ele calcula um **Tempo de Espera** baseado na média de aprendizado dele (ou uma constante genérica, se for a primeira vez). 
* Durante a espera (os "Ticks"), ele entra em "modo zumbi": continua executando a última ação definida (LIGADO ou DESLIGADO) e avisa o painel que está "Aguardando...".
from flask import Flask, render_template, request, jsonify
from agente import AgenteTermico

app = Flask(__name__)
agente_interativo = AgenteTermico(temp_desejada=24.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perceber', methods=['POST'])
def perceber():
    dados = request.json
    temp_atual = float(dados.get('temp_atual'))
    pessoas = int(dados.get('pessoas', 1))
    bloqueio = dados.get('bloqueio', False)
    energia = dados.get('energia_critica', False)
    
    if 'temp_desejada' in dados:
        agente_interativo.temp_desejada = float(dados['temp_desejada'])

    resposta = agente_interativo.perceber_e_agir(temp_atual, pessoas, bloqueio, energia)
    resposta['memoria'] = list(agente_interativo.memoria)
    return jsonify(resposta)

@app.route('/rodar_cenario', methods=['POST'])
def rodar_cenario():
    dados = request.json
    temperaturas = dados.get('temperaturas', [])
    temp_alvo = float(dados.get('temp_alvo', 24.0))
    
    # Cria um agente isolado para o teste não sujar a simulação manual
    agente_teste = AgenteTermico(temp_desejada=temp_alvo)
    resultados = []
    
    for t in temperaturas:
        res = agente_teste.perceber_e_agir(float(t))
        resultados.append(res)
        
    return jsonify({
        "resultados": resultados,
        "memoria_final": list(agente_teste.memoria)
    })

if __name__ == '__main__':
    app.run(debug=True)
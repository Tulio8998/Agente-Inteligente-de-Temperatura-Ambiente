from flask import Flask, render_template, request, jsonify
from agente import AgenteTermicoV2

app = Flask(__name__)
agente = AgenteTermicoV2()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perceber', methods=['POST'])
def perceber():
    dados = request.json
    temp_atual = float(dados.get('temp_atual'))
    pessoas = int(dados.get('pessoas', 1))
    bloqueio = dados.get('bloqueio', False)
    contexto = dados.get('contexto', 'Normal')
    modo = dados.get('modo', 'Auto')
    temp_manual = float(dados.get('temp_manual', 24.0))

    resposta = agente.perceber_e_agir(temp_atual, pessoas, contexto, bloqueio, modo, temp_manual)
    return jsonify(resposta)

@app.route('/rodar_cenario', methods=['POST'])
def rodar_cenario():
    dados = request.json
    temperaturas = dados.get('temperaturas', [])
    temp_alvo = float(dados.get('temp_alvo', 24.0))
    
    # Isola o teste criando um novo agente
    agente_teste = AgenteTermicoV2()
    resultados = []
    
    for t in temperaturas:
        # Roda o teste forçando o Modo Manual na meta solicitada
        res = agente_teste.perceber_e_agir(float(t), modo="Manual", temp_manual=temp_alvo)
        resultados.append(res)
        
    return jsonify({
        "resultados": resultados,
        "memoria_final": list(agente_teste.memoria)
    })

if __name__ == '__main__':
    app.run(debug=True)
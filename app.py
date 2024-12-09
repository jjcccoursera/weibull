import numpy as np

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/')
def home():
     return render_template('index.html')

@app.route('/invoke', methods=['POST'])
def invoke():
    print("POST request received at /invoke")
    data = request.json
    print("Received JSON:", data) # Debug log
    if data is None:
        print("No JSON payload received")
        return jsonify({"error": "No JSON payload received"}), 400
    # Extract values from the JSON object
    tamanho = data.get('tamanho')
    forma = data.get('forma')
    escala = data.get('escala')
    if None in [tamanho, forma, escala]:
        print("Parâmetros em falta ou não numéricos")
        return jsonify({"erro": "Parâmetros em falta ou não numéricos"}), 400
    if (tamanho<=0 or forma<=0 or escala<=0):
        print("Corrija valores não positivos");
        return jsonify({"erro": "Corrija valores não positivos"}), 400
    print(f"tamanho: {tamanho}, forma: {forma}, escala: {escala}")
    result = generate_weibull_random_numbers(forma, escala,  tamanho)
    return resultados(result)

@app.route('/api', methods=['GET'])
def api():
    tamanho = request.args.get('tamanho', type=int)
    forma = request.args.get('forma', type=float)
    escala = request.args.get('escala', type=float)
    numero = request.args.get('numero', type=int)
    print(f"GET request received with tamanho={tamanho}, forma={forma}, escala={escala}")
    if None in [tamanho, forma, escala]:
        return jsonify({"erro": "Parâmetros em falta ou não numéricos"}), 400
    if (tamanho<=0 or forma<=0 or escala<=0):
        print("Corrija valores não positivos");
        return jsonify({"erro": "Corrija valores não positivos"}), 400
    if (None in [numero] or numero<=0):
        result = generate_weibull_random_numbers(forma, escala, tamanho)
        return resultados(result)
    x = 0
    medias = []
    dps = []
    maxs = []
    mins = []
    while x < numero:
        result = generate_weibull_random_numbers(forma, escala, tamanho)
        medias.append(np.mean(result))
        dps.append(np.std(result))
        maxs.append(np.max(result))
        mins.append(np.min(result))
        x += 1
    json_object = { "0. cabeçalhos,": "médias, desvios padrão, mínimos, máximos",
                    "1. média das,": str(np.mean(medias)) + ", " +str(np.mean(dps)) + ", " + str(np.mean(mins)) + ", " + str(np.mean(maxs)),
                    "2. desvio padrão das,": str(np.std(medias)) + ", " + str(np.std(dps)) + ", " + str(np.std(mins)) + ", " + str(np.std(maxs)),
                    "3. mínimo das,": str(np.min(medias)) + ", " + str(np.min(dps)) + ", " + str(np.min(mins)) + ", " + str(np.min(maxs)),
                    "4. máximo das,": str(np.max(medias)) + ", " + str(np.max(dps)) + ", " + str(np.max(mins)) + ", " + str(np.max(maxs)),
                    "5. médias": medias,
                    "6. desvios padrão": dps,
                    "7. mínimos": mins,
                    "8. máximos": maxs
                  }
    print(json_object)
    return jsonify(json_object)
    

def generate_weibull_random_numbers(shape, scale, size):
    weibull_random_numbers = np.random.weibull(shape, size) * scale
    print(weibull_random_numbers)
    return weibull_random_numbers.tolist()

def resultados(result):
    média = np.mean(result)
    dp = np.std(result)
    json_object = { "média": média,
                   "dp": dp,
                   "lista": result }
    print(json_object)
    return jsonify(json_object)

if __name__ == '__main__': 
    app.run(debug=True)




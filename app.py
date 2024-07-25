from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# Função para obter a taxa de câmbio
def obter_taxa_de_cambio(api_key, moeda_origem, moeda_destino):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{moeda_origem}"
    response = requests.get(url)
    dados = response.json()
    if response.status_code == 200:
        return dados['conversion_rates'][moeda_destino]
    else:
        print(f"Erro: {dados['error-type']}")
        return None


# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        moeda_origem = request.form['moeda_origem'].upper()
        moeda_destino = request.form['moeda_destino'].upper()
        valor = float(request.form['valor'])
        api_key = "9b75d51e36e71baa9087f7b1"
        valor_convertido = converter_moeda(api_key, valor, moeda_origem, moeda_destino)
        if valor_convertido:
            resultado = f"{valor} {moeda_origem} é igual a {valor_convertido:.2f} {moeda_destino}"
        else:
            resultado = "Não foi possível obter a taxa de câmbio."

    return render_template('index.html', resultado=resultado)


# Função para converter moeda
def converter_moeda(api_key, valor, moeda_origem, moeda_destino):
    taxa = obter_taxa_de_cambio(api_key, moeda_origem, moeda_destino)
    if taxa:
        return valor * taxa
    else:
        print("Não foi possível obter a taxa de câmbio.")
        return None


if __name__ == '__main__':
    app.run(debug=True)

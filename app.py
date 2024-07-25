from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


# Função para obter a taxa de câmbio
def obter_taxa_de_cambio(api_key, moeda_origem, moeda_destino):
    try:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{moeda_origem}"
        response = requests.get(url)
        dados = response.json()
        print(f"Resposta da API: {dados}")  # Adiciona um log da resposta da API para depuração

        if response.status_code == 200:
            taxa = dados['conversion_rates'].get(moeda_destino)
            # Adiciona um log da taxa de câmbio para depuração
            print(f"Taxa de câmbio de {moeda_origem} para {moeda_destino}: {taxa}")
            return taxa
        else:
            print(f"Erro da API: {dados['error-type']}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None


# Função para converter moeda
def converter_moeda(api_key, valor, moeda_origem, moeda_destino):
    taxa = obter_taxa_de_cambio(api_key, moeda_origem, moeda_destino)
    if taxa:
        return valor * taxa
    else:
        return None


# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    erro = None
    if request.method == 'POST':
        try:
            moeda_origem = request.form['moeda_origem'].upper()
            moeda_destino = request.form['moeda_destino'].upper()
            valor = float(request.form['valor'])
            api_key = os.getenv('API_KEY')

            if moeda_origem == "" or moeda_destino == "" or valor <= 0:
                erro = "Por favor, insira valores válidos."
            else:
                valor_convertido = converter_moeda(api_key, valor, moeda_origem, moeda_destino)
                if valor_convertido:
                    resultado = f"{valor} {moeda_origem} é igual a {valor_convertido:.2f} {moeda_destino}"
                else:
                    erro = "Não foi possível obter a taxa de câmbio."

        except ValueError:
            erro = "Valor inválido. Por favor, insira um número."

    return render_template('index.html', resultado=resultado, erro=erro)


if __name__ == '__main__':
    app.run(debug=False)

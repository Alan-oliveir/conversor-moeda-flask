import requests

api_key = "9b75d51e36e71baa9087f7b1"
moeda_origem = "USD"
moeda_destino = "BRL"

url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{moeda_origem}"
response = requests.get(url)
dados = response.json()

if response.status_code == 200:
    taxa = dados['conversion_rates'].get(moeda_destino)
    print(f"Taxa de câmbio de {moeda_origem} para {moeda_destino}: {taxa}")
else:
    print(f"Erro da API: {dados['error-type']}")

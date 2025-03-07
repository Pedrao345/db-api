from flask import *
import requests
from googletrans import Translator

API = 'https://dragonball-api.com/api/characters'
app = Flask(__name__)

# Função de tradução
def traduzir(txt):
    try:
        translator = Translator()
        traducao = translator.translate(txt, src='es', dest='pt')  # Corrigido para usar a instância
        return traducao.text  # Corrigido para acessar a tradução corretamente
    except Exception as e:
        print(e)
        return txt

@app.route('/')
def index():
    response = requests.get(API)
    if response.status_code == 200:
        data = response.json()
    return render_template('index.html', items=data['items'])

@app.route('/db', methods=['POST'])
def db():
    if request.method == 'POST':
        perso = request.form['perso']
        PERSO_ENDPOINT = f'https://dragonball-api.com/api/characters/{perso}'
        response = requests.get(PERSO_ENDPOINT)
        if response.status_code == 200:
            data_perso = response.json()
            texto = traduzir(data_perso['description'])  # Corrigido para acessar o campo correto
            response = requests.get(API)
            if response.status_code == 200:
                data = response.json()
            
            return render_template('index.html', perso=data_perso, items=data['items'], texto=texto)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

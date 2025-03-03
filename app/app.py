import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html') 

@app.route('/scrape', methods=['POST'])
def execute_scrape():
    url = request.form.get('url')
    response = requests.get(url)
    supersoup = BeautifulSoup(response.text, 'html.parser')

    text_display = supersoup.get_text()   
    return render_template('index.html', result=text_display) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


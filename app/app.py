import requests
import html
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
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')
    divs_with_class_p = soup.find_all('div', attrs={'class': 'p'})
    extracted_text = [div.get_text() for div in divs_with_class_p]
    result_text = " ".join(extracted_text).replace("\xa0", " ").strip("[]")    
    return render_template('index.html', result=result_text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


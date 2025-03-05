from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import html

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html') 

@app.route('/scrape', methods=['POST'])
def execute_scrape():
    urls_input = request.form.get('urls')
    urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
    
    final_result_text = []
    
    for url in urls:
        try:
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')
            divs_with_class_p = soup.find_all('div', attrs={'class': 'p'})
            extracted_text = [div.get_text() for div in divs_with_class_p]
            result_text = " ".join(extracted_text).replace("\xa0", " ").strip("[]")
            final_result_text.append(result_text)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    combined_results = "\n".join(final_result_text)
    return render_template('index.html', result=combined_results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


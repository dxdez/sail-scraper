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
    tag = request.form.get('tag', '').strip()
    class_attr = request.form.get('class', '').strip()
    search_type = request.form.get('search_type', 'class')    
    urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
    
    final_result_text = []
    
    for url in urls:
        try:
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')

            if tag:
                if search_type == 'class':  # If 'class' is selected
                    if class_attr:
                        elements = soup.find_all(tag, class_=class_attr)
                    else:
                        elements = soup.find_all(tag)
                elif search_type == 'id':  # If 'id' is selected
                    if class_attr:
                        elements = soup.find_all(tag, id=class_attr)  # Use 'id' instead of 'class'
                    else:
                        elements = soup.find_all(tag)
            else:
                elements = soup.find_all("body")
            
            extracted_text = [element.get_text() for element in elements]
            result_text = " ".join(extracted_text).replace("\xa0", " ").strip("[]")
            final_result_text.append(result_text)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    return render_template('index.html', results=final_result_text)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


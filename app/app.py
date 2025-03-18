from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import html

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def hello_world():
    return render_template('index.html') 

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def find_elements(soup, tag, class_attr, search_type):
    if not tag:
        return soup.find_all("body")
    
    if search_type == 'class':
        return soup.find_all(tag, class_=class_attr) if class_attr else soup.find_all(tag)
    elif search_type == 'id':
        return soup.find_all(tag, id=class_attr) if class_attr else soup.find_all(tag)

def extract_text_from_elements(elements):
    for element in elements:
        for anchor in element.find_all('a'):
            anchor.decompose()
    
    return " ".join([element.get_text() for element in elements]).replace("\xa0", " ").strip("[]")

def process_urls(urls, tag, class_attr, search_type):
    final_result_text = []
    
    for url in urls:
        soup = fetch_page_content(url)
        if soup:
            elements = find_elements(soup, tag, class_attr, search_type)
            result_text = extract_text_from_elements(elements)
            final_result_text.append(result_text)
    
    return final_result_text

@app.route('/scrape', methods=['POST'])
def execute_scrape():
    urls_input = request.form.get('urls')
    tag = request.form.get('tag', '').strip()
    class_attr = request.form.get('class', '').strip()
    search_type = request.form.get('search_type', 'class')

    urls = [url.strip() for url in urls_input.split('\n') if url.strip()]

    final_result_text = process_urls(urls, tag, class_attr, search_type)
    session['scraped_content'] = final_result_text

    return render_template('index.html', results=final_result_text)

@app.route('/download')
def download_file():
    if 'scraped_content' not in session:
        return "No content to download. Please scrape first.", 400
    
    final_result_text = session['scraped_content']
    
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.txt') as temp_file:
        temp_file.write("\n\n".join(final_result_text))
        temp_filename = temp_file.name
    
    return send_file(temp_filename, as_attachment=True, download_name="scraped_content.txt")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


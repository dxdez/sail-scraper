from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def hello_world():
    random_num = random.randint(1, 100)
    return render_template('index.html', random_number=random_num) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


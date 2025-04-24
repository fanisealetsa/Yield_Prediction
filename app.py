import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/predict', methods=['POST'])
def predict():
    rainfall = float(request.form.get('rainfall'))
    temperature = float(request.form.get('temperature'))
    pesticide = float(request.form.get('pesticide'))
    return render_template('result.html', prediction=42.0) 


if __name__ == '__main__':
    app.run(debug=True)


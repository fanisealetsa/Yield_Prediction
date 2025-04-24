
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Placeholder prediction logic
    data = request.json
    prediction = {"yield": 100}  # Dummy prediction
    return jsonify(prediction)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get the PORT environment variable
    app.run(host='0.0.0.0', port=port)

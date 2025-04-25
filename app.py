import os
from flask import Flask, render_template, request, jsonify
 
app = Flask(__name__)
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/about')
def about():
    return render_template('about.html')
 
@app.route('/contact')
def contact():
    return render_template('contact.html')
 
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Replace this with actual prediction logic
    prediction = {"yield": 100}  # Dummy prediction
    return jsonify(prediction)
 
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    rainfall = float(request.form['rainfall'])
    temperature = float(request.form['temperature'])
    prediction = model.predict([[rainfall, temperature]])
    return render_template('result.html', prediction=round(prediction[0], 2))

if __name__ == '__main__':
    app.run(debug=True)

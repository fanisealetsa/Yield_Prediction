import os
from flask import Flask, render_template, request, jsonify
from model_rni import predict_yield  # import your prediction function
 
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
    pesticides = data.get("pesticides")
    temperature = data.get("temperature")
    rainfall = data.get("rainfall")
 
    if None in [pesticides, temperature, rainfall]:
        return jsonify({"error": "Missing data. Please provide pesticides, temperature, and rainfall."}), 400
 
    try:
        prediction_result = predict_yield(pesticides, temperature, rainfall)
        response = {
            "predicted_yield": round(prediction_result["predicted_yield"], 2),
            "confidence_interval": {
                "lower": round(prediction_result["confidence_interval"][0], 2),
                "upper": round(prediction_result["confidence_interval"][1], 2)
            },
            "interpretation": prediction_result["interpretation"],
            "improvements": prediction_result["improvements"]
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

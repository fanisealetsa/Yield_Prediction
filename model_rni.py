import joblib
import numpy as np
import requests
import os
 
MODEL_URL = "https://brightlabs.co.bw/crop_yield_model.pkl"
SCALER_URL = "https://brightlabs.co.bw/scaler.pkl"
 
MODEL_PATH = "crop_yield_model.pkl"
SCALER_PATH = "scaler.pkl"
 
def download_file(url, local_path):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(local_path, 'wb') as f:
        f.write(response.content)
 
# Function to load the pre-trained model and scaler
def load_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model...")
        download_file(MODEL_URL, MODEL_PATH)
 
    if not os.path.exists(SCALER_PATH):
        print("Downloading scaler...")
        download_file(SCALER_URL, SCALER_PATH)
 
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler
 
# Function to calculate confidence intervals
def get_confidence_interval(model, X, confidence=0.95):
    preds = np.array([tree.predict(X) for tree in model.estimators_])
    lower = np.percentile(preds, (1 - confidence) / 2 * 100, axis=0)
    upper = np.percentile(preds, (1 + confidence) / 2 * 100, axis=0)
    return lower, upper
 
# Function to interpret the crop yield predictions
def interpret_yield(yield_value):
    if yield_value < 2:
        return "Low yield. Possible issues: insufficient pesticide use, extreme temperatures, or inadequate rainfall."
    elif 2 <= yield_value <= 5:
        return "Moderate yield. Consider fine-tuning pesticide application and irrigation."
    else:
        return "High yield. Conditions are good, but optimization can improve efficiency."
 
# Function to suggest improvements based on input conditions
def suggest_improvements(pesticides, temperature, rainfall):
    suggestions = []
    if pesticides < 50:
        suggestions.append("Increase pesticide usage to prevent potential crop diseases.")
    if temperature < 15 or temperature > 35:
        suggestions.append("Monitor temperature conditions. Extreme temperatures may affect crop growth.")
    if rainfall < 20 or rainfall > 100:
        suggestions.append("Adjust irrigation based on rainfall levels.")
    return "; ".join(suggestions) if suggestions else "Current conditions are optimal."
 
# Function to make predictions on a single data point
def predict_yield(pesticides, temperature, rainfall):
    model, scaler = load_model()
    input_data = np.array([[pesticides, temperature, rainfall]])
    input_scaled = scaler.transform(input_data)
    predicted_yield = model.predict(input_scaled)[0]
    lower, upper = get_confidence_interval(model, input_scaled)
    yield_interpretation = interpret_yield(predicted_yield)
    improvements = suggest_improvements(pesticides, temperature, rainfall)
    return {
        "predicted_yield": predicted_yield,
        "confidence_interval": (lower[0], upper[0]),
        "interpretation": yield_interpretation,
        "improvements": improvements
    }

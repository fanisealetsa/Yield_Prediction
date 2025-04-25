import joblib
import numpy as np
 
def load_model():
    try:
        model = joblib.load("crop_yield_model.pkl")
        scaler = joblib.load("scaler.pkl")
        return model, scaler
    except FileNotFoundError:
        raise FileNotFoundError("Model or scaler file not found! Train and save your model first.")
 
def get_confidence_interval(model, X, confidence=0.95):
    preds = np.array([tree.predict(X) for tree in model.estimators_])
    lower = np.percentile(preds, (1 - confidence) / 2 * 100, axis=0)
    upper = np.percentile(preds, (1 + confidence) / 2 * 100, axis=0)
    return lower, upper
 
def interpret_yield(yield_value):
    if yield_value < 2:
        return "Low yield. Possible issues: insufficient pesticide use, extreme temperatures, or inadequate rainfall."
    elif 2 <= yield_value <= 5:
        return "Moderate yield. Consider fine-tuning pesticide application and irrigation."
    else:
        return "High yield. Conditions are good, but optimization can improve efficiency."
 
def suggest_improvements(pesticides, temperature, rainfall):
    suggestions = []
    if pesticides < 50:
        suggestions.append("Increase pesticide usage to prevent potential crop diseases.")
    if temperature < 15 or temperature > 35:
        suggestions.append("Monitor temperature conditions. Extreme temperatures may affect crop growth.")
    if rainfall < 20 or rainfall > 100:
        suggestions.append("Adjust irrigation based on rainfall levels.")
    return "; ".join(suggestions) if suggestions else "Current conditions are optimal."
 
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

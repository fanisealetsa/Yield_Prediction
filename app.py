@@ -1,13 +1,16 @@
import os
from flask import Flask, render_template

from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__, template_folder='.')
app = Flask(__name__)

@app.route('/')
def index():
def home():
return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

@app.route('/about')
def about():
return render_template('about.html')
@@ -24,5 +27,5 @@ def predict():
return jsonify(prediction)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get the PORT environment variable
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)

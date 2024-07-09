from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from waitress import serve

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing

# Define or import custom_tokenizer
def custom_tokenizer(text):
    # Define your tokenizer logic here
    return text.split()

# If the tokenizer is defined in a different file, import it
# from your_module import custom_tokenizer

# Load the model
model_xss = joblib.load("SSTI.pkl")

@app.route('/note', methods=['POST'])
def check_note():
    note = request.json.get('note')

    # Predict SSTI for the note
    prediction_xss = model_xss.predict([note.lower()])

    response = {
        "is_xss": bool(prediction_xss),
        "message": "No injection detected"
    }

    if response["is_xss"]:
        response["message"] = "SSTI detected in note"
    return jsonify(response)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=4090)

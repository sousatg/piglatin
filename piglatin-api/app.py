from flask import Flask, request
from flask_cors import CORS
from piglatin import translatePhrase

app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return "ok"

@app.route('/translate', methods=["POST"])
def translate_text():
    data = request.json

    phrase = data.get('phrase')

    if phrase == None:
        return (), 400
    
    return translatePhrase(phrase)

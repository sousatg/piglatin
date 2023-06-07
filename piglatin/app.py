from flask import Flask, request
from flask_cors import CORS
from piglatin import translatePhrase
import json

app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return "ok"

@app.route('/translate', methods=["POST"])
def translate_text():
    phrase = request.json.get('phrase')

    if phrase == None:
        return json.dumps({
            "error": "Phrase not provided"
        })
    
    print(phrase)
    
    return translatePhrase(phrase)

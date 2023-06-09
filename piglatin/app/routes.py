from flask import Blueprint, request, jsonify
from app.piglatin import translatePhrase
from app.models import User
from app.schemas import RegistrationSchema
from app.extensions import db
import json

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return "ok"


@bp.route('/register', methods=["POST"])
def user_registration():
    error = RegistrationSchema().validate(request.json)

    if error:
        return jsonify(error), 400
    
    user = RegistrationSchema().load(request.json)

    count = User.query.filter_by(email=user.get_email()).count()

    if count != 0:
        return jsonify({
            "error": "Email address already in registered"
        }), 400

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

    return jsonify({}), 201


@bp.route('/translate', methods=["POST"])
def translate_text():
    phrase = request.json.get('phrase')

    if phrase == None:
        return json.dumps({
            "error": "Phrase not provided"
        })
    
    print(phrase)
    
    return translatePhrase(phrase)

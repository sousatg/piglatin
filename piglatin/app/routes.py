from flask import Blueprint, request, jsonify
from flask_mail import Message
from app.piglatin import translatePhrase
from app.models import User
from app.schemas import RegistrationSchema
from app.extensions import db, mail
import json

bp = Blueprint('main', __name__)


def send_mail_with_token(email, token):
    '''Send email with the confirmation token'''
    msg = Message()
    msg.add_recipient(email)
    msg.subject = 'Account Verification'
    msg.sender = "Pig Latin <admin@piglatin.com>"
    msg.body = 'Token Verification: ' + token
    
    mail.send(msg)


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

    try:
        send_mail_with_token(email=user.get_email(), token=user.get_confirmation_token())
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

    return jsonify({}), 201


@bp.route("/confirm/<token>")
def confirm_user_email(token):
    user = User.query.filter_by(confirmation_token=token).first()

    if user is None:
        return jsonify({
            "error": "Token isn't valid"
        }), 400
    
    user.confirm()

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400
    
    return jsonify(), 204

@bp.route('/translate', methods=["POST"])
def translate_text():
    phrase = request.json.get('phrase')

    if phrase == None:
        return json.dumps({
            "error": "Phrase not provided"
        })
    
    print(phrase)
    
    return translatePhrase(phrase)

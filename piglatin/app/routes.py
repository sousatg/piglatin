from flask import Blueprint, request, jsonify
from flask_mail import Message
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from app.piglatin import translatePhrase
from app.models import User
from app.schemas import RegistrationSchema
from app.schemas import LoginSchema
from app.extensions import db, mail
from app.rate_limit import RateLimit
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


@bp.route("/verification", methods=["POST"])
def confirm_user_email():
    token = request.json.get('token')

    if token == None:
        return jsonify({
            "msg": "Missing token"
        }), 400

    user = User.query.filter_by(confirmation_token=token).first()

    if user is None:
        return jsonify({
            "msg": "Token isn't valid"
        }), 400
    
    user.confirm()

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    
    return jsonify(), 204

@bp.route('/translate', methods=["POST"])
def translate_text():
    is_jwt_verified = verify_jwt_in_request(optional=True)

    identity = None
    if is_jwt_verified == None:
        identity = request.remote_addr
    else:
        identity = get_jwt_identity()

    rateLimit = RateLimit()

    rateLimit.get_limit(identity)

    remainingTries = int(rateLimit.remainingTries)

    if remainingTries + 1 < 1:
        return jsonify({
            "msg": "Too many requests"
        }), 429

    phrase = request.json.get('phrase')

    if phrase == None:
        return json.dumps({
            "error": "Phrase not provided"
        }), 400
    
    return translatePhrase(phrase)

@bp.post('/login')
def login():
    errors = LoginSchema().validate(request.json)

    if errors:
        return jsonify(errors), 400

    data = LoginSchema().load(request.json)

    user = User.query.filter_by(email=data.get("email")).first()

    if user is None or not user.is_valid_password(data.get("password")):
        return jsonify({
            "msg": "Bad username or password"
        }), 401
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "access_token": access_token, 
        "refresh_token": refresh_token}
    ), 200

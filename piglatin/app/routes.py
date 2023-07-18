from flask import Blueprint, request, jsonify, Response
from flask_mail import Message
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from app.piglatin import translatePhrase
from app.models import User
from app.schemas import RegistrationSchema
from app.logger import logger
from app.schemas import LoginSchema
from app.extensions import db, mail
from app.rate_limit import RateLimit
from prometheus_client import Counter
import json

bp = Blueprint('main', __name__)


registration_http_request = Counter("registration_http_request", "User registration request")
registration_http_request_fail = Counter("registration_http_request_fail", "User registration request fail")

confirmation_email_request = Counter("confirmation_email_request", "User email confirmation message")
confirmation_email_request_fail = Counter("confirmation_email_request_fail", "User email confirmation message failed")

verification_http_request = Counter("verification_http_request", "User account email verification")
verification_http_request_fail = Counter("verification_http_request_fail", "User account email verification fail")

translation_http_request = Counter("translation_http_request", "Translation request")
translation_http_request_fail = Counter("translation_http_request_fail", "Translation request fail")
request_rejected_by_rate_limit = Counter("request_rejected_by_rate_limit", "Request has hit the rate limit")

login_http_request = Counter("login_http_request", "Login request")
login_http_request_fail = Counter("login_http_request_fail", "Login request fail")
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
    registration_http_request.inc()

    error = RegistrationSchema().validate(request.json)

    if error:
        registration_http_request_fail.inc()

        logger.info("Missing field when trying to register", extra={"error": error})
        return jsonify(error), 400
    
    user = RegistrationSchema().load(request.json)

    count = User.query.filter_by(email=user.get_email()).count()

    if count != 0:
        logger.info("Email already registered")
        registration_http_request_fail.inc()
        return jsonify({
            "error": "Email address already registered."
        }), 400

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logger.warning("Failed to persist the user in the database")
        registration_http_request_fail.inc()
        return jsonify({
            "error": str(e)
        }), 400

    try:
        confirmation_email_request.inc()
        send_mail_with_token(email=user.get_email(), token=user.get_confirmation_token())
    except Exception as e:
        confirmation_email_request_fail.ince()
        logger.warning("Failed to send email to user", extra={"exception": str(e)})
        return jsonify({
            "error": str(e)
        }), 500

    return jsonify({}), 201


@bp.route("/verification", methods=["POST"])
def confirm_user_email():
    verification_http_request.inc()
    token = request.json.get('token')

    if token == None:
        verification_http_request_fail.inc()
        logger.info("Missing verification token")
        return jsonify({
            "msg": "Missing token"
        }), 400

    user = User.query.filter_by(confirmation_token=token).first()

    if user is None:
        verification_http_request_fail.inc()
        logger.info("Could not find a user with the assigned validation token", extra={"token": token})
        return jsonify({
            "msg": "Token isn't valid"
        }), 400
    
    user.confirm()

    try:
        db.session.commit()
    except Exception as e:
        verification_http_request_fail.inc()
        logger.warning("Failed to save the user verification change", {"user_id": user.id})
        return jsonify({
            "error": str(e)
        }), 500
    
    return jsonify(), 204

@bp.route('/translate', methods=["POST"])
def translate_text():
    translation_http_request.inc()

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
        logger.info("User has passed the limite of request", extra={"identity": identity})
        translation_http_request_fail.inc()
        request_rejected_by_rate_limit.inc()
        return jsonify({
            "msg": "Too many requests"
        }), 429

    phrase = request.json.get('phrase')

    if phrase == None:
        logger.info("Request missing the phrase in request body")
        translation_http_request_fail.inc()
        return json.dumps({
            "error": "Phrase not provided"
        }), 400
    
    resp = Response(translatePhrase(phrase))
    resp.headers['X-Rate-Limit-Limit'] = 5
    resp.headers['X-Rate-Limit-Remaining'] = remainingTries
    resp.headers['X-Rate-Limit-Reset'] = 60

    return resp

@bp.post('/login')
def login():
    login_http_request.inc()
    errors = LoginSchema().validate(request.json)

    if errors:
        login_http_request_fail.inc()
        logger.info("Login request bad formated", extra={"errors": errors})
        return jsonify(errors), 400

    data = LoginSchema().load(request.json)

    user = User.query.filter_by(email=data.get("email")).first()

    if user is None or not user.is_valid_password(data.get("password")):
        login_http_request_fail.inc()
        return jsonify({
            "msg": "Bad username or password"
        }), 401
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "access_token": access_token, 
        "refresh_token": refresh_token}
    ), 200

from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route('/ping')
def ping_user():
    return "User route works!"

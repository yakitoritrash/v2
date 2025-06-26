from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')

    if not username or not password or not email or not phone_number:
        return jsonify({'message': 'Username and password are required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 409

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_pw, role='user', phone_number=phone_number)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token}), 200


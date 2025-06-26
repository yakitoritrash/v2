from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from redis import Redis
from celery import Celery
import os
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
mail = Mail()

load_dotenv()
def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'supersecretkey123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['broker_url'] = 'redis://localhost:6379/0'
    app.config['result_backend'] = 'redis://localhost:6379/0'
    app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER')
    app.config['MAIL_PORT'] = (os.getenv('SMTP_PORT'))
    app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    mail.init_app(app)

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    CORS(app)


    from app.views.auth import auth_bp
    from app.views.admin import admin_bp
    from app.views.parking import parking_bp
    from app.views.user import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(parking_bp)

    return app

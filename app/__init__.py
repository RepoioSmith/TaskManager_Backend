from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.config import Config

# Inicializamos las extensiones globalmente
mongo = PyMongo()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar plugins con la configuración de la app
    mongo.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)  # <-- Inicializamos Bcrypt
    CORS(app)

    # Importar y registrar los Blueprints (Rutas)
    from app.routes.auth_routes import auth_bp
    from app.routes.task_routes import task_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(task_bp, url_prefix='/api/tasks')

    return app
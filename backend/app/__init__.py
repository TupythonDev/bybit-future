from flask import Flask
from flask_cors import CORS
from app.routes import routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes)
    CORS(app)
    return app

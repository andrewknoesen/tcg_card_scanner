# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for React frontend
    
    from app.api.routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    return app

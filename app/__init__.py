from flask import Flask
from .routes import main  # Import the main Blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)  # Register the Blueprint
    return app

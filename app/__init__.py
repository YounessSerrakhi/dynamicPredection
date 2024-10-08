from flask import Flask
from flask_restful import Api
from .routes.model_training import ModelTrainingResource

def create_app():
    app = Flask(__name__)
    api = Api(app)
    
    api.add_resource(ModelTrainingResource, '/train')
    
    return app
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from flask import request
from ..utils.model_trainer import train_and_evaluate_models
import pandas as pd
import io

class ModelTrainingResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        # Expecting the file to be sent in 'files' and to use 'multipart/form-data'
        self.reqparse.add_argument('dataset', type=FileStorage, location='files', required=True, help='CSV file with the dataset')
        # Expecting the 'target' column to be passed as form-data
        self.reqparse.add_argument('target', type=str, required=True, help='Name of the target column')
        super(ModelTrainingResource, self).__init__()

    def post(self):
        # Parse the request arguments (file and target column)
        args = self.reqparse.parse_args()
        dataset_file = args['dataset']
        target_column = args['target']

        # Ensure the dataset file is not empty or null
        if dataset_file is None:
            return {"message": "No dataset file provided"}, 400

        # Ensure the file is in CSV format and try reading it
        try:
            # Read the CSV file from the uploaded dataset file
            df = pd.read_csv(io.StringIO(dataset_file.read().decode('utf-8')))
        except Exception as e:
            return {"message": f"Error processing CSV file: {str(e)}"}, 400

        # Ensure the target column exists in the CSV file
        if target_column not in df.columns:
            return {"message": f"Target column '{target_column}' not found in the dataset"}, 400

        # Train and evaluate models
        results = train_and_evaluate_models(df, target_column)

        # Return the model evaluation results
        return results, 200

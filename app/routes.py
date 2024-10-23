from flask import Blueprint, request, jsonify, render_template
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import joblib

main = Blueprint('main', __name__)  # Define a new Blueprint

# Specify the directory to save models
MODEL_DIR = 'saved_models'

# Create the directory if it doesn't exist
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# Function to transform non-numerical columns into numerical
def transform_to_numerical(df):
    label_encoders = {}
    for column in df.columns:
        if df[column].dtype == 'object':
            label_encoders[column] = LabelEncoder()
            df[column] = label_encoders[column].fit_transform(df[column])
    return df, label_encoders

# Load dataset and train models
def load_and_train_model(dataset, target_column):
    df = pd.read_csv(dataset)  # Load the dataset from the given path
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset")
    df = df.dropna()
    df_transformed, encoders = transform_to_numerical(df)

    X = df_transformed.drop(columns=[target_column])
    y = df_transformed[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    accuracies = []

    # Train Logistic Regression model
    model_lr = LogisticRegression()
    model_lr.fit(X_train, y_train)
    accuracy1 = accuracy_score(y_test, model_lr.predict(X_test))
    accuracies.append(('Logistic Regression', accuracy1))

    # Train Random Forest model
    model_rf = RandomForestClassifier(random_state=0)
    model_rf.fit(X_train, y_train)
    accuracy2 = accuracy_score(y_test, model_rf.predict(X_test))
    accuracies.append(('Random Forest', accuracy2))

    # Train Decision Tree model
    model_tree = DecisionTreeClassifier(random_state=42)
    model_tree.fit(X_train, y_train)
    accuracy3 = accuracy_score(y_test, model_tree.predict(X_test))
    accuracies.append(('Decision Tree', accuracy3))

    return jsonify({'models': [{'model_name': name, 'accuracy': acc} for name, acc in accuracies]})

# Route to render index.html
@main.route('/')
def home():
    return render_template('index.html')

# Flask route to receive dataset as file and target column as parameter
@main.route('/train', methods=['POST'])
def train_models():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']  # Get the uploaded file
    target_column = request.form.get('target_column')  # Get the target column from form-data

    if not file or not target_column:
        return jsonify({'error': 'Please provide both file and target_column'}), 400

    try:
        # Save the uploaded file temporarily
        dataset_name = 'uploaded_dataset.csv'
        file.save(dataset_name)

        result = load_and_train_model(dataset_name, target_column)
        return result
    except Exception as e:
        return jsonify({'error': str(e)}), 500

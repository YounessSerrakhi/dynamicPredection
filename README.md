# Dynamic Prediction Project

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo-url.git
    ```

2. Navigate to the project directory:
    ```bash
    cd dynamicPredection
    ```

3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the Flask application:
    ```bash
    python run.py
    ```

2. The application will be running on `http://127.0.0.1:5000/`.

## API Usage

- **Train a model**: Send a POST request to `/train` endpoint using Postman or curl with the following form-data:
  - **dataset**: (File) The CSV file containing your data.
  - **target**: (Text) The name of the target column in your dataset.

```bash
curl -X POST http://127.0.0.1:5000/train -F "dataset=@your_dataset.csv" -F "target=your_target_column"
```

## Notes

- Ensure that Python 3.x and pip are installed on your system before starting.
- Make sure you activate the virtual environment every time before running the application.



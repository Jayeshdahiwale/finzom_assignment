# Volatility Calculator

Welcome to the Volatility Calculator, a Django project that calculates daily and annualized volatility of financial data from CSV or Excel files.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Using the UI](#using-the-ui)
  - [Sending API Requests](#sending-api-requests)


## Installation

1. Clone the repository:
    ```bash
    open terminal.
    Run : git clone https://github.com/Jayeshdahiwale/finzom_assignment.git

    and run : cd finzom_assignment
2. Set up a virtual environment:
    python -m venv venv

    source venv/bin/activate  # For Linux/Mac
     #### or
    venv\Scripts\activate  # For Windows

3. Install dependencies:
    pip install -r requirements.txt

4. Run migrations:
    python manage.py migrate

5. Start the development server:
    python manage.py runserver

Visit http://localhost:8000/ in your browser to see the application.

## Usage

### Using the UI

1. Open your browser and go to http://localhost:8000/.
2. You will see a form for uploading CSV or Excel files.
3. Choose a file and click the "Submit" button.
4. The calculated daily and annualized volatility will be displayed on the page.

### Sending API Requests

You can use Postman to send API requests to calculate volatility programmatically.

1. Open Postman.

2. Set the request type to `POST` and enter the following URL:

    http://localhost:8000/api/calculate_volatility/


3. In the request body, select `form-data` and add a key-value pair:
- Key: `file`
- Value: Choose a CSV or Excel file.

4. Click the "Send" button.

5. The API will respond with JSON containing daily and annualized volatility.


Thank You
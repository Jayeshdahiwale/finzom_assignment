import pandas as pd
import numpy as np
from django.shortcuts import render
from .forms import UploadFileForm
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

def dataframe_reader(file):
    """
    Reads a CSV or Excel file and returns a pandas DataFrame.

    Parameters:
    - file (str or InMemoryUploadedFile): The file path or the uploaded file.

    Returns:
    pandas.DataFrame: The DataFrame containing the data from the file.
    """
    extension = file.name.split('.')[-1]
    if extension == 'csv':
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    return df

def calculate_volatility(df, api_request=False):
    """
    Calculates daily and annualized volatility of a DataFrame.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing financial data with a 'Close' column.
    - api_request (bool): If True, returns the result as a dictionary. If False, returns a formatted string.

    Returns:
    - If api_request is True:
      dict: Dictionary containing 'daily_volatility' and 'annualized_volatility' keys.
    - If api_request is False:
      str: Formatted string with daily and annualized volatility values.
    """
    try:
        df['prev_close'] = df['Close '].shift(1).fillna(df['Close '])
        df['daily_returns'] = (df['Close ']/df['prev_close']) - 1
        daily_volatility = df['daily_returns'].std()
        annualized_volatility = daily_volatility * np.sqrt(df.shape[0])

        if api_request:
            return {'daily_volatility': daily_volatility, 'annualized_volatility': annualized_volatility}

        result_str = f"Daily Volatility: {daily_volatility:.4f}, Annualized Volatility: {annualized_volatility:.4f}"
        return result_str

    except Exception as e:
        return str(e)

@csrf_exempt
def calculate_volatility_api(request):
    """
    View function for calculating volatility from an uploaded CSV or Excel file.

    Parameters:
    - request (HttpRequest): The Django HttpRequest object.

    Returns:
    HttpResponse: JSON response containing the calculated volatility or an error message.
    """
    file = request.FILES.get('file')
    extension = file.name.split('.')[-1]

    try:
        if not file:
            raise ValueError("No file was provided.")

        if not (extension == 'csv' or extension == 'xlsx'):
            error_message = "Only CSV or Excel (xlsx) files are allowed."
            return HttpResponse(json.dumps({'error': error_message}), content_type="application/json", status=400)

        df = dataframe_reader(file)
        result = calculate_volatility(df, api_request=True)

        if isinstance(result, dict):
            return HttpResponse(json.dumps(result), content_type="application/json", status=200)
        else:
            return HttpResponse(json.dumps({'error': result}), content_type="application/json", status=400)

    except Exception as e:
        error_message = str(e)
        return HttpResponse(json.dumps({'error': error_message}), content_type="application/json", status=400)

def index(request):
    """
    View function for rendering the index page with an upload form.

    Parameters:
    - request (HttpRequest): The Django HttpRequest object.

    Returns:
    HttpResponse: Rendered HTML response with the upload form and volatility result.
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = dataframe_reader(file)
            volatility_result = calculate_volatility(df)
            return render(request, 'index.html', {'form': form, 'volatility_result': volatility_result})
    else:
        form = UploadFileForm()
    
    return render(request, 'index.html', {'form': form})

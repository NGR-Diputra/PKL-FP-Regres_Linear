# """
# ==================================================================================================
# ERROR : 
# 1. Benerin function preprocessing data
# 2. Ubah jadi app.py sama main.py
# 3. app.py cuma apply flask sama functions dari main.py
# 4. main.py cuma untuk keseluruhan function regresi linear
# ==================================================================================================
# """

# from flask import Flask, render_template, request
# from main import preprocess_data, filtering_data, linear_regression
# import os
# import pandas as pd

# app = Flask(__name__)

# # Load dataset
# dataset_dir = "C:\\Users\\Diputra_W\\Documents\\Campus\\Study\\Mata Kuliah\\Semester 7\\PKL\\FInal Project\\src\\penerapan-pengelolaan-hama-terpadu-tanaman-pangan.xlsx"
# df = pd.ExcelFile(dataset_dir)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Ambil input dari pengguna
#         crop_type = request.form['crop_type']
        
#         # Load data berdasarkan jenis tanaman
#         data = df.parse(crop_type)
        
#         # Preprocess data
#         data = preprocess_data(data)
#         filtered_data = filter_data(data)

#         # Perform linear regression
#         prediction = linear_regression(filtered_data)

#         # Render template with prediction
#         return render_template('index.html', prediction=prediction, crop_type=crop_type)
#     except Exception as e:
#         # Render template with error
#         return render_template('index.html', error=str(e))

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request
from main import preprocess_data, filter_data, linear_regression

app = Flask(__name__)

# Path to dataset
dataset_path = (
    "C:\\Users\\Diputra_W\\Documents\\Campus\\Study\\Mata Kuliah\\Semester 7\\PKL\\FInal Project\\src\\penerapan-pengelolaan-hama-terpadu-tanaman-pangan.xlsx"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get crop type from user input
        crop_type = request.form['crop_type']

        # Preprocess data for the selected crop type
        preprocessed_data = preprocess_data(dataset_path, crop_type)

        # Filter the relevant columns
        filtered_data = filter_data(preprocessed_data)

        # Perform linear regression
        prediction = linear_regression(filtered_data)

        # Render results on the page
        return render_template(
            'index.html', prediction=prediction, crop_type=crop_type
        )
    except Exception as e:
        # Handle errors and display them on the page
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)

import pandas as pd
import numpy as np

def preprocess_data(dataset_path, sheet_name):
    data = pd.read_excel(dataset_path, sheet_name=sheet_name, header=[0, 1])
    data.columns = [" ".join(col).strip() for col in data.columns.values]
    data.columns = data.columns.str.strip().str.replace(" ", "_").str.replace("/", "_").str.replace("-", "_")
    
    data.rename(columns={
        "TAHUN_Unnamed:_0_level_1": "TAHUN",
        "NO_PROV_Unnamed:_1_level_1": "KODE_PROVINSI",
        "PROV_Unnamed:_2_level_1": "PROVINSI",
    }, inplace=True)

    data.fillna(0, inplace=True)
    rows_to_drop = [34, 69, 104, 139, 174]
    data = data.drop(index=rows_to_drop)
    
    columns_to_keep = ['TAHUN'] + ['KODE_PROVINSI'] + [col for col in data.columns if '_T' in col]
    data_T = data[columns_to_keep]
    data_T['TAHUN'] = pd.to_numeric(data_T['TAHUN'], errors='coerce')
    data_T.fillna(0, inplace=True)
    
    return data_T.astype(float)

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        for j in range(i+1, n):
            ratio = A[j, i] / A[i, i]
            A[j, i:] -= ratio * A[i, i:]
            b[j] -= ratio * b[i]
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i, i]
    return x

def predict_next_year(dataset_path, sheet_name):
    data_T = preprocess_data(dataset_path, sheet_name)
    
    # Ambil variabel X dan Y
    Y_T = data_T["TOTAL_OPUT_T"]
    X_T = ['TAHUN'] + [col for col in data_T.columns if '_T' in col and col != "TOTAL_OPUT_T"]
    X_T = data_T[X_T]
    
    X_T = np.hstack((np.ones((X_T.shape[0], 1)), X_T.values))  # Tambahkan intercept
    Y_T = Y_T.values.reshape(-1, 1)
    
    # Hitung koefisien regresi menggunakan eliminasi Gauss
    A = X_T.T @ X_T
    b = X_T.T @ Y_T
    coefficient = gaussian_elimination(A, b.flatten())
    
    # Prediksi 1 tahun ke depan
    last_year = int(data_T['TAHUN'].max())
    future_year = last_year + 1
    independent_columns = [col for col in data_T.columns if '_T' in col and col != "TOTAL_OPUT_T"]
    historical_means = data_T[independent_columns].mean().values
    
    future_data = [1, future_year] + list(historical_means)  # Tambahkan intercept
    prediction = np.dot(future_data, coefficient)
    
    return future_year, prediction

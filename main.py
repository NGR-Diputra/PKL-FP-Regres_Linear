# import pandas as pd
# import numpy as np

# # Function Preprocessing Dataset Excel/CSV
# def preprocess_data(dataset):
#     # Perbaikan header data
#     data = pd.read_excel(dataset, header=[0, 1])
#     data.columns = [" ".join(col).strip() for col in data.columns.values]

#     # Cleaning kolom data
#     data.columns = data.columns.str.strip()
#     data.columns = data.columns.str.replace(" ", "_")
#     data.columns = data.columns.str.replace("/", "_")
#     data.columns = data.columns.str.replace("-", "_")

#     # Ganti nama kolom (tujuan untuk mempermudah proses kedepannya)
#     data.rename(columns={
#         "TAHUN_Unnamed:_0_level_1": "TAHUN",
#         "NO_PROV_Unnamed:_1_level_1": "KODE_PROVINSI",
#         "PROV_Unnamed:_2_level_1": "PROVINSI",
#     }, inplace=True)

#     # Penanganan missing values
#     data.fillna(0, inplace=True)

#     # Menghilangkan baris yang tidak diperlukan
#     # rows_to_drop = [34, 69, 104, 139, 174]
#     # data = data.drop(index=rows_to_drop)

#     # Filtering kolom yang akan digunakan (kode provinsi, tahun, dan kolom _T)
#     columns_to_keep = ['KODE_PROVINSI'] + [col for col in data.columns if '_T' in col]
#     return data[columns_to_keep] 

# # Function Filtering Data Untuk Memilih Data Yang Akan Digunakan Dalam Model Regresi
# def filtering_data(preprocessed_data):
#     # Jumlahkan data dalam 5 tahun
#     return preprocessed_data.groupby('KODE_PROVINSI').sum().reset_index()

# # Function Untuk Melakukan Regresi Linear
# def linear_regression(filtered_data):
#     # Variabel dependen
#     Y_T = filtered_data["TOTAL_OPUT_T"]
#     X_T = [col for col in filtered_data.columns if '_T' in col and col != "TOTAL_OPUT_T"]
#     X_T = filtered_data[X_T]

#     X_T = X_T.values
#     Y_T = Y_T.values.reshape(-1, 1)

#     # Menambahkan variabel tambahan sebagai intercept/konstanta sesuai pada rumus regresi linear
#     X_T_intercept = np.hstack((np.ones((X_T.shape[0], 1)), X_T))

#     # Cari nllai transpose dari matriks X
#     X_transpose = X_T_intercept.T

#     # Kalikan Matriks Transpose X dengan Matriks X itu sendiri
#     multiplication_X = X_transpose @ X_T_intercept

#     # Cari invers dari perkalian matriks sebelumnya
#     inversed_multiplication_X = np.linalg.inv(multiplication_X)

#     # Kalikan matriks transpose X dengan matriks output Y_T
#     multiplication_Y = X_transpose @ Y_T

#     # Kalikan semua nilai tadi untuk memperoleh nilai koefisien untuk masing - masing variabel independen serta konstanta
#     coefficient = inversed_multiplication_X @ multiplication_Y

#     # Prediksi untuk tahun mendatang
#     prediction = X_T_intercept[-1] @ coefficient  # Gunakan data terakhir untuk proyeksi
#     return round(prediction[0], 2)

import pandas as pd
import numpy as np

# Function to preprocess the data from the selected sheet
def preprocess_data(dataset, sheet_name):
    # Load the data for the selected plant type
    data = pd.read_excel(dataset, sheet_name=sheet_name, header=[0, 1])
    data.columns = [" ".join(col).strip() for col in data.columns.values]
    data.columns = (
        data.columns.str.strip()
        .str.replace(" ", "_")
        .str.replace("/", "_")
        .str.replace("-", "_")
    )
    data.rename(
        columns={
            "TAHUN_Unnamed:_0_level_1": "TAHUN",
            "NO_PROV_Unnamed:_1_level_1": "KODE_PROVINSI",
            "PROV_Unnamed:_2_level_1": "PROVINSI",
        },
        inplace=True,
    )
    data.fillna(0, inplace=True)
    return data

# Function to filter needed columns for analysis
def filter_data(preprocessed_data):
    # Keep only 'KODE_PROVINSI' and columns ending with '_T'
    columns_to_keep = ['KODE_PROVINSI'] + [
        col for col in preprocessed_data.columns if '_T' in col
    ]
    filtered_data = preprocessed_data[columns_to_keep]
    return filtered_data.groupby('KODE_PROVINSI').sum().reset_index()

# Function to perform linear regression
def linear_regression(filtered_data):
    # Define dependent and independent variables
    Y_T = filtered_data["TOTAL_OPUT_T"]
    X_T = [
        col
        for col in filtered_data.columns
        if '_T' in col and col != "TOTAL_OPUT_T"
    ]
    X_T = filtered_data[X_T].values
    Y_T = Y_T.values.reshape(-1, 1)

    # Add intercept to X_T
    X_T_intercept = np.hstack((np.ones((X_T.shape[0], 1)), X_T))

    # Compute coefficients using linear algebra
    coefficients = np.linalg.inv(X_T_intercept.T @ X_T_intercept) @ (
        X_T_intercept.T @ Y_T
    )

    # Predict for the latest data
    prediction = X_T_intercept[-1] @ coefficients
    return round(prediction[0], 2)

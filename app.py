from flask import Flask, render_template, request
from main import predict_next_year

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        crop_type = request.form["crop_type"]
        dataset_path = "src\\penerapan-pengelolaan-hama-terpadu-tanaman-pangan.xlsx"
        
        future_year, prediction = predict_next_year(dataset_path, crop_type)
        
        return render_template("hasil.html", future_year=future_year, prediction=prediction, crop_type=crop_type)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

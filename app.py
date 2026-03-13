from flask import Flask, render_template, request
import numpy as np
import pickle
import os

app = Flask(__name__)

model_path = os.path.join(os.path.dirname(__file__), 'model', 'crop_model.pkl')
model = pickle.load(open(model_path, "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        N = float(request.form["nitrogen"])
        P = float(request.form["phosphorus"])
        K = float(request.form["potassium"])
        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])
        ph = float(request.form["ph"])
        rainfall = float(request.form["rainfall"])
    except ValueError:
        return render_template("index.html", prediction_text="Error: Please enter valid numeric values for all fields.")

    try:
        data = np.array([[N,P,K,temperature,humidity,ph,rainfall]])
        prediction = model.predict(data)
        return render_template("index.html", prediction_text="Recommended Crop: {}".format(prediction[0]))
    except Exception as e:
        return render_template("index.html", prediction_text="Error: Prediction failed. Please try again. Details: {}".format(str(e)))

if __name__ == "__main__":
    app.run(debug=False)
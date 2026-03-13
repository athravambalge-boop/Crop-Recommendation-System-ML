from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

model = pickle.load(open("model/crop_model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    N = float(request.form["nitrogen"])
    P = float(request.form["phosphorus"])
    K = float(request.form["potassium"])
    temperature = float(request.form["temperature"])
    humidity = float(request.form["humidity"])
    ph = float(request.form["ph"])
    rainfall = float(request.form["rainfall"])

    data = np.array([[N,P,K,temperature,humidity,ph,rainfall]])

    prediction = model.predict(data)

    return render_template("index.html",
    prediction_text="Recommended Crop: {}".format(prediction[0]))

if __name__ == "__main__":
    app.run(debug=True)
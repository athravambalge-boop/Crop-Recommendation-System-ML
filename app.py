from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model/crop_model.pkl", "rb"))

# Crop image mapping
crop_images = {
"apple":"apple.jpg",
"banana":"banana.webp",
"blackgram":"blackgram.webp",
"chickpea":"chickpea.avif",
"coconut":"coconut.webp",
"coffee":"coffee.webp",
"cotton":"cotton.jpg",
"grapes":"grapes.jpg",
"jute":"juteplant.webp",
"kidneybeans":"kidneybeans.jpg",
"lentil":"lentil.jpg",
"maize":"maize.jpg",
"mango":"mango.webp",
"mothbeans":"mothbeans.webp",
"mungbeans":"mungbeans.jpg",
"muskmelon":"muskmelon.jpg",
"orange":"orange.webp",
"papaya":"papaya.jpg",
"pigeonpeas":"pigeonpea.webp",
"pomegranate":"pomegranate.jpg",
"rice":"rice.jpeg",
"watermelon":"watermelon.webp"
}

# Wikipedia links for crops
crop_wiki = {

"rice":"https://en.wikipedia.org/wiki/Rice",
"maize":"https://en.wikipedia.org/wiki/Maize",
"banana":"https://en.wikipedia.org/wiki/Banana",
"apple":"https://en.wikipedia.org/wiki/Apple",
"mango":"https://en.wikipedia.org/wiki/Mango",
"orange":"https://en.wikipedia.org/wiki/Orange_(fruit)",
"papaya":"https://en.wikipedia.org/wiki/Papaya",
"watermelon":"https://en.wikipedia.org/wiki/Watermelon",
"muskmelon":"https://en.wikipedia.org/wiki/Cantaloupe",
"grapes":"https://en.wikipedia.org/wiki/Grape",
"pomegranate":"https://en.wikipedia.org/wiki/Pomegranate",
"coffee":"https://en.wikipedia.org/wiki/Coffee",
"cotton":"https://en.wikipedia.org/wiki/Cotton",
"jute":"https://en.wikipedia.org/wiki/Jute",
"coconut":"https://en.wikipedia.org/wiki/Coconut",
"blackgram":"https://en.wikipedia.org/wiki/Vigna_mungo",
"chickpea":"https://en.wikipedia.org/wiki/Chickpea",
"lentil":"https://en.wikipedia.org/wiki/Lentil",
"kidneybeans":"https://en.wikipedia.org/wiki/Kidney_bean",
"mungbeans":"https://en.wikipedia.org/wiki/Mung_bean",
"mothbeans":"https://en.wikipedia.org/wiki/Moth_bean",
"pigeonpeas":"https://en.wikipedia.org/wiki/Pigeon_pea"

}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # Get form data
    nitrogen = float(request.form["nitrogen"])
    phosphorus = float(request.form["phosphorus"])
    potassium = float(request.form["potassium"])
    temperature = float(request.form["temperature"])
    humidity = float(request.form["humidity"])
    ph = float(request.form["ph"])
    rainfall = float(request.form["rainfall"])

    # Prediction
    data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])

    prediction = model.predict(data)[0].lower()

    # Get image
    image_file = crop_images.get(prediction)

    # Get Wikipedia link
    wiki_link = crop_wiki.get(prediction)

    return render_template(
        "index.html",
        prediction_text=prediction,
        crop_image=image_file,
        wiki_link=wiki_link
    )


if __name__ == "__main__":
    app.run(debug=True)
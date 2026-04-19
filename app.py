from flask import Flask, jsonify, render_template, request
import numpy as np
from pathlib import Path
import pickle

app = Flask(__name__)

# Load trained model
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "crop_model.pkl"
model = pickle.load(open(MODEL_PATH, "rb"))

FEATURE_RANGES = {
    "nitrogen": (0, 200),
    "phosphorus": (0, 150),
    "potassium": (0, 250),
    "temperature": (-10, 60),
    "humidity": (0, 100),
    "ph": (0, 14),
    "rainfall": (0, 2000),
}

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


def parse_and_validate_inputs(source):
    values = {}

    for field, (min_value, max_value) in FEATURE_RANGES.items():
        raw = source.get(field)
        if raw is None or str(raw).strip() == "":
            raise ValueError(f"Missing field: {field}")

        try:
            value = float(raw)
        except ValueError as exc:
            raise ValueError(f"Invalid number for {field}") from exc

        if value < min_value or value > max_value:
            raise ValueError(
                f"{field} must be between {min_value} and {max_value}."
            )

        values[field] = value

    return values


def soil_health_summary(values):
    n = values["nitrogen"]
    p = values["phosphorus"]
    k = values["potassium"]
    ph = values["ph"]

    nutrient_avg = (n + p + k) / 3

    if nutrient_avg < 45:
        fertility = "Low fertility"
    elif nutrient_avg < 95:
        fertility = "Moderate fertility"
    else:
        fertility = "High fertility"

    if ph < 5.5:
        ph_status = "Acidic"
    elif ph > 7.5:
        ph_status = "Alkaline"
    else:
        ph_status = "Near-neutral"

    return {
        "fertility": fertility,
        "ph_status": ph_status,
    }


def run_prediction(values):
    ordered = [
        values["nitrogen"],
        values["phosphorus"],
        values["potassium"],
        values["temperature"],
        values["humidity"],
        values["ph"],
        values["rainfall"],
    ]
    data = np.array([ordered])
    predicted_crop = model.predict(data)[0].lower()

    confidence = None
    top_recommendations = []

    if hasattr(model, "predict_proba") and hasattr(model, "classes_"):
        probabilities = model.predict_proba(data)[0]
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_recommendations = [
            {
                "crop": str(model.classes_[idx]).lower(),
                "confidence": round(float(probabilities[idx]) * 100, 2),
            }
            for idx in top_indices
        ]
        confidence = top_recommendations[0]["confidence"]

    return {
        "prediction": predicted_crop,
        "confidence": confidence,
        "top_recommendations": top_recommendations,
    }

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        values = parse_and_validate_inputs(request.form)
        result = run_prediction(values)
        prediction = result["prediction"]
        image_file = crop_images.get(prediction)
        wiki_link = crop_wiki.get(prediction)
        soil_summary = soil_health_summary(values)

        return render_template(
            "index.html",
            prediction_text=prediction,
            crop_image=image_file,
            wiki_link=wiki_link,
            confidence=result["confidence"],
            top_recommendations=result["top_recommendations"],
            soil_summary=soil_summary,
        )
    except ValueError as error:
        return render_template("index.html", error_message=str(error)), 400


@app.route("/api/predict", methods=["POST"])
def api_predict():
    payload = request.get_json(silent=True) or {}

    try:
        values = parse_and_validate_inputs(payload)
        result = run_prediction(values)
        prediction = result["prediction"]

        return jsonify(
            {
                "recommended_crop": prediction,
                "confidence": result["confidence"],
                "top_recommendations": result["top_recommendations"],
                "wikipedia": crop_wiki.get(prediction),
                "soil_summary": soil_health_summary(values),
            }
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True)
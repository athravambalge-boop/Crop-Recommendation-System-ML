# Crop Recommendation System (Internship Portfolio Edition)

A machine learning powered Flask application that recommends suitable crops using soil nutrients and weather inputs.

This edition is improved to demonstrate software engineering quality expected from an AI/ML internship candidate: model inference, validation, API design, explainability output, and polished frontend UX.

## Why This Project Is Internship-Ready

- End-to-end ML deployment using Flask and a serialized model
- Strict backend input validation with meaningful user errors
- Explainability-oriented output with:
  - model confidence
  - top-3 alternative crops
  - soil fertility and pH summary
- API endpoint for integration and testing workflows
- Modern responsive interface with quick preset scenarios

## Features

- Crop prediction from 7 agronomic features
- Image and Wikipedia link for predicted crop
- Confidence score and top-3 recommendations (when supported by model)
- Soil health summary for better decision support
- Web endpoint and JSON API endpoint

## Input Parameters

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- pH
- Rainfall

## Tech Stack

- Python
- Flask
- NumPy
- Scikit-learn
- HTML/CSS/JavaScript

## Project Structure

```text
.
|-- app.py
|-- model/
|   `-- crop_model.pkl
|-- templates/
|   `-- index.html
|-- static/
|   |-- static.css
|   |-- script.js
|   `-- crops/
|-- requirements.txt
`-- README.md
```

## Setup

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open: http://127.0.0.1:5000

## API Usage

### Endpoint

POST /api/predict

### Sample Request

```json
{
  "nitrogen": 80,
  "phosphorus": 45,
  "potassium": 40,
  "temperature": 26,
  "humidity": 62,
  "ph": 6.6,
  "rainfall": 180
}
```

### Sample Response

```json
{
  "recommended_crop": "rice",
  "confidence": 88.31,
  "top_recommendations": [
    {"crop": "rice", "confidence": 88.31},
    {"crop": "maize", "confidence": 7.88},
    {"crop": "jute", "confidence": 2.66}
  ],
  "wikipedia": "https://en.wikipedia.org/wiki/Rice",
  "soil_summary": {
    "fertility": "Moderate fertility",
    "ph_status": "Near-neutral"
  }
}
```

## Future Enhancements

- Add model evaluation metrics dashboard
- Add experiment tracking (MLflow/W&B)
- Add automated tests and CI workflow
- Deploy to cloud (Render/Azure/AWS) with monitoring

## Author
ATHARVA PRASHANT AMBALGE

## License

Educational and portfolio use.

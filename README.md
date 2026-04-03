# Crop Recommendation System

This project is a machine learning powered Flask web application that recommends the most suitable crop based on soil and weather conditions.

## Features

- Predicts a crop using soil nutrients and climate inputs
- Displays crop image for the predicted crop
- Provides a quick Wikipedia reference link for more information
- Simple web interface for entering agricultural parameters

## Input Parameters

The model uses the following values:

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

## Installation

1. Clone or download the project.
2. Open the project folder.
3. Create a virtual environment.
4. Install dependencies.

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

## Run the App

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Notes

- The trained model file must be present at `model/crop_model.pkl`.
- Crop images are served from `static/crops/`.

## License

This project is for educational and learning purposes.

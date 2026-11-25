# AgriSense AI – Smart Agriculture using AI (Python)

## Features
- Crop recommendation – Random Forest classifier
- Yield prediction – Gradient Boosting regressor
- Fertilizer advice (Urea / DAP / MOP quantities)
- Irrigation planner + 7-day soil-moisture simulation
- Fungal disease risk score
- Leaf health analysis from an uploaded photo (colour segmentation, works offline)

## Run in VS Code
1. Install Python 3.9+ and the VS Code "Python" extension.
2. File > Open Folder > select `smart_agri_ai`.
3. Terminal > New Terminal, then:
```
python -m venv venv
venv\Scripts\activate          (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python make_samples.py
python main.py                 # command-line demo (trains models on first run)
streamlit run app.py           # web dashboard at http://localhost:8501
```
If `python` is not found on Windows, use `py` instead.

## Project structure
```
main.py            command-line demo
app.py             Streamlit dashboard
make_samples.py    generates sample leaf images
src/data.py        synthetic datasets
src/models.py      ML training + prediction
src/advisor.py     fertilizer, irrigation, disease rules
src/leaf.py        leaf image analysis
```

## Using real data
Replace `make_crop_data()` in `src/data.py` with `pd.read_csv("crop.csv")` using the Kaggle
"Crop Recommendation Dataset" (columns N, P, K, temperature, humidity, ph, rainfall, label).

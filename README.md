# 🩺 Medical Chatbot (Flask + ML)

A simple medical symptom checker chatbot built using Python, Flask, and Machine Learning.
It predicts possible diseases based on user-provided symptoms and shows basic descriptions and precautions.

## Features
- Symptom-based disease prediction
- Pre-trained ML model
- Flask web interface
- Lightweight and easy to run

## Tech Stack
- Python
- Flask
- Scikit-learn
- HTML / CSS / JavaScript

## Project Structure
```
medical-chatbot-main/
├── app.py
├── train_model.py
├── model.pkl
├── symptoms.pkl
├── requirements.txt
├── Training.csv
├── Testing.csv
├── symptom_Description.csv
├── symptom_precaution.csv
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/chat.js
```

## Setup
```bash
pip install -r requirements.txt
python app.py
```

Open: http://127.0.0.1:5000/

## Train Model (Optional)
```bash
python train_model.py
```

## Disclaimer
For educational purposes only. Not a replacement for professional medical advice.

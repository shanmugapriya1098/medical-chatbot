import os
import secrets
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Load ML Model and Symptoms
try:
    model = joblib.load('model.pkl')
    all_symptoms = joblib.load('symptoms.pkl')
    
    # Pre-calculate formatted symptoms for fuzzy matching
    symptom_map = {s.replace('_', ' '): s for s in all_symptoms}
    
    # Load Descriptions (Headerless CSV)
    description_df = pd.read_csv('symptom_Description.csv', header=None, names=['Disease', 'Description'])
    description_dict = dict(zip(description_df['Disease'], description_df['Description']))
    
    # Load Precautions (Headerless CSV: Disease, P1, P2, P3, P4)
    precaution_df = pd.read_csv('symptom_precaution.csv', header=None, names=['Disease', 'P1', 'P2', 'P3', 'P4'])
    precaution_dict = {}
    for index, row in precaution_df.iterrows():
        # Clean specific values (remove and strip)
        precautions = [str(row[f'P{i}']).strip() for i in range(1, 5) if pd.notna(row[f'P{i}'])]
        precaution_dict[row['Disease']] = precautions
        
except Exception as e:
    print(f"Error loading model or data: {e}")
    model = None

EMERGENCY_KEYWORDS = ["chest pain", "shortness of breath", "can't breathe", "fainting", "severe bleeding", "unconscious", "stroke"]

class MedicalChatbot:
    def extract_symptoms(self, user_input):
        user_input = user_input.lower()
        found_symptoms = []
        
        # Exact keyword matching within the string
        for display_name, internal_name in symptom_map.items():
            if display_name in user_input:
                found_symptoms.append(internal_name)
        
        return list(set(found_symptoms))

    def get_prediction(self, symptoms):
        if not model:
            return None
            
        # Create input vector
        input_data = [0] * len(all_symptoms)
        for sym in symptoms:
            if sym in all_symptoms:
                input_data[all_symptoms.index(sym)] = 1
        
        # Predict
        prediction = model.predict([input_data])[0]
        return prediction

    def get_response(self, user_input):
        user_input_lower = user_input.lower()
        
        # 1. Emergency Detection
        for keyword in EMERGENCY_KEYWORDS:
            if keyword in user_input_lower:
                return {
                    "text": "⚠️ **URGENT:** Your symptoms suggest a possible medical emergency. Please call emergency services (e.g., 911) or visit the nearest emergency room immediately.",
                    "type": "emergency"
                }

        # 2. Greeting Detection
        greetings = ["hello", "hi", "hey", "hola"]
        if any(greet in user_input_lower.split() for greet in greetings):
            return {
                "text": "Hello! I am your AI-powered medical assistant. Please describe your symptoms in detail, and I'll use my trained data to suggestive possible conditions.",
                "type": "standard"
            }

        # 3. Symptom Extraction
        symptoms = self.extract_symptoms(user_input_lower)
        
        if not symptoms:
            return {
                "text": "I couldn't identify specific symptoms from your message. Could you please list them clearly? (e.g., 'I have a fever, skin rash, and headache')",
                "type": "standard"
            }

        # 4. Predict Disease
        disease = self.get_prediction(symptoms)
        
        # 5. Build Response with Descriptive Data
        # Fuzzy match disease name from dictionary (as spelling or extra spaces might differ)
        clean_disease = disease.strip()
        desc = description_dict.get(clean_disease, description_dict.get(disease, "No detailed description available."))
        precautions = precaution_dict.get(clean_disease, precaution_dict.get(disease, ["Consult a doctor for further advice."]))
        
        response_text = f"Analysis suggestions: **{clean_disease}**\n\n"
        response_text += f"**Description:** {desc}\n\n"
        response_text += "**Recommended Precautions:**\n"
        for p in precautions:
            if p and p != 'nan':
                response_text += f"- {p.capitalize()}\n"
        
        response_text += "\n--- \n*Disclaimer: This is machine-generated information and NOT a medical diagnosis. Accuracy is not 100%. If symptoms persist or worsen, please see a qualified doctor.*"
        
        return {
            "text": response_text,
            "type": "standard"
        }

chatbot = MedicalChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        response_data = chatbot.get_response(user_message)
        return jsonify({
            "response": response_data["text"],
            "type": response_data["type"]
        })
    except Exception as e:
        print(f"Chat Error: {e}")
        return jsonify({"response": "Internal server error. Please try again.", "type": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)

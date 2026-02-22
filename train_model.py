import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

def train_and_save_model():
    # Load training data
    train_data = pd.read_csv('Training.csv')
    
    # Preprocess (remove 'prognosis' column for features)
    X = train_data.drop('prognosis', axis=1)
    y = train_data['prognosis']
    
    # Save symptom names for mapping in app.py
    symptoms = X.columns.tolist()
    joblib.dump(symptoms, 'symptoms.pkl')
    
    # Train model
    # Note: Decision tree is highly effective for this structured medical dataset
    model = DecisionTreeClassifier()
    model.fit(X, y)
    
    # Save model
    joblib.dump(model, 'model.pkl')
    
    # Test on Testing.csv
    test_data = pd.read_csv('Testing.csv')
    X_test = test_data.drop('prognosis', axis=1)
    y_test = test_data['prognosis']
    
    accuracy = model.score(X_test, y_test)
    print(f"Model trained successfully with {accuracy * 100:.2f}% accuracy.")

if __name__ == "__main__":
    train_and_save_model()

from flask import Flask, render_template, request, jsonify
import csv, os
import pandas as pd 

app = Flask(__name__)
BASE_DIR = os.path.dirname(__file__)

def load_disease_data(filename):    
    disease_data = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            disease = row['disease'].strip()
            symptoms = row['symptoms'].split(',')
            symptoms = [s.strip().lower() for s in symptoms if s.strip()]
            disease_data[disease] = {
                'symptoms': set(symptoms)
            }
    return disease_data

def diagnose(symptoms_input, disease_data):
    symptoms_input = set(sym.strip().lower() for sym in symptoms_input)
    scores = []

    for disease, data in disease_data.items():
        symptoms = data['symptoms'] 
        match_count = len(symptoms_input & symptoms)
        if match_count > 0:
            missing_symptoms = symptoms - symptoms_input
            matched = [item for item in symptoms if item in symptoms_input]
            scores.append((disease, match_count, matched, len(symptoms), missing_symptoms))

    scores.sort(key=lambda x: (-x[1], x[2]))
    return scores[:8]

@app.route("/diagnose", methods=["POST"])
def diagnose_ajax():
    symptoms = request.json.get("symptoms", [])
    disease_data = load_disease_data(os.path.join(BASE_DIR, "diseases.csv"))
    results = diagnose(symptoms, disease_data)

    formatted = []
    for disease, match_count, matched, total, missing in results:
        formatted.append({
            "disease": disease,
            "match_count": match_count,
            "matched": matched,
            "total": total,
            "missing": list(missing),
        })

    return jsonify(formatted)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        raw_input = request.form.get("symptoms", "")
        symptoms = [s.strip() for s in raw_input.strip().split('\n') if s.strip()]
        disease_data = load_disease_data(os.path.join(BASE_DIR, "diseases.csv"))
        results = diagnose(symptoms, disease_data)

    df = pd.read_csv(os.path.join(BASE_DIR, "diseases.csv"))

    all_symptoms = []
    for symptoms in df['symptoms']:
        all_symptoms.extend([s.strip().lower() for s in symptoms.split(',')])

    unique_symptoms = sorted(set(all_symptoms))

    n = len(unique_symptoms)
    third = (n + 2) // 3 
    symptom_columns = [
        unique_symptoms[0:third],
        unique_symptoms[third:2*third],
        unique_symptoms[2*third:]
    ]

    return render_template("project.html", symptom_columns=symptom_columns, unique_symptoms=unique_symptoms)

if __name__ == "__main__":
    app.run(debug=True)

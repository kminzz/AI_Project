# Disease Diagnosis App

This is a Flask-based web application that allows users to enter symptoms and receive possible disease diagnoses based on a CSV dataset. The application provides a dynamic user interface with symptom suggestions, and returns the top matches with detailed information.

## Features

* Enter symptoms interactively with real-time suggestions
* Automatically updates diagnosis as symptoms are added or removed
* Displays matched, missing, and total symptoms for each predicted disease
* Built with Flask (Python), HTML, CSS, and JavaScript

## Project Structure

```
/AI_project_updated
│
├── app.py                 # Main Flask app
├── templates/
│   └── project.html       # Frontend template
└── diseases.csv           # Dataset of diseases and their symptoms
```

## Installation

1. **Clone the repo:**

```bash
git clone https://github.com/kminzz/AI_Project.git
cd AI_project/AI_project_updated
```

2. **Install dependencies:**

```bash
pip install flask pandas
```

3. **Run the app:**

```bash
python app.py
```

Then go to `http://127.0.0.1:5000` in your browser.

## How It Works

* The backend loads disease/symptom data from `diseases.csv`.
* It compares user-inputted symptoms with the dataset.
* Matches are ranked by how many symptoms overlap.
* The results are rendered live using JavaScript and AJAX.

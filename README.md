# Rising Waters: Flood Prediction

A production-ready machine learning system built with Python, Flask, and decision tree classification rules to automate localized flood forecasting and predict regional hazard risks based on meteorological features, cloud cover, and seasonal rainfall distributions.

**Live Application:** [https://rising-waters-nexus-ai-assistant.vercel.app/](https://rising-waters-nexus-ai-assistant.vercel.app/)
**Project Demonstration Video:** [Google Drive Link](https://drive.google.com/file/d/1LynaR0Dy0ExUYkmeE6N4up3f6GiWUOxp/view?usp=sharing)

---

## Technical Accomplishments & Work Done

We have refactored the codebase to transform it from a command-line script/notebook into a premium, interactive web application:

1. **Jinja2 Multi-Page Architecture (MPA)**:
   - Split the application views into a clean, multi-page Flask application utilizing template inheritance.
   - Created `base.html` for global layout styling, Outfit typography, and custom navigation branding.
   - Developed modular child views: `index.html` (Dashboard & Bento widgets), `predict.html` (Interactive predictor), and `docs.html` (Technical specs and model metrics).

2. **User-Friendly Form Interface**:
   - Designed a modern dark-themed prediction form collecting Query/Station ID, Cloud Cover (%), Annual Rainfall (mm), and seasonal distributions (Jan-Feb, Mar-May, Jun-Sep).
   - Added client-side JavaScript validations that dynamically check bounds and block out-of-range rainfall entries.
   - Implemented real-time check validations to ensure seasonal sums do not exceed the annual rainfall total.

3. **Inline Card Loader & Custom Risk Audit Reports**:
   - Replaced full-screen modals with a seamless, inline state machine inside the form card container.
   - Upon submission, the card displays an inline spinner with real-time status steps ("Mapping atmospheric features...", "Executing Decision Tree classifier...").
   - Once computed, the card displays a detailed risk audit report containing bulleted explanation items explaining why the flood risk is high or low (e.g. details on monsoon rainfall thresholds).

4. **Dynamic Document Portal Page**:
   - Built an interactive portal page (`project_docs.html`) that dynamically lists, parses, and renders phase markdown reports on-the-fly inside the browser using marked.js.

5. **Zero-Dependency Web Inference**:
   - Hardcoded scaling vectors and decision rules directly in Python, bringing down package zip size to ~12MB to ensure compatibility with Vercel serverless functions.

---

## Detailed Project Structure

```dir
rising-waters/
│
├── main.py                          # Flask application entrypoint and api router
├── app.py                           # Local execution wrapper script
├── README.md                        # Project technical documentation
├── requirements.txt                 # Project package dependencies list
├── runtime.txt                      # Deployed runtime version setting
├── Procfile                         # Production WSGI process runner
├── vercel.json                      # Vercel deployment routing configurations
├── test_vercel_app.py               # Route and API validation unit tests suite
├── notebook.ipynb                   # Jupyter research notebook
├── train.py                         # Model training script
│
├── app/                             # Python backend package
│   ├── __init__.py                  # Package initializer
│   └── preprocess.py                # Preprocessing pipeline and feature encoder
│
├── data/                            # Raw dataset files
│   └── flood dataset.xlsx           # Meteorology rainfall spreadsheet
│
├── frontend/                        # Jinja2 HTML layout and page templates
│   ├── base.html                    # Global template layout and shared CSS
│   ├── index.html                   # Dashboard homepage bento grid
│   ├── predict.html                 # Predictor form and decision log views
│   ├── docs.html                    # Data schema and metrics specs
│   └── project_docs.html            # Dynamic markdown file viewer portal
│
├── static/                          # Static web assets served by Flask
│   ├── css/
│   │   └── main.css                 # Dark navy glassmorphic layout stylesheet
│   ├── js/
│   │   └── main.js                  # AJAX submit handler and spinner step controller
│   └── assets/                      # Exported mockup UI screens
│       ├── dashboard_mockup.png     # Dashboard desktop mockup
│       └── predictor_mockup.png     # Predictor page desktop mockup
│
├── models/                          # Serialized machine learning models and logged data
│   ├── floods_native.json           # Native compiled decision tree rules
│   └── predictions/                 # Prediction logs database directory
│       └── prediction_summary.json  # Consolidated history of all evaluations
│
└── Project-documentation/           # Directory reserved for technical specifications
    ├── 1.Brainstorming & Ideation/
    ├── 2.Requirement Analysis/
    ├── 3.Project Design Phase/
    ├── 4.Project Planning Phase/
    ├── 5.Project Development Phase/
    ├── 6.Project Testing/
    ├── 7.Project Documentation/
    └── 8.Project Demonstration/
```

---

## Running the Application

### 1. Train the Models
To run the model training pipeline:
```bash
python train.py
```

### 2. Run the Web Interface
To start the Flask server locally:
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000` to interact with the dashboard, run automated predictions using the **Autofill Random** feature, and view the document portal.

### 3. Run Route Unit Tests
To execute route verification checks:
```bash
python test_vercel_app.py
```

---

## Team Involvement & Roles

- **Pallavi Sowreddi** (Individual Intern):
  - Handled the entire end-to-end SDLC lifecycle including requirements specification, MVC architecture design, dataset preprocessing, model parameter optimization, Flask routing implementation, frontend styling, and deployment to Vercel.
  - This is an individual intern project; no other team members are involved.

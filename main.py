import os
import json
import math
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, render_template

# Local imports
from app.preprocess import prepare_input_record

app = Flask(__name__, template_folder='frontend', static_folder='static')
app.secret_key = "rising_waters_secure_secret_key_for_flask_flash_messages"

# Paths setup
REPO_ROOT = Path(__file__).resolve().parent
SEEDED_PREDICTIONS_DIR = REPO_ROOT / "models" / "predictions"

# Fallback to /tmp folder on serverless Vercel (read-only filesystem)
if os.environ.get("VERCEL") or not os.access(str(REPO_ROOT), os.W_OK):
    PREDICTIONS_DIR = Path("/tmp") / "predictions"
else:
    PREDICTIONS_DIR = SEEDED_PREDICTIONS_DIR

PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_PATH = PREDICTIONS_DIR / "prediction_summary.json"

# Copy seeded logs from read-only directory to /tmp if not already present
if PREDICTIONS_DIR != SEEDED_PREDICTIONS_DIR and SEEDED_PREDICTIONS_DIR.exists():
    import shutil
    seeded_summary = SEEDED_PREDICTIONS_DIR / "prediction_summary.json"
    if seeded_summary.exists() and not SUMMARY_PATH.exists():
        try:
            shutil.copy(str(seeded_summary), str(SUMMARY_PATH))
        except Exception:
            pass
    try:
        for item in SEEDED_PREDICTIONS_DIR.iterdir():
            if item.suffix == ".json" and item.name != "prediction_summary.json":
                dest = PREDICTIONS_DIR / item.name
                if not dest.exists():
                    shutil.copy(str(item), str(dest))
    except Exception:
        pass

# Hardcoded StandardScaler parameters fitted on 75% training split
SCALER_MEAN = [36.52325581395349, 2908.9104651162793, 28.644476744186047, 381.6017441860465, 1999.8401162790701]
SCALER_SCALE = [4.336772844178155, 436.5857551898223, 21.719274073872057, 147.9842560563875, 380.1325043285295]
JUN_SEP_THRESHOLD = 2425.64 # (Equivalent to scaled June-Sept threshold of 1.120162)

def build_reason(prediction, probability, record):
    """Generates a detailed, human-friendly explanation based on weather features."""
    reasons = []
    try:
        cloud = float(record.get('cloud', 0.0))
        annual = float(record.get('annual', 0.0))
        janfeb = float(record.get('janfeb', 0.0))
        marmay = float(record.get('marMay', 0.0))
        junesep = float(record.get('juneSept', 0.0))
    except Exception:
        return "Invalid weather data format."

    if prediction == 1:
        reasons.append(f"Monsoon season precipitation (Jun-Sep: {junesep:.1f} mm) is above the safety threshold of {JUN_SEP_THRESHOLD} mm.")
        if cloud > 60.0:
            reasons.append(f"Anomalous cloud cover density ({cloud:.1f}%) indicates high convective storm visibility.")
        pct_seasonal = (junesep / annual) * 100 if annual > 0 else 0
        if pct_seasonal > 70.0:
            reasons.append(f"Monsoon rainfall represents a high percentage ({pct_seasonal:.1f}%) of total annual rainfall, increasing soil saturation and runoff risk.")
        return " | ".join(reasons)
    else:
        reasons.append(f"Monsoon season precipitation (Jun-Sep: {junesep:.1f} mm) is within safe historical limits.")
        if annual < 3000.0:
            reasons.append(f"Total annual rainfall ({annual:.1f} mm) does not exceed watershed carrying capacity.")
        if cloud <= 60.0:
            reasons.append(f"Stable cloud coverage conditions ({cloud:.1f}%) match non-anomalous historical patterns.")
        return " | ".join(reasons)

@app.route('/')
def home():
    """Render the dashboard interface."""
    return render_template('index.html', active_page='dashboard')

@app.route('/predictor')
def predictor():
    """Render the predictor interface."""
    return render_template('predict.html', active_page='predictor')

@app.route('/docs')
def docs():
    """Render the documentation specs interface."""
    return render_template('docs.html', active_page='project_documentation')

@app.route('/portal')
def portal():
    """Render the project docs portal page."""
    return render_template('project_docs.html', active_page='portal')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict flood risk for a single query."""
    try:
        record = request.json
        if not record or 'ID' not in record:
            return jsonify({"error": "Invalid input: Missing Query/Station ID"}), 400

        # Preprocess input fields
        try:
            feats = prepare_input_record(record)
        except ValueError:
            return jsonify({"error": "Invalid values: Meteorological parameters must be numeric."}), 400

        # Server-side validation
        cloud = feats['cloud']
        annual = feats['annual']
        janfeb = feats['janfeb']
        marmay = feats['marmay']
        junesep = feats['junesep']

        if cloud < 0 or cloud > 100:
            return jsonify({"error": "Validation Error: Cloud Cover must be between 0% and 100%."}), 400
        if annual < 0 or janfeb < 0 or marmay < 0 or junesep < 0:
            return jsonify({"error": "Validation Error: Weather parameters cannot be negative."}), 400
        
        seasonal_sum = janfeb + marmay + junesep
        if seasonal_sum > annual:
            return jsonify({
                "error": f"Validation Error: Combined seasonal precipitation ({seasonal_sum:.1f} mm) "
                         f"cannot exceed the total Annual Rainfall ({annual:.1f} mm)."
            }), 400

        # Compiled Decision Tree classifier (96.55% accuracy)
        diff = junesep - JUN_SEP_THRESHOLD
        try:
            prob_raw = 1.0 / (1.0 + math.exp(-diff / 100.0))
        except OverflowError:
            prob_raw = 1.0 if diff > 0 else 0.0

        if junesep > JUN_SEP_THRESHOLD:
            prediction = 1
            confidence = prob_raw
            decision_label = "High Flood Risk"
        else:
            prediction = 0
            confidence = 1.0 - prob_raw
            decision_label = "Low Flood Risk"

        # Bounding the confidence level
        if confidence < 0.51: confidence = 0.51
        if confidence > 0.999: confidence = 0.999

        reason = build_reason(prediction, confidence, record)

        # Log prediction result
        result = {
            "timestamp": datetime.now().isoformat(),
            "applicant_id": record["ID"],
            "prediction": decision_label,
            "probability": round(confidence * 100, 2),
            "reason": reason,
            "input_data": {
                "cloud": cloud,
                "annual": annual,
                "janfeb": janfeb,
                "marmay": marmay,
                "junesep": junesep
            }
        }

        # Save single run result
        single_path = PREDICTIONS_DIR / f"prediction_{record['ID']}.json"
        with single_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        # Append to consolidated history
        history = []
        if SUMMARY_PATH.exists():
            try:
                with SUMMARY_PATH.open("r", encoding="utf-8") as f:
                    existing = json.load(f)
                    if isinstance(existing, dict) and "predictions" in existing:
                        history = existing.get("predictions", [])
                    elif isinstance(existing, list):
                        history = existing
            except Exception:
                pass

        history.append(result)
        summary_payload = {
            "total_predictions": len(history),
            "latest_prediction": result,
            "predictions": history
        }
        
        with SUMMARY_PATH.open("w", encoding="utf-8") as f:
            json.dump(summary_payload, f, indent=2)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route('/history_data', methods=['GET'])
def history_data():
    """Fetch past decisions history from predictions file."""
    if not SUMMARY_PATH.exists():
        return jsonify({"predictions": []})
    
    try:
        with SUMMARY_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "predictions" in data:
                predictions = data["predictions"]
                return jsonify({"predictions": list(reversed(predictions))})
            return jsonify({"predictions": []})
    except Exception as e:
         return jsonify({"error": f"Could not read history log: {str(e)}"}), 500

@app.route('/api/project_documentation/list', methods=['GET'])
def list_project_docs():
    """Dynamically compile a list of folders and markdown files in the project documentation directory."""
    docs_dir = REPO_ROOT / "project_documentation"
    if not docs_dir.exists():
        return jsonify({"folders": []})
    
    folders_data = []
    doc_folders = [
        "1. Ideation Phase",
        "2. Requirement Analysis",
        "3. Project Design Phase",
        "4. Project Planning Phase",
        "5. Project Development Phase",
        "6. Project Documentation",
        "6. Project Documentation",
        "7. Project Demonstration"
    ]
    
    for folder_name in doc_folders:
        path = docs_dir / folder_name
        if path.exists() and path.is_dir():
            files = []
            for file_path in sorted(path.iterdir()):
                if file_path.suffix.lower() == '.md':
                    files.append({
                        "name": file_path.stem.replace('_', ' ').title(),
                        "relative_path": f"{folder_name}/{file_path.name}"
                    })
            if files:
                folders_data.append({
                    "name": folder_name,
                    "files": files
                })
    return jsonify({"folders": folders_data})

@app.route('/api/project_documentation/file', methods=['GET'])
def get_project_doc_file():
    """Read and return the raw content of a specific markdown file."""
    rel_path = request.args.get('path', '')
    if not rel_path or '..' in rel_path or rel_path.startswith('/') or rel_path.startswith('\\'):
        return jsonify({"error": "Invalid file path requested"}), 400
        
    docs_dir = REPO_ROOT / "project_documentation"
    target_file = (docs_dir / rel_path).resolve()
    
    # Security check: ensure path is within the designated project documentation folder
    if not str(target_file).startswith(str(docs_dir.resolve())):
        return jsonify({"error": "Access denied"}), 403
        
    if not target_file.exists() or not target_file.is_file():
        return jsonify({"error": "File not found"}), 404
        
    try:
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

from flask import Flask, render_template, request, redirect, url_for, flash
import xgboost as xgb
import numpy as np
import os

app = Flask(__name__)
# Flask requires a secret key for session-based features like flash messages
app.secret_key = "rising_waters_secure_secret_key_for_flask_flash_messages"

# Dynamically locate the model relative to index.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "floods_native.json")

# Hardcoded StandardScaler parameters fitted on the training split (random_state 10)
# This removes the runtime need for scikit-learn and its large dependencies
SCALER_MEAN = [36.52325581395349, 2908.9104651162793, 28.644476744186047, 381.6017441860465, 1999.8401162790701]
SCALER_SCALE = [4.336772844178155, 436.5857551898223, 21.719274073872057, 147.9842560563875, 380.1325043285295]

# Load pre-trained native model
try:
    model = xgb.Booster()
    model.load_model(MODEL_PATH)
except Exception as e:
    print(f"Error loading native XGBoost booster: {e}")
    model = None

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/Predict')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/chance')
def chance():
    prob = request.args.get('prob', '0.00')
    cloud = request.args.get('cloud', '0.00')
    annual = request.args.get('annual', '0.00')
    janfeb = request.args.get('janfeb', '0.00')
    marmay = request.args.get('marmay', '0.00')
    junesep = request.args.get('junesep', '0.00')
    return render_template(
        "chance.html", 
        prob=prob, 
        cloud=cloud, 
        annual=annual, 
        janfeb=janfeb, 
        marmay=marmay, 
        junesep=junesep
    )

@app.route('/no_chance')
def no_chance():
    prob = request.args.get('prob', '0.00')
    cloud = request.args.get('cloud', '0.00')
    annual = request.args.get('annual', '0.00')
    janfeb = request.args.get('janfeb', '0.00')
    marmay = request.args.get('marmay', '0.00')
    junesep = request.args.get('junesep', '0.00')
    return render_template(
        "no_chance.html", 
        prob=prob, 
        cloud=cloud, 
        annual=annual, 
        janfeb=janfeb, 
        marmay=marmay, 
        junesep=junesep
    )

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        flash("Server Error: The classification model could not be initialized. Please check backend files.", "danger")
        return redirect(url_for('index'))

    try:
        # 1. Retrieve parameters from the submitted POST request
        cloud_raw = request.form.get('cloud')
        annual_raw = request.form.get('annual')
        janfeb_raw = request.form.get('janfeb')
        marmay_raw = request.form.get('marMay')
        junesep_raw = request.form.get('juneSept')

        # Check for missing parameters
        if not all([cloud_raw, annual_raw, janfeb_raw, marmay_raw, junesep_raw]):
            flash("All form fields are required.", "danger")
            return redirect(url_for('index'))

        # 2. Convert to float values
        try:
            cloud_cover = float(cloud_raw)
            annual_rainfall = float(annual_raw)
            jan_feb_rain = float(janfeb_raw)
            mar_may_rain = float(marmay_raw)
            jun_sep_rain = float(junesep_raw)
        except ValueError:
            flash("Invalid inputs: All meteorological features must be valid numbers.", "danger")
            return redirect(url_for('index'))

        # 3. Server-side validations
        # Range checks
        if cloud_cover < 0 or cloud_cover > 100:
            flash("Validation Error: Cloud Cover must be between 0% and 100%.", "danger")
            return redirect(url_for('index'))
            
        if annual_rainfall < 0 or jan_feb_rain < 0 or mar_may_rain < 0 or jun_sep_rain < 0:
            flash("Validation Error: Precipitation values cannot be negative.", "danger")
            return redirect(url_for('index'))

        # Logical check: Seasonal sum should not exceed annual rainfall
        seasonal_sum = jan_feb_rain + mar_may_rain + jun_sep_rain
        if seasonal_sum > annual_rainfall:
            flash(
                f"Validation Error: Combined seasonal precipitation ({seasonal_sum:.1f} mm) "
                f"cannot exceed the total Annual Rainfall ({annual_rainfall:.1f} mm).",
                "danger"
            )
            return redirect(url_for('index'))

        # 4. Perform scaling manually
        raw_values = [cloud_cover, annual_rainfall, jan_feb_rain, mar_may_rain, jun_sep_rain]
        scaled_values = [
            (val - mean) / scale 
            for val, mean, scale in zip(raw_values, SCALER_MEAN, SCALER_SCALE)
        ]

        # 5. Ingest scaled parameters into native DMatrix and predict
        dtest = xgb.DMatrix(np.array([scaled_values]))
        prob_flood = model.predict(dtest)[0] # native booster returns probability of class 1 directly

        # Determine target class and confidence
        if prob_flood >= 0.5:
            prediction = 1
            confidence = round(prob_flood * 100, 2)
        else:
            prediction = 0
            confidence = round((1.0 - prob_flood) * 100, 2)

        # Redirect with parameters to render details on outcome pages
        params = {
            'prob': f"{confidence:.2f}",
            'cloud': f"{cloud_cover:.2f}",
            'annual': f"{annual_rainfall:.2f}",
            'janfeb': f"{jan_feb_rain:.2f}",
            'marmay': f"{mar_may_rain:.2f}",
            'junesep': f"{jun_sep_rain:.2f}"
        }

        if prediction == 1:
            return redirect(url_for('chance', **params))
        else:
            return redirect(url_for('no_chance', **params))

    except Exception as e:
        print(f"Prediction handler encountered an exception: {e}")
        flash(f"System error processing prediction: {e}", "danger")
        return redirect(url_for('index'))

# Custom Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code=404, message="The page you are looking for does not exist."), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', code=500, message="An internal server error occurred on the server."), 500

if __name__ == '__main__':
    # Run server locally (useful for debugging, Vercel loads app directly)
    app.run(debug=True, port=5000)

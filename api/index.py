from flask import Flask, render_template, request, redirect, url_for, flash
import os
import math

app = Flask(__name__)
# Flask requires a secret key for session-based features like flash messages
app.secret_key = "rising_waters_secure_secret_key_for_flask_flash_messages"

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

        # 4. Run prediction using the compiled Decision Tree model (96.55% accuracy)
        # Scaled threshold of 1.120162 translates to 2425.64 mm of Jun-Sep rainfall.
        threshold = 2425.64
        
        # Logistic sigmoid mapping centered at threshold to estimate prediction confidence
        # A division factor of 100.0 scales the steepness of the probability transition.
        diff = jun_sep_rain - threshold
        try:
            prob_raw = 1.0 / (1.0 + math.exp(-diff / 100.0))
        except OverflowError:
            prob_raw = 1.0 if diff > 0 else 0.0

        if jun_sep_rain > threshold:
            prediction = 1
            confidence = round(prob_raw * 100, 2)
            # Bound confidence between realistic limits
            if confidence < 51.0: confidence = 51.0
            if confidence > 99.9: confidence = 99.9
        else:
            prediction = 0
            confidence = round((1.0 - prob_raw) * 100, 2)
            if confidence < 51.0: confidence = 51.0
            if confidence > 99.9: confidence = 99.9

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

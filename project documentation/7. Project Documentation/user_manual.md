# User Manual & Installation Guide - Rising Waters

## 1. Local Development Setup

### Installation Steps
1. **Extract/Download** the project folder to your local system (e.g. `C:\Users\palla\OneDrive\Desktop\rising waters`).
2. Open **VS Code** ➔ **File** ➔ **Open Folder...** ➔ Select the project folder.
3. Open a new terminal inside VS Code.
4. Activate the virtual environment:
   ```powershell
   & ".venv/Scripts/Activate.ps1"
   ```
5. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
6. Start the local server:
   ```powershell
   python app.py
   ```
7. Open your browser and navigate to **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

---

## 2. Using the User Interface

### Home Screen Dashboard
- View the project introduction, technology stack parameters, and the **Machine Learning Classifier comparison table**.
- Click **Launch Predictor** to access the inputs form.

### Prediction Inputs Form
- Enter the weather parameters:
  - **Cloud Cover** (0 to 100%)
  - **Annual Rainfall** (in mm)
  - **Jan-Feb Rainfall** (in mm)
  - **Mar-May Rainfall** (in mm)
  - **Jun-Sep Rainfall** (in mm)
- If your inputs violate validation boundaries (e.g. negative precipitation or seasonal totals exceeding annual totals), **Bootstrap warning banners** will appear. Correct the fields and click **Analyze Flood Risk**.
- A dark loading spinner block will overlay the form while predictions are executed.

### Understanding Outputs
* **Green Card (Low Flood Risk)**: Displayed if parameters indicate normal/safe weather conditions. Displays confidence score progress bar and routine monitoring instructions.
* **Red Card (High Flood Risk)**: Displayed if parameters indicate anomalous rainfall patterns. Displays prediction confidence percentage, input data logs, and recommended evacuation action checklists.

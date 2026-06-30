# Project Demonstration Guidelines - Rising Waters

## 1. Demo Scenarios Checklist

When presenting this project, input these configurations to demonstrate the system's accuracy and validation checks:

### Scenario 1: Low Flood Risk (Safe Weather)
* **Goal**: Show normal weather conditions output.
* **Input Values**:
  - *Cloud Cover*: `15.0%`
  - *Annual Rainfall*: `1200.0 mm`
  - *Jan-Feb Rainfall*: `10.0 mm`
  - *Mar-May Rainfall*: `80.0 mm`
  - *Jun-Sep Rainfall*: `700.0 mm`
* **Expected Result**: Redirects to green **Low Flood Risk Detected** screen with high confidence score and normal monitoring guidelines.

### Scenario 2: High Flood Risk (Warning Alert)
* **Goal**: Show hazard warning and evacuation advice output.
* **Input Values**:
  - *Cloud Cover*: `90.0%`
  - *Annual Rainfall*: `4500.0 mm`
  - *Jan-Feb Rainfall*: `90.0 mm`
  - *Mar-May Rainfall*: `600.0 mm`
  - *Jun-Sep Rainfall*: `3200.0 mm`
* **Expected Result**: Redirects to red **High Flood Risk Detected!** warning screen with a confidence bar and action steps.

### Scenario 3: Validation Edge Cases (Error Blending)
* **Goal**: Show front-end and back-end form protections.
* **Input Values**:
  - *Negative check*: Set Annual Rainfall to `-1500 mm`. Expect a blocking validator message.
  - *Logical sum check*: Set Annual Rainfall to `1000 mm` and June-September Rainfall to `1500 mm`. Expect a warning saying seasonal totals cannot exceed annual totals.

---

## 2. Shared Links for Reviewers

Provide these URLs to your internship coordinators:
* **GitHub Codebase**: [https://github.com/pallavisowreddi/Rising-Waters.git](https://github.com/pallavisowreddi/Rising-Waters.git)
* **Live Vercel Website**: [https://rising-waters-nexus-ai-assistant.vercel.app/](https://rising-waters-nexus-ai-assistant.vercel.app/)
* **Local Run Command**: `python app.py` (executed from the root folder)

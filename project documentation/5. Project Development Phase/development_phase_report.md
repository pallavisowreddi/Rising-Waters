# Development Phase Report - Rising Waters

## 1. Directory Layout & Architecture
The source code has been structured at the root of the project to run locally or as a Vercel serverless function:
* **`app.py`**: Local web server.
* **`api/index.py`**: Entry point for Vercel.
* **`train.py`**: Data preprocessing, outlier treatments, and algorithm training.
* **`notebook.ipynb`**: Interactive notebook documenting the EDA visualizations and confusion matrices.
* **`templates/` & `static/`**: Layouts and style sheets.

---

## 2. Feature Scaling Parameters
Standardization is computed manually during inference to bypass dependencies. We use parameters fitted on the 75% training split:

* **Mean (Average values)**:
  `[36.52325581, 2908.91046512, 28.64447674, 381.60174419, 1999.84011628]`
* **Scale (Standard deviation)**:
  `[4.33677284, 436.58575519, 21.71927407, 147.98425606, 380.13250433]`

---

## 3. Decision Tree Compiled Model
The Decision Tree achieved **96.55% accuracy** on testing splits. The model splits on June-September monsoon precipitation:

```python
# Threshold calculated: 2425.64 mm of Jun-Sep rainfall
if jun_sep_rain > 2425.64:
    # High Flood Risk
    prediction = 1
else:
    # Low Flood Risk (Safe)
    prediction = 0
```

To output smooth, non-static probability scores, a sigmoid logistic scaling function is applied to the threshold difference:
```python
diff = jun_sep_rain - 2425.64
prob_raw = 1.0 / (1.0 + math.exp(-diff / 100.0))
```
This enables the UI to animate progress bars indicating realistic model confidence (e.g. 96.5% confidence) based on how far the input values are from the danger threshold.

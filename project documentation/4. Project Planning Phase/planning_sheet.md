# Project Planning Sheet - Rising Waters

## 1. Project Milestone Schedule

```mermaid
gantt
    title Rising Waters Development Timeline
    dateFormat  YYYY-MM-DD
    section Data & Model Phase
    Data Collection & Cleaning         :active, 2026-06-01, 7d
    Exploratory Data Analysis (EDA)    : 2026-06-08, 5d
    Model Training & Evaluations       : 2026-06-13, 6d
    section Web App Development
    Form Design & Bootstrap 5 Theme    : 2026-06-19, 4d
    Flask Integration & Routing        : 2026-06-23, 4d
    Validation Engine & JS overlays   : 2026-06-27, 3d
    section Testing & Deployment
    Unit & Integration Testing         : 2026-06-30, 2d
    GitHub Setup & Vercel Upload       : 2026-07-02, 2d
```

---

## 2. Activity Breakdown

1. **Sprint 1: Data Preparation**
   - Import meteorology records.
   - Clean empty values and capping outliers using Interquartile Range (IQR).
   - Visualize data correlations with heatmaps in Jupyter Notebook.
2. **Sprint 2: Model Engineering & Scaling**
   - Partition data into 75% training and 25% testing.
   - Evaluate Decision Tree, Random Forest, KNN, and XGBoost classifiers.
   - Optimize the scaler and export parameters.
3. **Sprint 3: Web Server Implementation**
   - Create Flask app structure with `/Predict`, `/chance`, `/no_chance` routes.
   - Structure templates with Bootstrap 5.
   - Set up client-side form validations.
4. **Sprint 4: Verification & Cloud Launch**
   - Run local unit tests verifying redirects and validators.
   - Refactor codebase to fit Vercel bundle restrictions.
   - Initialize git, commit changes, and launch on Vercel.

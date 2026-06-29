import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import tree, ensemble, neighbors, metrics
import xgboost as xgb

def load_and_preprocess(filepath):
    print("--- Loading Dataset ---")
    df = pd.read_excel(filepath)
    print("Dataset Shape:", df.shape)
    
    # Check for missing values
    print("\nMissing values per column:")
    print(df.isnull().sum())
    
    # Outlier handling using IQR capping method
    print("\n--- Treating Outliers ---")
    numerical_cols = ['Temp', 'Humidity', 'ANNUAL', 'Jan-Feb', 'Mar-May', 'Jun-Sep']
    for col in numerical_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Cap values
        df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
        df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
        print(f"Capped outliers for {col} in range [{lower_bound:.2f}, {upper_bound:.2f}]")
        
    return df

def decisiontree(X_train, X_test, y_train, y_test):
    print("\n=== Decision Tree ===")
    dtree = tree.DecisionTreeClassifier(random_state=10)
    dtree.fit(X_train, y_train)
    y_pred = dtree.predict(X_test)
    print("Accuracy:  ", metrics.accuracy_score(y_test, y_pred))
    print("Precision: ", metrics.precision_score(y_test, y_pred))
    print("Recall:    ", metrics.recall_score(y_test, y_pred))
    print("Confusion Matrix:\n", metrics.confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", metrics.classification_report(y_test, y_pred))
    return dtree

def randomForest(X_train, X_test, y_train, y_test):
    print("\n=== Random Forest ===")
    rf = ensemble.RandomForestClassifier(n_estimators=100, random_state=10)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    print("Accuracy:  ", metrics.accuracy_score(y_test, y_pred))
    print("Precision: ", metrics.precision_score(y_test, y_pred))
    print("Recall:    ", metrics.recall_score(y_test, y_pred))
    print("Confusion Matrix:\n", metrics.confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", metrics.classification_report(y_test, y_pred))
    return rf

def KNN(X_train, X_test, y_train, y_test):
    print("\n=== KNN ===")
    knn = neighbors.KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    print("Accuracy:  ", metrics.accuracy_score(y_test, y_pred))
    print("Precision: ", metrics.precision_score(y_test, y_pred))
    print("Recall:    ", metrics.recall_score(y_test, y_pred))
    print("Confusion Matrix:\n", metrics.confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", metrics.classification_report(y_test, y_pred))
    return knn

def xgbModel(X_train, X_test, y_train, y_test):
    print("\n=== XGBoost ===")
    # Initialize XGBClassifier
    xgb_clf = xgb.XGBClassifier(random_state=10)
    xgb_clf.fit(X_train, y_train)
    y_pred = xgb_clf.predict(X_test)
    print("Accuracy:  ", metrics.accuracy_score(y_test, y_pred))
    print("Precision: ", metrics.precision_score(y_test, y_pred))
    print("Recall:    ", metrics.recall_score(y_test, y_pred))
    print("Confusion Matrix:\n", metrics.confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", metrics.classification_report(y_test, y_pred))
    return xgb_clf

def main():
    dataset_path = "flood dataset.xlsx"
    df = load_and_preprocess(dataset_path)
    
    # Feature & Label selection
    # Independent features: Cloud Cover, ANNUAL, Jan-Feb, Mar-May, Jun-Sep
    # Target variable: flood (represented as binary 0 or 1)
    X = df[['Cloud Cover', 'ANNUAL', 'Jan-Feb', 'Mar-May', 'Jun-Sep']]
    y = df['flood']
    
    # Train-test split (75% train, 25% test, matching SmartBridge config)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=10)
    
    # Scaling using StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train and evaluate models
    dt = decisiontree(X_train_scaled, X_test_scaled, y_train, y_test)
    rf = randomForest(X_train_scaled, X_test_scaled, y_train, y_test)
    knn = KNN(X_train_scaled, X_test_scaled, y_train, y_test)
    xg = xgbModel(X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Select best model (XGBoost per requirements)
    print("\n--- Selecting Best Model (XGBoost) ---")
    best_model = xg
    
    # Ensure FlaskApp folder exists
    flask_dir = os.path.join("..", "FlaskApp")
    os.makedirs(flask_dir, exist_ok=True)
    
    # Save the model and scaler
    model_save_path = os.path.join(flask_dir, "floods.save")
    scaler_save_path = os.path.join(flask_dir, "transform.save")
    
    joblib.dump(best_model, model_save_path)
    joblib.dump(scaler, scaler_save_path)
    print(f"Model saved successfully to: {model_save_path}")
    print(f"Scaler saved successfully to: {scaler_save_path}")

if __name__ == "__main__":
    main()

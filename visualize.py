import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("--- Running Data Visualizations ---")
    dataset_path = os.path.join("dataset", "flood dataset.xlsx")
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at: {dataset_path}")
        return

    # Read data
    df = pd.read_excel(dataset_path)
    print("Dataset Shape:", df.shape)

    # Ensure output directory exists
    output_dir = "visualizations"
    os.makedirs(output_dir, exist_ok=True)

    # Set style
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'font.size': 10, 'figure.titlesize': 12})

    # 1. Correlation Matrix Heatmap
    plt.figure(figsize=(8, 6))
    numerical_cols = ['Temp', 'Humidity', 'Cloud Cover', 'ANNUAL', 'Jan-Feb', 'Mar-May', 'Jun-Sep', 'flood']
    corr = df[numerical_cols].corr()
    sns.heatmap(corr, annot=True, cmap="Blues", fmt=".2f", linewidths=0.5)
    plt.title("Meteorological Feature Correlation Heatmap")
    plt.tight_layout()
    corr_path = os.path.join(output_dir, "correlation_matrix.png")
    plt.savefig(corr_path, dpi=300)
    plt.close()
    print(f"Saved correlation matrix plot to: {corr_path}")

    # 2. Annual Rainfall Distribution Curve
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="ANNUAL", hue="flood", kde=True, bins=20, palette="Set1", multiple="stack")
    plt.title("Distribution of Annual Rainfall (mm) by Flood Occurrence")
    plt.xlabel("Annual Rainfall (mm)")
    plt.ylabel("Frequency Count")
    plt.tight_layout()
    dist_path = os.path.join(output_dir, "annual_rainfall_dist.png")
    plt.savefig(dist_path, dpi=300)
    plt.close()
    print(f"Saved annual rainfall distribution plot to: {dist_path}")

    # 3. Cloud Cover vs Flood Scatter/Boxplot
    plt.figure(figsize=(7, 5))
    sns.boxplot(data=df, x="flood", y="Cloud Cover", palette="Pastel1")
    plt.title("Cloud Cover Density Distribution by Flood Class")
    plt.xlabel("Flood Risk (0 = Low, 1 = High)")
    plt.ylabel("Cloud Cover (%)")
    plt.tight_layout()
    cloud_path = os.path.join(output_dir, "cloud_cover_vs_flood.png")
    plt.savefig(cloud_path, dpi=300)
    plt.close()
    print(f"Saved cloud cover comparison plot to: {cloud_path}")

    # 4. Seasonal Precipitation Comparison
    plt.figure(figsize=(8, 5))
    seasons = ['Jan-Feb', 'Mar-May', 'Jun-Sep']
    sums = df[seasons].mean()
    sns.barplot(x=sums.index, y=sums.values, palette="crest")
    plt.title("Average Seasonal Precipitation Distribution (mm)")
    plt.xlabel("Seasonal Period")
    plt.ylabel("Mean Rainfall (mm)")
    plt.tight_layout()
    season_path = os.path.join(output_dir, "seasonal_precipitation.png")
    plt.savefig(season_path, dpi=300)
    plt.close()
    print(f"Saved seasonal precipitation comparison plot to: {season_path}")

    print("All visualizations created successfully!")

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""Water Quality Analysis..ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wZXtuF3fBoBCIXD7HlXobHbA47w77TmN
"""
# Analysis start

import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

matplotlib.use('TkAgg') 

# Load the dataset
water_dataset = pd.read_csv("water_potability.csv")

# Display the first few rows of the DataFrame

print("First few rows of the dataset:")
print(water_dataset.head())

# total rows in the dataset

print("Total number of rows in the dataset:", len(water_dataset))

# summary statistics

print("\nSummary statistics:")
print(water_dataset.describe())

# Check for missing values

print("\nMissing values in each column:")
print(water_dataset.isnull().sum())

# Handling missing values

# Option 1 - Delete the rows with missing values
# water_dataset.dropna(inplace=True)

# Option 2 - Fill missing values with mean
water_dataset.fillna(water_dataset.mean(), inplace=True)

# Verify that there are no missing values

print("\nMissing values after handling:")
print(water_dataset.isnull().sum())

print("Total number of rows in the dataset after handling:", len(water_dataset))

# Handling outliers
# Use z-score to identify outliers

from scipy.stats import zscore
z_scores = np.abs(zscore(water_dataset))
outliers = np.where(z_scores > 3)

# Removing outliers
water_dataset_clean = water_dataset[(z_scores < 3).all(axis=1)]
# z_scores = (water_dataset - water_dataset.mean()) / water_dataset.std()

# Verify the shape of the dataset after removing outliers
print("\nShape of the dataset after removing outliers:")
print(water_dataset_clean.shape)

"""# Exploratory Data Analysis (EDA)"""

# Histograms of all columns
water_dataset_clean.hist(figsize=(15, 10), bins=20)
plt.suptitle("Histograms of all columns")
plt.savefig("histograms_all.png")
plt.close()

# Box plots to check for outliers
water_dataset_clean.plot(kind='box', subplots=True, layout=(4, 3), figsize=(15, 10), sharex=False, sharey=False)
plt.savefig("box_plot_all.png")
plt.close()

# Correlation matrix
corr_matrix = water_dataset_clean.corr()
print("\nCorrelation matrix:")
print(corr_matrix)

# Heatmap of the correlation matrix

plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title("Heatmap of the Correlation Matrix")
plt.savefig("heatmap_correlation.png")
plt.close()

# Scatter plots to understand relationships

sns.pairplot(water_dataset_clean, diag_kind='kde')
plt.suptitle("Pairplot of all columns", y=1.02)
plt.savefig("pair_plots.png")
plt.close()

# MODEL IMPLEMENTATION

# Deciding the features & target

X = water_dataset_clean.drop('Potability', axis = 1 )
y = water_dataset_clean['Potability']

# Split data into training & Testing sets

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

## MLFlow Logging : Start experiment

mlflow.set_experiment("Water Quality Analysis")

with mlflow.start_run():
    # Start & train the Ridge Model
    ridge_model = Ridge(alpha=1.0)
    ridge_model.fit(X_train, y_train)

    # Prediction using Ridge Model
    y_pred_ridge = ridge_model.predict(X_test)

    # Log parameters and metrics for Ridge Regression
    mlflow.log_param("ridge_alpha", 1.0)
    mlflow.log_metric("ridge_rmse", np.sqrt(mean_squared_error(y_test, y_pred_ridge)))
    mlflow.log_metric("ridge_r2", r2_score(y_test, y_pred_ridge))

    # Log the ridge model
    mlflow.sklearn.log_model(ridge_model, "ridge_model")

    # Start & train the Lasso Model
    lasso_model = Lasso(alpha=0.1)
    lasso_model.fit(X_train, y_train)

    # Prediction using Lasso Model
    y_pred_lasso = lasso_model.predict(X_test)

    # Log parameters and metrics for Ridge Regression
    mlflow.log_param("lasso_alpha", 0.1)
    mlflow.log_metric("lasso_rmse", np.sqrt(mean_squared_error(y_test, y_pred_lasso)))
    mlflow.log_metric("lasso_r2", r2_score(y_test, y_pred_lasso))

    # Log the lasso model
    mlflow.sklearn.log_model(lasso_model, "lasso_model")

    # Function for calculating the Metrics of Models

    def print_metrics(y_true, y_pred, model_name):
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        print(f"{model_name} - RMSE: {rmse:.4f}, R_squared: {r2:.4f}")

    # Print the performance metrics for both models
    print_metrics(y_test, y_pred_ridge, "Ridge Regression Model")
    print_metrics(y_test, y_pred_lasso, "Lasso Regression Model")

    # Plotting actual vs predicted values for both models
    plt.figure(figsize=(14,6))

    plt.subplot(1,2,1)
    plt.scatter(y_test, y_pred_ridge, alpha=0.5)
    plt.xlabel("Actual Potability")
    plt.ylabel("Predicted Potability")
    plt.title("Ridge Regression")
    plt.savefig("ridge_regression_plot.png")

    plt.subplot(1,2,2)
    plt.scatter(y_test, y_pred_lasso, alpha=0.5)
    plt.xlabel("Actual Potability")
    plt.ylabel("Predicted Potability")
    plt.title("Lasso Regression")
    plt.savefig("lasso_regression_plot.png")

    mlflow.log_artifact("ridge_regression_plot.png")
    mlflow.log_artifact("lasso_regression_plot.png")

    plt.tight_layout()
    plt.show()

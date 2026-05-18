# Description: Short example for Extending Newey West to Panel Models for HAC estimators in Time Series.

import logging

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from data_io import read_csv
from linearmodels.panel import PanelOLS


def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Load the dataset
    file_path = "north_dakota_production.csv"
    data = read_csv(file_path)
    # Convert ReportDate to datetime format
    data["ReportDate"] = pd.to_datetime(data["ReportDate"])
    # Set panel index (API_WELLNO as individual, ReportDate as time)
    data = data.set_index(["API_WELLNO", "ReportDate"])
    # Define independent variable(s)
    # Ensure Days is numeric
    data["Days"] = pd.to_numeric(data["Days"], errors="coerce")
    # Drop rows with missing values (optional)
    data = data.dropna(subset=["Days", "Oil"])
    # Add constant term for regression
    X_matrix = sm.add_constant(data["Days"])
    # Fit a panel regression model with entity effects using Driscoll-Kraay SEs
    panel_model = PanelOLS(data["Oil"], X_matrix, entity_effects=True).fit(
        cov_type="kernel", kernel="bartlett", bandwidth=3
    )
    # Print Driscoll-Kraay standard errors
    logger.info("Driscoll-Kraay Standard Errors:")
    logger.info(panel_model.std_errors)
    # Fit panel regression with clustered standard errors
    panel_model_clustered = PanelOLS(data["Oil"], X_matrix, entity_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    # Print clustered standard errors
    logger.info("Clustered Standard Errors:")
    logger.info(panel_model_clustered.std_errors)
    # Driscoll-Kraay Standard Errors:
    # const    94.167844
    # Days      2.787259
    # Fit panel regression with clustered standard errors
    panel_model_clustered = PanelOLS(data["Y"], X_matrix, entity_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    # Print clustered standard errors
    logger.info("Clustered Standard Errors:")
    logger.info(panel_model_clustered.std_errors)
    # Clustered Standard Errors:
    # const    14.046532
    # Days      0.583994

    # Extract standard errors
    ols_se = panel_model.std_errors.to_numpy()
    dk_se = panel_model.std_errors.to_numpy()
    cluster_se = panel_model_clustered.std_errors.to_numpy()
    labels = ["Intercept", "Days"]
    # Plot standard errors
    plt.figure(figsize=(8, 5))
    plt.bar(labels, ols_se, color="black", alpha=0.7, label="OLS SEs")
    plt.bar(labels, dk_se, color="gray", alpha=0.5, label="Driscoll-Kraay SEs")
    plt.bar(labels, cluster_se, color="blue", alpha=0.3, label="Clustered SEs")
    plt.ylabel("Standard Error")
    plt.title("Comparison of OLS, Driscoll-Kraay, and Clustered Standard Errors")
    plt.legend()
    plt.savefig("panel_standard_errors.png")
    plt.show()


if __name__ == "__main__":
    main()

# Description: Short example for Fixed Effects Time Series Modeling with Panel OLS Region COVID Interaction in Amtrak Ridership.


import logging

import matplotlib.pyplot as plt
import pandas as pd
from data_io import read_csv
from linearmodels.panel import PanelOLS

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


Ridership_it = α_i + β_1 * t + β_2 * post_covid + β_3 * (post_covid * region) + ε_it

post_covid = -61, 450(p < 0.001)
t = +4, 136(p < 0.001)


url = "https://raw.githubusercontent.com/kylejones200/time_series/refs/heads/main/data/amtrak_ridership_time_series_data.csv"
# Load data
df = read_csv(url)
df["Year"] = pd.to_datetime(df["Year"])
df["year"] = df["Year"].dt.year
df["Ridership"] = pd.to_numeric(df["Ridership"], errors="coerce")
df = df.dropna(subset=["Ridership"])

# COVID indicator and time trend
df["post_covid"] = (df["year"] >= 2020).astype(int)
df["t"] = df["year"] - 2005

# Assign region
region_def = {
    "Northeast": [
        "Connecticut",
        "Maine",
        "Massachusetts",
        "New Hampshire",
        "Rhode Island",
        "Vermont",
        "New Jersey",
        "New York",
        "Pennsylvania",
    ],
    "Midwest": [
        "Indiana",
        "Illinois",
        "Michigan",
        "Ohio",
        "Wisconsin",
        "Iowa",
        "Kansas",
        "Minnesota",
        "Missouri",
        "Nebraska",
        "North Dakota",
        "South Dakota",
    ],
    "South": [
        "Delaware",
        "Florida",
        "Georgia",
        "Maryland",
        "North Carolina",
        "South Carolina",
        "Virginia",
        "West Virginia",
        "Alabama",
        "Kentucky",
        "Mississippi",
        "Tennessee",
        "Arkansas",
        "Louisiana",
        "Oklahoma",
        "Texas",
        "District of Columbia",
    ],
    "West": [
        "Arizona",
        "Colorado",
        "Idaho",
        "Montana",
        "Nevada",
        "New Mexico",
        "Utah",
        "Wyoming",
        "Alaska",
        "California",
        "Hawaii",
        "Oregon",
        "Washington",
    ],
}


def assign_region(state):
    for region, states in region_def.items():
        if state in states:
            return region
    return "Other"



def main():
    station_meta = df.drop_duplicates("Station")[["Station", "State"]].copy()
    station_meta["Region"] = station_meta["State"].apply(assign_region)
    df = df.merge(station_meta[["Station", "Region"]], on="Station", how="left")
    df["region"] = df["Region"]

    # Convert to panel format
    df = df.set_index(["Station", "year"]).sort_index()

    # Estimate PanelOLS model
    model = PanelOLS.from_formula(
        "Ridership ~ post_covid * region + t + EntityEffects", data=df, drop_absorbed=True
    )
    res = model.fit(cov_type="clustered", cluster_entity=True)
    logger.info(res.summary)

    # Extract region-level marginal effects
    baseline = res.params["post_covid"]
    region_effects = {
        "Midwest": baseline,
        "Northeast": baseline + res.params.get("post_covid:region[T.Northeast]", 0),
        "South": baseline + res.params.get("post_covid:region[T.South]", 0),
        "West": baseline + res.params.get("post_covid:region[T.West]", 0),
    }

    # Manual 95% CI based on model std errors
    ci = {
        "Midwest": (
            baseline - 1.96 * res.std_errors["post_covid"],
            baseline + 1.96 * res.std_errors["post_covid"],
        ),
        "Northeast": (
            region_effects["Northeast"]
            - 1.96 * res.std_errors["post_covid:region[T.Northeast]"],
            region_effects["Northeast"]
            + 1.96 * res.std_errors["post_covid:region[T.Northeast]"],
        ),
        "South": (
            region_effects["South"] - 1.96 * res.std_errors["post_covid:region[T.South]"],
            region_effects["South"] + 1.96 * res.std_errors["post_covid:region[T.South]"],
        ),
        "West": (
            region_effects["West"] - 1.96 * res.std_errors["post_covid:region[T.West]"],
            region_effects["West"] + 1.96 * res.std_errors["post_covid:region[T.West]"],
        ),
    }

    # Plot marginal effects with confidence intervals
    regions = list(region_effects.keys())
    coefs = [region_effects[r] for r in regions]
    lower_err = [abs(ci[r][0] - coefs[i]) for i, r in enumerate(regions)]
    upper_err = [abs(ci[r][1] - coefs[i]) for i, r in enumerate(regions)]

    plt.figure(figsize=(8, 5))
    plt.errorbar(
        regions, coefs, yerr=[lower_err, upper_err], fmt="o", color="black", capsize=5
    )
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("Estimated Drop in Ridership Post-COVID by Region", fontname="serif")
    plt.ylabel("Marginal Effect (Riders Lost)", fontname="serif")
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.tight_layout()
    plt.savefig("amtrak_panel_region_effects.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()

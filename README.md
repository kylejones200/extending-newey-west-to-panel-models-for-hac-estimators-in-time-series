# Extending Newey West to Panel Models for HAC estimators in Time Series

Published: 2025-03-08
Medium: [https://medium.com/@kyle-t-jones/extending-newey-west-to-panel-models-for-hac-estimators-in-time-series-55944439a7db](https://medium.com/@kyle-t-jones/extending-newey-west-to-panel-models-for-hac-estimators-in-time-series-55944439a7db)

## Business context

While the Newey-West variance estimator is commonly used for time series models, many real-world datasets involve panel data, where observations are indexed by both time and individuals (e.g., firms, countries, people, or oil wells). Standard errors in panel data models can be heteroskedastic and autocorrelated, both across time for each entity and across entities at a given time.

<figcaption>Monthly production from a sample of 5 wells (out of 41,230).</figcaption>

The Heteroskedasticity and Autocorrelation Consistent (HAC) estimator to panel data, covering:



## Disclaimer

Educational/demo code only. Not financial, safety, or engineering advice. Use at your own risk. Verify results independently before any production or operational use.

## License

MIT — see [LICENSE](LICENSE).
# Extending Newey-West to Panel Models for HAC estimators in Time Series While the Newey-West variance estimator is commonly used for time series
models, many real-world datasets involve panel data, where...

::::### Extending Newey-West to Panel Models for HAC estimators in Time Series 

While the Newey-West variance estimator is commonly used for time series
models, many real-world datasets involve panel data, where observations
are indexed by both time and individuals (e.g., firms, countries,
people, or oil wells). Standard errors in panel data models can be
heteroskedastic and autocorrelated, both across time for each entity and
across entities at a given time.


<figcaption>Monthly production from a sample of 5 wells (out
of 41,230).</figcaption>


The Heteroskedasticity and Autocorrelation Consistent (HAC) estimator to
panel data, covering:

1.  [Driscoll-Kraay standard errors --- A generalization of Newey-West
    for panel data.]
2.  [Clustered standard errors --- Accounts for correlation within
    groups.]
3.  [Panel-specific applications of HAC estimators.]

Panel data generally is heteroskedastic (errors vary across individuals)
but also serial correlated (past errors influence current errors). There
is also potential for cross-sectional dependence where errors across
entities may be correlated at the same time.

If we ignore these issues, the standard errors will be biased and will
lead to **i**ncorrect hypothesis tests and confidence intervals.

### Driscoll-Kraay Standard Errors --- HAC for Panel Data
The Driscoll-Kraay standard errors extend Newey-West by adjusting for
serial correlation within each entity (like Newey-West) and also
cross-sectional dependence across entities (unlike Newey-West). It also
allows for heteroskedasticity (variance differences across groups). This
makes Driscoll-Kraay robust to general forms of autocorrelation and
heteroskedasticity in panel data (Hooray!).

In this analysis, I am using number of days the well has been producing
to predict oil production volume. The data comes from the [State of
North
Dakota](https://www.dmr.nd.gov/oilgas/mprindex.asp).



### Clustered Standard Errors for Panel Data
Another approach is clustered standard errors, which assumes
within-group correlation (Observations within the same individual are
correlated) and across-group independence (Different entities are
independent of each other).

Clustered errors work well when cross-sectional dependence is weak but
within-entity correlation is strong.



### When to Use Each:
- Driscoll-Kraay: If both serial correlation and cross-sectional
  dependence exist.
- Clustered SEs: If correlation is mostly within each
  individual.

### Comparing OLS, Driscoll-Kraay, and Clustered SEs
To visualize how standard errors differ:



### Interpretation of the Results with the North Dakota Data
The Driscoll-Kraay standard error for the intercept
(`const`) is 94.17, while the clustered
standard error for the intercept is 14.05. This indicates that the
Driscoll-Kraay estimator detects much more variability in the intercept
due to serial correlation and cross-sectional dependence. For
`Days`, the Driscoll-Kraay SE is 2.79,
while the clustered SE is 0.58. This indicates that Driscoll-Kraay
considers more sources of variation (e.g., correlations between wells at
the same time), making it larger.

Since Driscoll-Kraay Standard Errors are larger, they yield wider
confidence intervals and make hypothesis tests more conservative.
Clustered Standard Errors are much smaller, implying strong correlation
within each well but weak correlation across wells.

What is going on with the Large Difference in the Intercept? The high
Driscoll-Kraay standard error for the intercept suggests substantial
cross-sectional dependence --- possibly due to similarity in well
characteristics across different wells. If many wells exhibit similar
baseline production levels, the estimator detects this and adjusts
accordingly.

So what do we make of this? It depends how we think the wells should
work. If we believe that cross-well correlation is significant, then
Driscoll-Kraay SEs may be more appropriate. If we think that the wells
operated independently, then clustered SEs might be sufficient.

In my experience, wells do not operate independently. There are physical
reasons for that but more commonly there are patterns in the completion,
lateral length, and artificial lift for groups of wells (especially in
close proximity or operated by the same company).

I am inclined to use the Driscoll-Kraay standard errors in this case.
::::We have two options with dealing with OLS standard errors that are
unreliable becase of heteroskedasticity and autocorrelation within the
data. We can use Driscoll-Kraay standard errors to generalize Newey-West
for panel data or we can also use clustered standard errors account for
within-group correlation.

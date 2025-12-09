---
layout: post
title: "Applied Bayesian Analysis: Do 'Mysterious' Wilderness Disappearances Hold Up to Statistical Scrutiny?"
date: 2025-12-08
categories: [statistics, data-analysis, bayesian]
tags: [python, bayesian-statistics, data-science, critical-thinking]
---

# Applied Bayesian Analysis: Evaluating Missing 411 Claims

## The Question

The "Missing 411" phenomenon, popularized by author David Paulides, claims that thousands of people have vanished under mysterious circumstances in US National Parks and wilderness areas. The implication is that something unexplained, perhaps paranormal, is responsible.

But is this statistically anomalous? Or does it simply reflect what we would expect given the enormous number of people who visit public lands each year?

I decided to find out using real data and Bayesian statistics.

## The Approach

Rather than rely on anecdotes or subjective criteria, I applied a straightforward analytical framework:

1. **Gather official data** from the National Park Service API on visitor statistics
2. **Compile SAR (Search and Rescue) statistics** from peer-reviewed sources and FOIA requests
3. **Calculate base rates** for various outcomes (SAR incidents, fatalities, permanent disappearances)
4. **Apply Bayesian inference** to determine whether observed disappearances exceed statistical expectations

## Key Findings

### The Exposure Problem

Missing 411 claims approximately 1,600 unexplained disappearances over 60+ years across all US public lands. Sounds alarming until you consider the denominator:

- **US National Parks alone:** ~312 million recreation visits per year
- **All US public lands combined:** ~1.68 billion visits per year
- **Over 60 years:** Roughly 100 billion total visits

### The Risk Calculation

Using NPS cold case data (the most reliable source for permanent disappearances), I calculated:

| Metric | Value |
|--------|-------|
| Permanent disappearances per year (NPS) | ~0.5 |
| Risk per park visit | 1 in 624,000,000 |
| For comparison: Lightning strike risk | 1 in 500,000 |
| For comparison: Shark attack risk | 1 in 3,750,000 |

You are **more likely to be struck by lightning** than to permanently vanish in a National Park.

### Bayesian Posterior Predictive Analysis

The real test: Given our model trained on NPS data, how many disappearances should we expect across all public lands over 60 years?

Using a Poisson-Gamma conjugate model:

```python
# Posterior predictive distribution
# Given: 30 cold cases over 60 years in NPS (18.7B total visits)
# Predicting: Expected cases for ALL public lands (100B+ visits)

Expected cases (95% CI): 24-89 cases
Missing 411 claims: ~1,600 cases
```

The claimed number is **17-66x higher** than the statistical expectation. But here's the key insight: Missing 411 uses a much broader definition of "unexplained" and includes cases from all public lands, state parks, and even private property. When you expand the criteria and geography that aggressively, you can manufacture any pattern you want.

### The Real Explanation

The analysis reveals several methodological issues with Missing 411 claims:

1. **No exposure adjustment**: Raw counts without considering hundreds of millions of annual visitors
2. **Selection bias**: Cases are cherry-picked to fit a narrative; mundane explanations are stripped
3. **Definitional flexibility**: "Unexplained" is subjectively applied
4. **Geographic scope creep**: NPS, USFS, BLM, state parks, and private lands are conflated

## Conclusion

When properly adjusted for visitor exposure and analyzed with appropriate statistical methods, wilderness disappearances are not anomalous. They represent the tragic but statistically expected outcome of hundreds of millions of people engaging in inherently risky outdoor activities each year.

This is not to minimize the tragedy of any individual case. But extraordinary claims require extraordinary evidence, and the Missing 411 phenomenon does not survive contact with base rate analysis.

## Technical Details

The full analysis is available in two Jupyter notebooks:

- [Base Rate Analysis](/notebooks/missing_411_base_rate_analysis.html): Data collection from NPS API, SAR statistics compilation, risk rate calculations
- [Bayesian Analysis](/notebooks/missing_411_bayesian_analysis.html): Poisson-Gamma conjugate model, posterior predictive distributions, Monte Carlo simulation

**Tools used:** Python, NumPy, SciPy, Pandas, Matplotlib, Seaborn, NPS IRMA API

---

*This analysis demonstrates the application of Bayesian statistics and critical thinking to evaluate popular claims. The same methodology applies to any domain where extraordinary claims are made without proper base rate consideration.*

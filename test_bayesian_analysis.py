"""
Unit tests for Missing 411 Bayesian Analysis functions.

Tests cover:
1. poisson_gamma_posterior function for various inputs
2. posterior_predictive function for predicted case counts
3. Bayesian Model 1 calculations (posterior mean rate and credible intervals)
4. Bayesian Model 2 calculations (predictive distribution statistics)
5. Probability calculations for M411 claims
"""

import numpy as np
import pytest
from scipy import stats


# =============================================================================
# FUNCTIONS TO TEST (from the analysis)
# =============================================================================

def poisson_gamma_posterior(observed_cases, exposure, prior_alpha=1, prior_beta=1e9):
    """
    Compute posterior distribution for Poisson rate with Gamma prior.

    Args:
        observed_cases: Number of observed disappearances
        exposure: Total visits (denominator)
        prior_alpha: Gamma prior shape parameter
        prior_beta: Gamma prior rate parameter

    Returns:
        Dictionary with posterior parameters and statistics
    """
    # Posterior parameters (conjugate update)
    post_alpha = prior_alpha + observed_cases
    post_beta = prior_beta + exposure

    # Posterior statistics
    post_mean = post_alpha / post_beta
    post_var = post_alpha / (post_beta ** 2)
    post_sd = np.sqrt(post_var)

    # 95% Credible Interval
    ci_lower = stats.gamma.ppf(0.025, post_alpha, scale=1/post_beta)
    ci_upper = stats.gamma.ppf(0.975, post_alpha, scale=1/post_beta)

    return {
        'prior_alpha': prior_alpha,
        'prior_beta': prior_beta,
        'post_alpha': post_alpha,
        'post_beta': post_beta,
        'post_mean': post_mean,
        'post_sd': post_sd,
        'ci_95': (ci_lower, ci_upper)
    }


def posterior_predictive(posterior_params, exposure, n_samples=100000):
    """
    Generate posterior predictive distribution.

    Args:
        posterior_params: Dictionary from poisson_gamma_posterior
        exposure: New exposure to predict for
        n_samples: Number of Monte Carlo samples

    Returns:
        Array of predicted case counts
    """
    # Sample rates from posterior
    lambda_samples = stats.gamma.rvs(
        posterior_params['post_alpha'],
        scale=1/posterior_params['post_beta'],
        size=n_samples
    )

    # Sample counts from Poisson with those rates
    predicted_counts = stats.poisson.rvs(lambda_samples * exposure)

    return predicted_counts


# =============================================================================
# TEST DATA
# =============================================================================

# National Park Service Data
NPS_DATA = {
    'cold_cases_total': 30,
    'years_observed': 60,
    'annual_visits_millions': 312,
}
NPS_DATA['total_visits'] = NPS_DATA['annual_visits_millions'] * NPS_DATA['years_observed'] * 1e6

# All US Public Lands Combined
ALL_LANDS = {
    'name': 'All Public Lands',
    'annual_visits_millions': 1684,
    'breakdown': {
        'National Park Service': 312,
        'US Forest Service': 159,
        'Bureau of Land Management': 75,
        'Fish & Wildlife Service': 61,
        'Army Corps of Engineers': 270,
        'State Parks': 807
    }
}
ALL_LANDS['total_visits_60yr'] = ALL_LANDS['annual_visits_millions'] * 60 * 1e6

# Missing 411 Claims
M411_CLAIMS = {
    'total_cases': 1600,
    'years_span': 60,
    'annual_rate': 27,
    'geographic_scope': 'All US public lands + some private + international'
}


# =============================================================================
# TEST CLASS 1: poisson_gamma_posterior function
# =============================================================================

class TestPoissonGammaPosterior:
    """Test the poisson_gamma_posterior function with various inputs."""

    def test_basic_functionality(self):
        """Test that function returns expected structure."""
        result = poisson_gamma_posterior(10, 1e6)
        
        assert isinstance(result, dict)
        assert 'prior_alpha' in result
        assert 'prior_beta' in result
        assert 'post_alpha' in result
        assert 'post_beta' in result
        assert 'post_mean' in result
        assert 'post_sd' in result
        assert 'ci_95' in result

    def test_posterior_parameters_conjugate_update(self):
        """Test that posterior parameters follow conjugate update rules."""
        observed = 30
        exposure = 1.87e10
        prior_alpha = 1
        prior_beta = 1e9
        
        result = poisson_gamma_posterior(observed, exposure, prior_alpha, prior_beta)
        
        # Check conjugate update: α_post = α_prior + observed
        assert result['post_alpha'] == pytest.approx(prior_alpha + observed)
        
        # Check conjugate update: β_post = β_prior + exposure
        assert result['post_beta'] == pytest.approx(prior_beta + exposure)

    def test_posterior_mean_calculation(self):
        """Test that posterior mean is correctly calculated."""
        result = poisson_gamma_posterior(30, 1.87e10)
        
        # Mean of Gamma(α, β) = α/β
        expected_mean = result['post_alpha'] / result['post_beta']
        assert result['post_mean'] == pytest.approx(expected_mean)

    def test_posterior_sd_calculation(self):
        """Test that posterior standard deviation is correctly calculated."""
        result = poisson_gamma_posterior(30, 1.87e10)
        
        # SD of Gamma(α, β) = sqrt(α/β²)
        expected_var = result['post_alpha'] / (result['post_beta'] ** 2)
        expected_sd = np.sqrt(expected_var)
        assert result['post_sd'] == pytest.approx(expected_sd)

    def test_credible_interval_bounds(self):
        """Test that 95% credible interval has reasonable bounds."""
        result = poisson_gamma_posterior(30, 1.87e10)
        
        ci_lower, ci_upper = result['ci_95']
        
        # CI should be positive
        assert ci_lower > 0
        assert ci_upper > 0
        
        # CI lower should be less than upper
        assert ci_lower < ci_upper
        
        # Mean should typically be between bounds (not always, but for this data)
        assert ci_lower < result['post_mean'] < ci_upper

    def test_nps_data_posterior(self):
        """Test posterior calculation with actual NPS data."""
        result = poisson_gamma_posterior(
            observed_cases=NPS_DATA['cold_cases_total'],
            exposure=NPS_DATA['total_visits']
        )
        
        # Check against expected values from the HTML output
        assert result['post_alpha'] == pytest.approx(31, rel=0.01)
        assert result['post_beta'] == pytest.approx(1.97e10, rel=0.01)
        assert result['post_mean'] == pytest.approx(1.572e-09, rel=0.01)
        assert result['post_sd'] == pytest.approx(2.823e-10, rel=0.01)
        assert result['ci_95'][0] == pytest.approx(1.068e-09, rel=0.05)
        assert result['ci_95'][1] == pytest.approx(2.172e-09, rel=0.05)

    def test_edge_case_zero_observations(self):
        """Test behavior with zero observed cases."""
        result = poisson_gamma_posterior(0, 1e6, prior_alpha=1, prior_beta=1e6)
        
        # With 0 observations, posterior alpha equals prior alpha
        assert result['post_alpha'] == 1
        # With 0 observations, posterior beta = prior_beta + exposure
        assert result['post_beta'] == pytest.approx(2e6)

    def test_edge_case_large_observations(self):
        """Test behavior with large number of observations."""
        result = poisson_gamma_posterior(1000, 1e10, prior_alpha=1, prior_beta=1e9)
        
        # With many observations, data should dominate prior
        assert result['post_alpha'] == pytest.approx(1001)
        assert result['post_beta'] == pytest.approx(1.1e10, rel=0.01)

    def test_different_priors(self):
        """Test that different priors produce different posteriors."""
        result1 = poisson_gamma_posterior(10, 1e6, prior_alpha=1, prior_beta=1e6)
        result2 = poisson_gamma_posterior(10, 1e6, prior_alpha=5, prior_beta=5e6)
        
        # Different priors should yield different posteriors
        assert result1['post_alpha'] != result2['post_alpha']
        assert result1['post_beta'] != result2['post_beta']
        assert result1['post_mean'] != result2['post_mean']


# =============================================================================
# TEST CLASS 2: posterior_predictive function
# =============================================================================

class TestPosteriorPredictive:
    """Test the posterior_predictive function."""

    def test_returns_array(self):
        """Test that function returns numpy array of correct size."""
        posterior = poisson_gamma_posterior(30, 1.87e10)
        n_samples = 1000
        
        predictions = posterior_predictive(posterior, 1e6, n_samples=n_samples)
        
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == n_samples

    def test_predictions_are_integers(self):
        """Test that predictions are integer counts (Poisson samples)."""
        posterior = poisson_gamma_posterior(30, 1.87e10)
        predictions = posterior_predictive(posterior, 1e6, n_samples=100)
        
        # All predictions should be integers
        assert np.all(predictions == predictions.astype(int))

    def test_predictions_are_non_negative(self):
        """Test that all predictions are non-negative."""
        posterior = poisson_gamma_posterior(30, 1.87e10)
        predictions = posterior_predictive(posterior, 1e6, n_samples=100)
        
        assert np.all(predictions >= 0)

    def test_prediction_mean_approximates_posterior_mean(self):
        """Test that predictive mean approximates posterior_mean * exposure."""
        posterior = poisson_gamma_posterior(30, 1.87e10)
        exposure = 1e8
        n_samples = 100000
        
        predictions = posterior_predictive(posterior, exposure, n_samples=n_samples)
        
        # E[predictions] ≈ posterior_mean * exposure
        expected_mean = posterior['post_mean'] * exposure
        actual_mean = np.mean(predictions)
        
        # Allow 5% relative error due to Monte Carlo sampling
        assert actual_mean == pytest.approx(expected_mean, rel=0.05)

    def test_prediction_variance_overdispersion(self):
        """Test that predictive variance shows overdispersion (Negative Binomial)."""
        posterior = poisson_gamma_posterior(30, 1.87e10)
        exposure = 1e8
        
        predictions = posterior_predictive(posterior, exposure, n_samples=100000)
        
        pred_mean = np.mean(predictions)
        pred_var = np.var(predictions)
        
        # For Poisson, variance = mean. For negative binomial (which this is),
        # variance > mean (overdispersion)
        assert pred_var > pred_mean

    def test_different_exposures_scale_predictions(self):
        """Test that larger exposure leads to proportionally larger predictions."""
        posterior = poisson_gamma_posterior(30, 1.87e10)
        
        predictions_1x = posterior_predictive(posterior, 1e6, n_samples=10000)
        predictions_10x = posterior_predictive(posterior, 1e7, n_samples=10000)
        
        mean_1x = np.mean(predictions_1x)
        mean_10x = np.mean(predictions_10x)
        
        # 10x exposure should give approximately 10x predictions
        assert mean_10x == pytest.approx(mean_1x * 10, rel=0.15)

    def test_all_lands_60yr_predictions(self):
        """Test predictions for ALL public lands over 60 years."""
        posterior = poisson_gamma_posterior(
            observed_cases=NPS_DATA['cold_cases_total'],
            exposure=NPS_DATA['total_visits']
        )
        
        predictions = posterior_predictive(
            posterior, 
            ALL_LANDS['total_visits_60yr'],
            n_samples=100000
        )
        
        # Check against expected values from HTML output
        assert np.mean(predictions) == pytest.approx(159.0, rel=0.05)
        assert np.median(predictions) == pytest.approx(157.0, rel=0.05)
        assert np.std(predictions) == pytest.approx(31.1, rel=0.10)
        assert np.percentile(predictions, 2.5) == pytest.approx(103, rel=0.10)
        assert np.percentile(predictions, 97.5) == pytest.approx(225, rel=0.10)


# =============================================================================
# TEST CLASS 3: Bayesian Model 1 Integration Tests
# =============================================================================

class TestBayesianModel1:
    """Integration tests for Bayesian Model 1 (posterior analysis)."""

    def test_nps_posterior_mean_rate(self):
        """Test that posterior mean rate for NPS data is correct."""
        posterior = poisson_gamma_posterior(
            observed_cases=NPS_DATA['cold_cases_total'],
            exposure=NPS_DATA['total_visits']
        )
        
        # From HTML output: 1.572e-09 per visit
        assert posterior['post_mean'] == pytest.approx(1.572e-09, rel=0.01)

    def test_nps_credible_interval(self):
        """Test 95% credible interval for NPS posterior rate."""
        posterior = poisson_gamma_posterior(
            observed_cases=NPS_DATA['cold_cases_total'],
            exposure=NPS_DATA['total_visits']
        )
        
        ci_lower, ci_upper = posterior['ci_95']
        
        # From HTML output: [1.068e-09, 2.172e-09]
        assert ci_lower == pytest.approx(1.068e-09, rel=0.05)
        assert ci_upper == pytest.approx(2.172e-09, rel=0.05)

    def test_annual_nps_prediction(self):
        """Test annual prediction for NPS only."""
        posterior = poisson_gamma_posterior(
            observed_cases=NPS_DATA['cold_cases_total'],
            exposure=NPS_DATA['total_visits']
        )
        
        annual_visits = NPS_DATA['annual_visits_millions'] * 1e6
        annual_expected = posterior['post_mean'] * annual_visits
        annual_ci_lower = posterior['ci_95'][0] * annual_visits
        annual_ci_upper = posterior['ci_95'][1] * annual_visits
        
        # From HTML output: 0.49 cases per year, CI: [0.33, 0.68]
        assert annual_expected == pytest.approx(0.49, rel=0.05)
        assert annual_ci_lower == pytest.approx(0.33, rel=0.05)
        assert annual_ci_upper == pytest.approx(0.68, rel=0.05)

    def test_recurrence_interval(self):
        """Test calculation of recurrence interval."""
        posterior = poisson_gamma_posterior(
            observed_cases=NPS_DATA['cold_cases_total'],
            exposure=NPS_DATA['total_visits']
        )
        
        annual_visits = NPS_DATA['annual_visits_millions'] * 1e6
        annual_expected = posterior['post_mean'] * annual_visits
        recurrence_years = 1 / annual_expected
        
        # From HTML output: about 1 disappearance every 2.0 years
        assert recurrence_years == pytest.approx(2.0, rel=0.05)


# =============================================================================
# TEST CLASS 4: Bayesian Model 2 Integration Tests
# =============================================================================

class TestBayesianModel2:
    """Integration tests for Bayesian Model 2 (posterior predictive)."""

    def test_predictive_distribution_statistics(self):
        """Test posterior predictive distribution statistics."""
        posterior = poisson_gamma_posterior(
            observed_cases=NPS_DATA['cold_cases_total'],
            exposure=NPS_DATA['total_visits']
        )
        
        np.random.seed(42)  # For reproducibility
        predictions = posterior_predictive(
            posterior,
            ALL_LANDS['total_visits_60yr'],
            n_samples=100000
        )
        
        # From HTML output
        assert np.mean(predictions) == pytest.approx(159.0, rel=0.05)
        assert np.median(predictions) == pytest.approx(157.0, rel=0.05)
        assert np.std(predictions) == pytest.approx(31.1, rel=0.10)

    def test_predictive_interval(self):
        """Test 95% predictive interval."""
        posterior = poisson_gamma_posterior(
            observed_cases=NPS_DATA['cold_cases_total'],
            exposure=NPS_DATA['total_visits']
        )
        
        np.random.seed(42)
        predictions = posterior_predictive(
            posterior,
            ALL_LANDS['total_visits_60yr'],
            n_samples=100000
        )
        
        pi_lower = np.percentile(predictions, 2.5)
        pi_upper = np.percentile(predictions, 97.5)
        
        # From HTML output: [103, 225]
        assert pi_lower == pytest.approx(103, rel=0.10)
        assert pi_upper == pytest.approx(225, rel=0.10)

    def test_exposure_scaling(self):
        """Test that predictions scale correctly with exposure."""
        posterior = poisson_gamma_posterior(
            observed_cases=NPS_DATA['cold_cases_total'],
            exposure=NPS_DATA['total_visits']
        )
        
        # NPS only (60 years)
        nps_60yr_exposure = NPS_DATA['total_visits']
        
        # ALL lands (60 years)
        all_lands_exposure = ALL_LANDS['total_visits_60yr']
        
        # Ratio of exposures
        ratio = all_lands_exposure / nps_60yr_exposure
        
        np.random.seed(42)
        pred_nps = posterior_predictive(posterior, nps_60yr_exposure, n_samples=50000)
        pred_all = posterior_predictive(posterior, all_lands_exposure, n_samples=50000)
        
        # Mean should scale approximately linearly with exposure
        actual_ratio = np.mean(pred_all) / np.mean(pred_nps)
        assert actual_ratio == pytest.approx(ratio, rel=0.10)


# =============================================================================
# TEST CLASS 5: M411 Claims Probability Tests
# =============================================================================

class TestM411ClaimsProbability:
    """Test probability calculations for M411 claims."""

    def test_probability_at_least_m411_claims(self):
        """Test calculation of P(predicted ≥ M411 claims)."""
        posterior = poisson_gamma_posterior(
            observed_cases=NPS_DATA['cold_cases_total'],
            exposure=NPS_DATA['total_visits']
        )
        
        np.random.seed(42)
        predictions = posterior_predictive(
            posterior,
            ALL_LANDS['total_visits_60yr'],
            n_samples=100000
        )
        
        p_at_least_m411 = np.mean(predictions >= M411_CLAIMS['total_cases'])
        
        # From HTML output: essentially 0.00e+00
        assert p_at_least_m411 < 1e-10
        # In practice, should be exactly 0 for this sample
        assert p_at_least_m411 == 0.0

    def test_m411_claims_multiple_of_expected(self):
        """Test that M411 claims are multiple of model expectation."""
        posterior = poisson_gamma_posterior(
            observed_cases=NPS_DATA['cold_cases_total'],
            exposure=NPS_DATA['total_visits']
        )
        
        np.random.seed(42)
        predictions = posterior_predictive(
            posterior,
            ALL_LANDS['total_visits_60yr'],
            n_samples=100000
        )
        
        ratio = M411_CLAIMS['total_cases'] / np.mean(predictions)
        
        # From HTML output: 10x higher than expected
        assert ratio == pytest.approx(10.0, rel=0.05)

    def test_m411_outside_predictive_interval(self):
        """Test that M411 claims fall far outside 95% predictive interval."""
        posterior = poisson_gamma_posterior(
            observed_cases=NPS_DATA['cold_cases_total'],
            exposure=NPS_DATA['total_visits']
        )
        
        np.random.seed(42)
        predictions = posterior_predictive(
            posterior,
            ALL_LANDS['total_visits_60yr'],
            n_samples=100000
        )
        
        pi_upper = np.percentile(predictions, 97.5)
        
        # M411 claims should be far beyond the upper 95% bound
        assert M411_CLAIMS['total_cases'] > pi_upper
        # Specifically, should be about 7x the upper bound
        assert M411_CLAIMS['total_cases'] / pi_upper > 6


# =============================================================================
# TEST CLASS 6: Statistical Properties
# =============================================================================

class TestStatisticalProperties:
    """Test that the statistical properties of the model are sound."""

    def test_gamma_distribution_properties(self):
        """Test that posterior Gamma distribution has correct properties."""
        posterior = poisson_gamma_posterior(30, 1.87e10)
        
        # Sample from the posterior
        samples = stats.gamma.rvs(
            posterior['post_alpha'],
            scale=1/posterior['post_beta'],
            size=100000,
            random_state=42
        )
        
        # Check mean
        assert np.mean(samples) == pytest.approx(posterior['post_mean'], rel=0.02)
        # Check std
        assert np.std(samples) == pytest.approx(posterior['post_sd'], rel=0.05)

    def test_credible_interval_coverage(self):
        """Test that 95% CI contains 95% of posterior samples."""
        posterior = poisson_gamma_posterior(30, 1.87e10)
        
        samples = stats.gamma.rvs(
            posterior['post_alpha'],
            scale=1/posterior['post_beta'],
            size=100000,
            random_state=42
        )
        
        ci_lower, ci_upper = posterior['ci_95']
        coverage = np.mean((samples >= ci_lower) & (samples <= ci_upper))
        
        # Should be approximately 95%
        assert coverage == pytest.approx(0.95, abs=0.01)

    def test_negative_binomial_from_compound(self):
        """Test that posterior predictive follows Negative Binomial."""
        # The compound Poisson-Gamma is analytically a Negative Binomial
        posterior = poisson_gamma_posterior(30, 1.87e10)
        exposure = 1e8
        
        np.random.seed(42)
        predictions = posterior_predictive(posterior, exposure, n_samples=100000)
        
        # Negative Binomial mean
        nb_mean = posterior['post_alpha'] / posterior['post_beta'] * exposure
        
        # Negative Binomial variance (for this parameterization)
        # Var = mean + mean²/α
        nb_var = nb_mean + (nb_mean ** 2) / posterior['post_alpha']
        
        assert np.mean(predictions) == pytest.approx(nb_mean, rel=0.05)
        assert np.var(predictions) == pytest.approx(nb_var, rel=0.10)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])

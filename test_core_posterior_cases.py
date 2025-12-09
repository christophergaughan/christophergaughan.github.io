import numpy as np
import pytest
from scipy import stats

# Import functions under test from existing module in repo
from test_bayesian_analysis import poisson_gamma_posterior, posterior_predictive


class TestCorePosteriorCases:
    """Minimal tests for core posterior and predictive functionality requested."""

    def test_posterior_parameters_conjugate_update(self):
        # Case 1: posterior parameters (alpha, beta) update correctly
        observed = 12
        exposure = 2.5e6
        prior_alpha = 3.0
        prior_beta = 4.0

        result = poisson_gamma_posterior(observed, exposure, prior_alpha, prior_beta)

        assert result['post_alpha'] == pytest.approx(prior_alpha + observed)
        assert result['post_beta'] == pytest.approx(prior_beta + exposure)

    def test_posterior_mean_and_sd(self):
        # Case 2: mean and standard deviation formulas
        result = poisson_gamma_posterior(observed_cases=20, exposure=5e6, prior_alpha=2.0, prior_beta=10.0)

        expected_mean = result['post_alpha'] / result['post_beta']
        expected_sd = np.sqrt(result['post_alpha'] / (result['post_beta'] ** 2))

        assert result['post_mean'] == pytest.approx(expected_mean)
        assert result['post_sd'] == pytest.approx(expected_sd)

    def test_posterior_credible_interval_95(self):
        # Case 3: 95% credible interval from Gamma(alpha_post, beta_post)
        observed = 7
        exposure = 1.2e5
        prior_alpha = 1.5
        prior_beta = 2.5
        res = poisson_gamma_posterior(observed, exposure, prior_alpha, prior_beta)

        a = prior_alpha + observed
        b = prior_beta + exposure
        ci_lower = stats.gamma.ppf(0.025, a, scale=1/b)
        ci_upper = stats.gamma.ppf(0.975, a, scale=1/b)

        assert res['ci_95'][0] == pytest.approx(ci_lower)
        assert res['ci_95'][1] == pytest.approx(ci_upper)
        assert res['ci_95'][0] < res['post_mean'] < res['ci_95'][1]

    def test_posterior_predictive_sample_size(self):
        # Case 4: predictive draws length equals n_samples
        post = poisson_gamma_posterior(observed_cases=15, exposure=3e6)
        n = 5000
        preds = posterior_predictive(post, exposure=1e4, n_samples=n)
        assert isinstance(preds, np.ndarray)
        assert len(preds) == n

    def test_posterior_predictive_mean_matches_rate_times_exposure(self):
        # Case 5: E[Y] ≈ E[lambda]*exposure
        post = poisson_gamma_posterior(observed_cases=25, exposure=8e6)
        exposure = 2e5
        n = 100000
        preds = posterior_predictive(post, exposure=exposure, n_samples=n)

        expected = post['post_mean'] * exposure
        actual = np.mean(preds)
        assert actual == pytest.approx(expected, rel=0.05)

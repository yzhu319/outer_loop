"""
wilson_ci.py
Wilson score confidence intervals and the gated acceptance test.
"""

import math
from dataclasses import dataclass


@dataclass
class WilsonCI:
    lower: float
    upper: float
    center: float
    n: int
    k: int  # successes

    def __repr__(self):
        return f"WilsonCI(p={self.center:.3f}, [{self.lower:.3f}, {self.upper:.3f}], n={self.n})"


def wilson_ci(k: int, n: int, alpha: float = 0.05) -> WilsonCI:
    """
    Compute the Wilson score confidence interval.

    Args:
        k: number of successes
        n: number of trials
        alpha: significance level (1-alpha is the confidence level)

    Returns:
        WilsonCI with lower/upper bounds
    """
    if n == 0:
        return WilsonCI(0.0, 1.0, 0.0, 0, 0)

    z = _z_score(1 - alpha / 2)
    p_hat = k / n
    z2 = z * z
    n_z2 = n + z2
    center = (p_hat + z2 / (2 * n)) / (1 + z2 / n)
    margin = z * math.sqrt(p_hat * (1 - p_hat) / n + z2 / (4 * n * n)) / (1 + z2 / n)
    lower = max(0.0, center - margin)
    upper = min(1.0, center + margin)
    return WilsonCI(lower=lower, upper=upper, center=center, n=n, k=k)


def gated_accept(ci_candidate: WilsonCI, ci_incumbent: WilsonCI) -> bool:
    """
    Gated acceptance test: candidate is certified better than incumbent iff
    the lower bound of candidate exceeds the upper bound of incumbent.

    This gives a false-acceptance probability <= alpha/2 (Theorem 3.3).
    """
    return ci_candidate.lower > ci_incumbent.upper


def illusion_probability(n: int, epsilon: float, q: float) -> float:
    """
    Theoretical probability of ratchet illusion (Theorem 3.1).
    P(F_hat(h') > F_hat(h)) when F(h') = q - epsilon.

    Args:
        n: number of evaluation episodes
        epsilon: true performance gap (h' is epsilon worse)
        q: baseline completion rate

    Returns:
        Illusion probability
    """
    from scipy import stats
    mean_diff = -epsilon  # h' is epsilon worse
    std_diff = math.sqrt(2 * q * (1 - q) / n)
    # P(difference > 0) = P(Z > -mean_diff/std_diff) = 1 - Phi(-mean_diff/std_diff)
    z = -mean_diff / std_diff
    return 1 - stats.norm.cdf(z)


def _z_score(p: float) -> float:
    """Inverse normal CDF (percent-point function)."""
    from scipy import stats
    return stats.norm.ppf(p)


def sample_size_for_delta(delta: float, q0: float, alpha: float = 0.05) -> int:
    """
    Minimum N such that Wilson CI half-width < delta/2 at completion rate q0.
    """
    z = _z_score(1 - alpha / 2)
    # Wilson margin ≈ z * sqrt(q(1-q)/n) / (1 + z^2/n)
    # For large n: margin ≈ z * sqrt(q(1-q)/n)
    # Set margin = delta/2 and solve for n:
    n = math.ceil((z / (delta / 2)) ** 2 * q0 * (1 - q0))
    return n


if __name__ == "__main__":
    # Quick sanity check
    ci = wilson_ci(30, 85, alpha=0.05)
    print(f"30/85: {ci}")

    ci2 = wilson_ci(45, 85, alpha=0.05)
    print(f"45/85: {ci2}")
    print(f"Gated accept (45 over 30)? {gated_accept(ci2, ci)}")

    print("\nIllusion probabilities (q=0.35, eps=0.02):")
    for n in [5, 20, 85, 200]:
        p = illusion_probability(n, 0.02, 0.35)
        print(f"  N={n:4d}: P_illusion = {p:.3f}")

    print(f"\nSample size for delta=0.15, q0=0.35: N={sample_size_for_delta(0.15, 0.35)}")

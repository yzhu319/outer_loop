"""
gated_ratchet.py
Gated ratchet evaluator: compares harness candidates against the incumbent
using Wilson confidence intervals.  Implements Algorithm 1 (GROL) evaluation step.
"""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np

from src.evaluator.wilson_ci import wilson_ci, gated_accept, WilsonCI
from src.harness.harness_config import HarnessConfig


@dataclass
class HarnessEval:
    """Result of evaluating a harness for N episodes."""
    harness: HarnessConfig
    n_episodes: int
    n_success: int
    ci: WilsonCI
    stage_completions: dict = field(default_factory=dict)  # stage_k -> (successes, total)

    @property
    def completion_rate(self) -> float:
        return self.n_success / self.n_episodes if self.n_episodes > 0 else 0.0

    def stage_rate(self, k: int) -> float:
        if k not in self.stage_completions:
            return 0.0
        s, n = self.stage_completions[k]
        return s / n if n > 0 else 0.0

    def __repr__(self):
        return (f"HarnessEval(rate={self.completion_rate:.3f}, "
                f"CI={self.ci}, n={self.n_episodes})")


class GatedRatchet:
    """
    Manages the incumbent harness and applies the gated acceptance test.
    Supports both greedy and archive modes.
    """

    def __init__(self, n_eval: int = 85, alpha: float = 0.05):
        self.n_eval = n_eval
        self.alpha = alpha
        self.incumbent: Optional[HarnessEval] = None
        self.history: list[HarnessEval] = []

    def set_incumbent(self, eval_result: HarnessEval):
        self.incumbent = eval_result
        self.history.append(eval_result)

    def test(self, candidate: HarnessEval) -> bool:
        """
        Returns True iff candidate is certified better than incumbent
        by the gated ratchet test (Theorem 3.3).
        """
        if self.incumbent is None:
            return True
        return gated_accept(candidate.ci, self.incumbent.ci)

    def accept(self, candidate: HarnessEval) -> bool:
        """Test and update incumbent if accepted."""
        accepted = self.test(candidate)
        if accepted:
            self.incumbent = candidate
        self.history.append(candidate)
        return accepted

    def naive_test(self, candidate: HarnessEval) -> bool:
        """Naive point-estimate comparison (for ablation)."""
        if self.incumbent is None:
            return True
        return candidate.completion_rate > self.incumbent.completion_rate


class ParetorArchive:
    """
    Maintains a Pareto-non-dominated set of harnesses with respect to
    stage completion rates.  Implements the archive component of GROL.
    """

    def __init__(self, max_size: int = 20):
        self.max_size = max_size
        self.entries: list[HarnessEval] = []
        self._ucb_counts: dict = {}   # harness hash -> selection count

    def _stage_vector(self, e: HarnessEval) -> tuple:
        """Returns stage completion rate vector for Pareto comparison."""
        if not e.stage_completions:
            return (e.completion_rate,)
        stages = sorted(e.stage_completions.keys())
        return tuple(e.stage_rate(k) for k in stages)

    def dominates(self, a: HarnessEval, b: HarnessEval) -> bool:
        """Returns True if a Pareto-dominates b (a better on all stages, strictly better on one)."""
        va, vb = self._stage_vector(a), self._stage_vector(b)
        if len(va) != len(vb):
            return a.completion_rate > b.completion_rate
        return all(ai >= bi for ai, bi in zip(va, vb)) and any(ai > bi for ai, bi in zip(va, vb))

    def try_add(self, candidate: HarnessEval) -> bool:
        """Add candidate if it's not dominated. Returns True if added."""
        # Remove any existing entries dominated by candidate
        dominated = [e for e in self.entries if self.dominates(candidate, e)]
        # Check if candidate is dominated by any existing entry
        if any(self.dominates(e, candidate) for e in self.entries):
            return False
        for e in dominated:
            self.entries.remove(e)
        self.entries.append(candidate)
        # Enforce max size by evicting lowest completion rate
        if len(self.entries) > self.max_size:
            self.entries.sort(key=lambda e: e.completion_rate)
            self.entries = self.entries[1:]
        return True

    def best(self) -> Optional[HarnessEval]:
        if not self.entries:
            return None
        return max(self.entries, key=lambda e: e.completion_rate)

    def ucb_select(self, t: int, c: float = 1.4) -> HarnessEval:
        """UCB1 selection from archive for parent harness."""
        if not self.entries:
            raise ValueError("Archive is empty")
        scores = []
        for e in self.entries:
            h = hash(e.harness)
            n = self._ucb_counts.get(h, 0)
            if n == 0:
                return e  # prioritize unexplored
            ucb = e.completion_rate + c * np.sqrt(np.log(t + 1) / n)
            scores.append((ucb, e))
        _, selected = max(scores, key=lambda x: x[0])
        self._ucb_counts[hash(selected.harness)] = self._ucb_counts.get(hash(selected.harness), 0) + 1
        return selected

    def summary(self) -> str:
        if not self.entries:
            return "Archive: empty"
        lines = [f"Archive ({len(self.entries)} entries):"]
        for e in sorted(self.entries, key=lambda x: -x.completion_rate):
            lines.append(f"  {e.harness.to_dict()} → {e.completion_rate:.3f}")
        return "\n".join(lines)

"""
harness_config.py
Defines the HarnessConfig dataclass and the full harness search space.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
import json
import itertools

OBS_MODALITIES  = ["screenshot", "ax_tree", "dom_text", "hybrid_ax_ss", "hybrid_dom_ss"]
ACTION_VOCABS   = ["low_level", "high_level", "mixed"]
CTX_WINDOWS     = ["last_1", "last_3", "last_5", "full_summary"]
SCAFFOLDS       = ["none", "step_counter", "error_overlay", "task_decomp", "full"]
RETRY_POLICIES  = ["none", "once", "backtrack"]


@dataclass
class HarnessConfig:
    obs_modality: str = "screenshot"
    action_vocab: str = "high_level"
    ctx_window:   str = "last_3"
    scaffold:     str = "none"
    retry_policy: str = "once"

    def __post_init__(self):
        assert self.obs_modality in OBS_MODALITIES, f"Bad obs_modality: {self.obs_modality}"
        assert self.action_vocab in ACTION_VOCABS,  f"Bad action_vocab: {self.action_vocab}"
        assert self.ctx_window   in CTX_WINDOWS,    f"Bad ctx_window: {self.ctx_window}"
        assert self.scaffold     in SCAFFOLDS,      f"Bad scaffold: {self.scaffold}"
        assert self.retry_policy in RETRY_POLICIES, f"Bad retry_policy: {self.retry_policy}"

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, d: dict) -> "HarnessConfig":
        return cls(**{k: d[k] for k in ["obs_modality", "action_vocab",
                                         "ctx_window", "scaffold", "retry_policy"]})

    @classmethod
    def from_json(cls, s: str) -> "HarnessConfig":
        return cls.from_dict(json.loads(s))

    def __hash__(self):
        return hash((self.obs_modality, self.action_vocab,
                     self.ctx_window, self.scaffold, self.retry_policy))

    def __eq__(self, other):
        return (self.obs_modality == other.obs_modality and
                self.action_vocab == other.action_vocab and
                self.ctx_window   == other.ctx_window   and
                self.scaffold     == other.scaffold     and
                self.retry_policy == other.retry_policy)


def default_harness() -> HarnessConfig:
    return HarnessConfig(
        obs_modality="screenshot",
        action_vocab="high_level",
        ctx_window="last_3",
        scaffold="none",
        retry_policy="once",
    )


def best_checkout_harness() -> HarnessConfig:
    """Best harness found by GROL for checkout tasks."""
    return HarnessConfig(
        obs_modality="hybrid_ax_ss",
        action_vocab="mixed",
        ctx_window="full_summary",
        scaffold="full",
        retry_policy="backtrack",
    )


def enumerate_all_harnesses() -> list:
    """Returns all 900 harness configurations."""
    configs = []
    for combo in itertools.product(OBS_MODALITIES, ACTION_VOCABS,
                                   CTX_WINDOWS, SCAFFOLDS, RETRY_POLICIES):
        configs.append(HarnessConfig(*combo))
    return configs


def random_harness(rng=None) -> HarnessConfig:
    import random
    r = rng or random
    return HarnessConfig(
        obs_modality=r.choice(OBS_MODALITIES),
        action_vocab=r.choice(ACTION_VOCABS),
        ctx_window=r.choice(CTX_WINDOWS),
        scaffold=r.choice(SCAFFOLDS),
        retry_policy=r.choice(RETRY_POLICIES),
    )

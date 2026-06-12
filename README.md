# outer_loop

Learning beyond gradients: theory, literature review, and experiments on the one loop
every "self-improving AI" system runs — a frozen LLM proposes edits to a text/code
artifact, a noisy evaluator scores them, a selection rule keeps something.

## Contents

| Folder | What it is |
|---|---|
| `harness-optimization-review/` | Literature review of the four core works (HL, GEPA, autoresearch, Meta-Harness). Start at `index.html`, then `lit-review.html` ("The Outer Loop"). |
| `beyond-gradients-theory/` | The theory project. `paper-iclr2027/` — **v2** "Learning Beyond Gradients: Resources, Certificates, and Limits of LLM-Guided Artifact Search" (ICLR 2027 format, addresses both referee reports; see its `response-to-reviewers.html` and README). `paper-icml2026/` — v1 (ICML format) plus the two referee reports. `one-loop-many-names.html` — the essay that seeded it. |
| `beyond-gradients-blog/` | Companion blog post "The 53% Speedup That Wasn't". Single source `post.md` → self-contained `index.html` via `build.py`; figures regenerate from `make_figures.py` (seeded). |
| `shopgym-neurips/` | ShopGym (NeurIPS, under review) — paper analysis through the harness lens, rebuttal-prep notes, and the proposed CUA harness-search experiment (`notes/harness-track-proposal.md`). |

## Reference repos (not tracked)

Third-party clones studied in `harness-optimization-review/` are gitignored. To restore:

```bash
git clone https://github.com/trinkle23897/learning-beyond-gradients harness-optimization-review/1-heuristic-learning/learning-beyond-gradients
git clone https://github.com/gepa-ai/gepa                            harness-optimization-review/2-gepa/gepa
git clone https://github.com/karpathy/autoresearch                   harness-optimization-review/3-karpathy-auto-research/autoresearch
git clone https://github.com/stanford-iris-lab/meta-harness          harness-optimization-review/4-meta-harness/meta-harness
```

## Milestones

- **m1-blog** (June 12, 2026): lit review → theory paper (ICML format, review-ready, 6/10 simulated review) → companion blog post, all built and verified.
- **m2-paper-v2** (June 12, 2026): major revision addressing both referee reports (every W/E/N/R/Q item), retargeted to ICLR 2027 in `beyond-gradients-theory/paper-iclr2027/`. New: composed certified-improvement Theorem 6.1, γ-estimability Prop 3.5 + pre-registered protocol (App I), archival evidence base, honest audit trail; body exactly 9 pp. Next: run the App I γ measurement, then the ShopGym harness-search pilot.

# Beyond-Gradients Theory — blog project

## The prompt (why this exists)

> "I feel there is something more fundamentally common among these learning-beyond-gradients works
> (Heuristic Learning, GEPA, autoresearch, Meta-Harness, SkillOpt…). Are there any theoretical works on
> computation theory / math related to this? Abstractly, do these methods share something in common?
> — that would be a great paper/blog idea." — Yuanzheng, June 11, 2026

Working hypothesis: yes — they are all **stochastic search in program/text space where the proposal
distribution is a frontier LLM conditioned on execution traces**, and the theory to explain them already
exists in five scattered literatures that haven't been introduced to each other. The field has theory
*debt*, not theory absence.

## Deliverables

- `one-loop-many-names.html` — **the blog essay** (main artifact). Four tabs: essay, theory lenses,
  conjectures (the paper-idea payload), reading list.
- `paper-icml2026/` — **the full paper** (June 12, 2026): "Learning Beyond Gradients: A Unifying
  Theory of LLM-Guided Artifact Search." ICML 2026 format, review-ready: 8-page body (ends p. 7),
  6 theorem groups with complete appendix proofs (C1–C5 proved; C6 stated as formal open problem),
  3 seeded simulations (`paper-icml2026/code/`), vendored style files, compiles clean. See its README
  for the submission-requirements checklist and theorem-to-evidence map.
- `notes/research-notes.md` — research base: each theory area, key works, links, and how it maps onto
  the empirical works.
- Companion empirical review: `../harness-optimization-review/` (kept separate; ShopGym effort separate
  again in `../shopgym-neurips/`).

## The five theory lenses (summary)

1. **Universal search & learned priors** — Levin (1973), Solomonoff, Schmidhuber's OOPS/adaptive Levin
   search; modern: "AI Agents as Universal Task Solvers" (Amazon AGI, 2025), "LLM Priors for ERM over
   Programs" (2025). Levin's bound: search time ∝ t(p)/P(p) — *sample efficiency is prior mass*. LLM
   pretraining = learning the prior; trace conditioning = adaptive Levin search.
2. **Feedback as information** — "Provably Learning from Language Feedback" (2025): transfer eluder
   dimension; exponential separation between scalar-reward and language-feedback learning. Formalizes
   "GEPA beats GRPO with 35x fewer rollouts."
3. **Selection under noise & diversity** — best-arm identification / racing / successive halving (why
   noisy 5-minute evals demand repeats); quality-diversity theory (novelty search, MAP-Elites) behind
   GEPA's Pareto frontier, ADAS's archive, DGM's lineages.
4. **The artifact as compression** — MDL / PAC-Bayes view: the evolved prompt/skill/harness is a
   compressed posterior over the task distribution; HL's "compress history" and ACE's "context collapse"
   are description-length management, success and failure mode respectively. ICL theory (implicit
   Bayesian inference; in-context gradient descent) supplies the inner mechanism.
5. **Limits** — No Free Lunch (gains = prior–task alignment); Goodhart taxonomy (Manheim & Garrabrant);
   RSI limits (Yampolskiy, Chalmers); "Reward is Enough" (Silver et al.) as the counterpoint to lens 2.

## Status

- [x] Research pass (June 11, 2026)
- [x] Essay draft v1
- [x] Full theory paper draft, ICML format (`paper-icml2026/`, June 12, 2026)
- [ ] External feedback round (paper is review-ready)
- [ ] Pick deadline: ICLR 2027 (~Sept 2026, nearest) vs. ICML 2027 (~Jan 2027; swap in new style files when released)

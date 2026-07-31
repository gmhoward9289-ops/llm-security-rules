# Positioning

Why this ruleset exists, whether it can be differentiated, and what would
make people actually use it. Landscape surveyed 2026-07-30.

## The landscape

- **[Semgrep's own `skills` repo](https://github.com/semgrep/skills)** — guidance
  documents for AI coding agents based on OWASP LLM Top 10, largely
  transformed from existing generic rules. Not a tested, LLM-specific
  ruleset. The Semgrep registry's LLM-specific coverage is thin.
- **[agent-audit](https://github.com/HeadyZhang/agent-audit)** — the strongest
  adjacent project: 72 rules, OWASP *Agentic* Top 10 mapping, real
  benchmarks (73.6% precision). But it is a **separate tool with a custom
  engine, Python-only**.
- **[Trail of Bits semgrep-rules](https://github.com/trailofbits/semgrep-rules)** —
  excellent ML rules, but scoped to model loading (pickle/torch), nothing
  for prompt handling, LLM APIs, or model-output sinks.
- **Inkog, AgentShield** — agent/MCP *configuration* scanners, commercial or
  config-focused; not source-level SAST for app code.
- **Runtime tools (LLM Guard, Rebuff, garak, NeMo Guardrails)** — different
  layer entirely: they filter traffic or probe deployed systems. None stops
  a hardcoded key or an `eval(response)` from being merged.

## Differentiation — what this repo has that nothing above has

1. **Zero-adoption-cost.** This is not a tool, it's a config. Semgrep is
   already in thousands of CI pipelines; consuming this repo is one
   `--config` argument, one Action line, or one pre-commit stanza. Rules
   travel further than tools.
2. **TypeScript/JavaScript coverage.** The Node LLM stack (OpenAI/Anthropic
   Node SDKs, Vercel AI SDK, React chat UIs) is where a huge share of LLM
   apps get built — and where none of the adjacent projects look.
   agent-audit is Python-only; ToB has no LLM rules at all. This is the
   clearest open gap.
3. **The tested-fixture contract.** Every rule proves its pass *and* fail
   cases in CI. Most community rulesets assert; this one demonstrates.
   That's also the credibility wedge for registry submission.
4. **Taint mode now, not "roadmap."** Model output and request data are
   tracked through assignments and destructuring to sinks. Pattern-only
   rules are dodged by a single variable rename; these aren't.
5. **OWASP LLM Top 10 (2025) mapping in every rule's metadata.** Security
   teams buying/approving tools ask "what framework does this map to."
   The answer is in the finding itself.
6. **Agent-skill distribution.** AI agents write much of today's LLM app
   code. Packaging the ruleset as a skill puts the check at the point of
   generation, not just review. None of the adjacent projects do this.

## Honest risks — why it might not get used

- **Semgrep could ship an official LLM pack.** They know the space (their
  skills repo proves it). Mitigation: be first with the tested TS/JS
  coverage, and treat registry submission as a win (rules get attribution
  and reach) rather than competition.
- **"Nobody scans for this yet"** — the category is young; most teams don't
  know they need LLM-specific SAST. Mitigation: the secrets rules deliver
  immediate, undeniable value (leaked provider keys cost real money within
  hours), and they pull the rest of the ruleset in with them.
- **Precision decay as coverage grows.** The temptation to add fuzzy rules
  (e.g. "user input near a prompt") would wreck trust. The precision
  contract in the README is the guardrail: fuzzy heuristics stay out.
- **Maintenance surface.** SDKs churn (OpenAI's API shapes changed twice in
  two years). The fixture suite makes churn visible: when a pattern rots,
  its test still passes but real-world hits drop — so the roadmap's
  benchmark corpus matters.

## What "valuable enough to use" means concretely

The adoption ladder, in order of effort:

1. **Publish public + submit 2–3 best rules to the Semgrep registry**
   (`hardcoded-api-key-in-llm-client`, `exec-of-llm-output`,
   `dangerously-set-llm-html`). Registry inclusion = discovery inside the
   tool people already run, with a backlink.
2. **Write the launch post** ("Your LLM app has the same 5 bugs everyone
   else's does — here's a semgrep config that catches them") for
   blog.swamplink.com, with real before/after snippets from the fixtures.
3. **Scan popular open-source LLM apps** and file the true-positive
   findings as issues (with the fix). Each accepted issue is both a
   precision datapoint and organic marketing.
4. **Marketplace listing for the GitHub Action** once the repo is public.

If after those steps the repo gets no traction, the fallback value is still
real: it's a working security gate for our own LLM projects and a
demonstration artifact of rule-engineering competence.

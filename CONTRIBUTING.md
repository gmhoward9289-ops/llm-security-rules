# Contributing

Rules, fixtures, and framework coverage are all welcome. Read the bar below
before writing one — most rejected rules are rejected on precision, not on
craft.

Security issues (missed detections, evasions, tooling bugs) go through
[SECURITY.md](SECURITY.md), not the public issue tracker.

## The bar

**Precision over recall.** From the README: a rule that cries wolf gets the
whole ruleset uninstalled. Concretely, a rule belongs here when a match is
near-certainly a defect — the reader should reach for a fix, not for
`nosemgrep`.

Expect pushback on:

- **Proximity and naming heuristics.** "User input appears near a prompt
  string." "A variable called `prompt` is concatenated." Near-misses, not
  defects.
- **Pattern-only rules where taint mode is available.** If the defect is
  data reaching a sink, track it. A pattern-only rule is dodged by one
  variable rename.
- **Strawman `ok:` cases.** Five `ruleid:` lines and one throwaway safe case
  does not demonstrate precision.
- **LLM08 and LLM10 as currently framed.** The README roadmap keeps vector/
  embedding weaknesses and unbounded consumption out because nobody has
  expressed them as precise static patterns. A PR that genuinely does is
  very welcome; one that approximates them isn't.

If you think a rule is right but can't get the precision, open an issue
before the PR. Discussing it beats landing a noisy rule.

## Setup

```bash
pip install semgrep
./run-tests.sh        # wraps: semgrep --test rules/
```

## Adding a rule

**1. Pick the directory.** Rules live at
`rules/<owasp-category>/<language>/<name>.yaml`:

```
rules/llm01-prompt-injection/{python,typescript}/
rules/llm02-sensitive-info/{python,typescript,go}/
rules/llm03-supply-chain/python/
rules/llm05-output-handling/{python,typescript,go}/
rules/llm06-excessive-agency/{python,typescript}/
rules/llm07-system-prompt-leakage/python/
rules/secrets/                 # regex rules, no language subdirectory
```

A new OWASP category gets a new directory named `llmNN-<slug>`.

**2. Write `<name>.yaml`.** One file may hold several rules when they share
a threat model and a fixture — `llm05-output-handling/python/exec-of-llm-output.yaml`
holds three.

**3. Keep rule ids globally unique.** They collide across the whole ruleset,
so language variants take a suffix: Python holds the bare id, TypeScript
adds `-js`, Go adds `-go`. Hence `exec-of-llm-output`,
`eval-of-llm-output-js`, `shell-from-llm-output-go`.

**4. Fill in the metadata block.** All of it:

```yaml
metadata:
  category: security
  subcategory: [code-injection]
  owasp-llm: "LLM05:2025 Improper Output Handling"
  cwe: "CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code"
  confidence: HIGH
  references:
    - https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/
```

The `owasp-llm` mapping is not decoration — it lands in the finding, and it
is what security teams filter on.

**5. Write the message like the fix matters.** What is wrong, why it's wrong
specifically in an LLM context, and what to do instead. Two to four
sentences, ending in an imperative. Copy the register from an existing rule.

## The fixture

**Every rule needs a fixture, and every fixture needs both directions.**
This is the repo's whole credibility claim: rules here demonstrate rather
than assert.

The fixture is a sibling file with the same basename and the language
extension — `foo.yaml` → `foo.py` / `foo.ts` / `foo.tsx` / `foo.go`. For
each rule id in the yaml it must contain at least one of each:

```python
# ruleid: dangerous-sink-in-tool
return str(eval(code))

# ok: dangerous-sink-in-tool
return subprocess.check_output(["ls", "-la"]).decode()
```

The annotation goes on the line above the match, in the language's comment
syntax (`//` for TypeScript and Go).

Two things that decide whether a fixture is worth anything:

- **The `ok:` cases carry the weight.** Make them the near-misses a sloppier
  rule would trip on: the safe call shape from the same SDK, the same sink
  reached from a source that isn't model output, the function without the
  decorator.
- **Fixtures must be realistic and must parse.** Real imports, real SDK call
  shapes. If semgrep can't parse the file, `ok:` lines pass for the wrong
  reason and the suite goes green over a dead rule.

If a fixture has to contain credential-shaped strings, use fake
non-functional values and add the path **by name** to
`.github/secret_scanning.yml` — that file uses explicit paths, not globs, so
new fixtures don't silently inherit the exemption.

## Before you open the PR

- [ ] Rule and sibling fixture, with `ruleid:` **and** `ok:` lines for every
      rule id in the file
- [ ] `./run-tests.sh` passes
- [ ] `semgrep --validate --config rules/` is clean
- [ ] Metadata complete: `owasp-llm`, `cwe`, `confidence`, `references`
- [ ] README coverage table updated
- [ ] Any credential-shaped fixture string is fake and the file is listed in
      `.github/secret_scanning.yml`

CI (`.github/workflows/test.yml`) runs validate plus the full suite on every
pull request. It has to be green.

## Other contributions

Bug reports, false positives, and framework requests go in public issues.
Include the code, the rule id, and the SDK version — a false positive report
that arrives as a proposed `ok:` fixture line is the ideal shape.

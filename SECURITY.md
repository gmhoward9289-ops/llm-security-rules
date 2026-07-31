# Security policy

This repo ships static-analysis rules, not a running service. The security
bugs that matter here are the ones that make the rules lie: a rule that
silently stops firing, or tooling that executes something it shouldn't on a
consumer's runner.

A rule that doesn't fire is worse than no rule. CI is green, the badge is
green, and nobody is looking at the code the rule was supposed to be
watching. Treat a missed detection as the flagship bug class of this repo,
not a coverage gap.

## Reporting

Use GitHub's private vulnerability reporting — **Security → Report a
vulnerability** on
[gmhoward9289-ops/llm-security-rules](https://github.com/gmhoward9289-ops/llm-security-rules/security/advisories/new).
If that is unavailable to you, email **dev@swamplink.com**.

**Do not open a public issue for a missed detection or an evasion.** A
working bypass posted publicly is a how-to-evade guide for everyone still
running the last tag. It goes public in the release notes once the fixed
rule is out.

False positives are not sensitive — those go in a normal public issue.

Include:

- the rule id, and the fixed tag or commit you ran
- the code that should have matched and didn't (or matched and shouldn't)
- language, SDK/framework, and version
- your semgrep version

A minimal reproducer in the shape of a fixture (`ruleid:` / `ok:` lines) is
the fastest possible report — it drops straight into the test suite.

## Response

One maintainer, no contractual SLA. The intent:

- **Acknowledgment** — 5 business days.
- **Assessment and a severity call** — 14 days.
- **Fix, a fixture proving it, and a tag** — usually days for a detection
  gap in an existing rule; longer if the fix needs a new taint source or a
  semgrep capability that isn't there yet.

Credit in the release notes unless you'd rather not have it.

## Scope

**In scope:**

- **Detection gaps.** Code inside a rule's documented threat model — what
  its `message` and `owasp-llm` metadata claim it covers — that the rule
  does not flag.
- **Trivial evasions.** A rewrite that preserves the defect and dodges the
  match: a variable rename or destructuring hop the taint rules should have
  followed, an aliased import, a different call shape from the same SDK.
- **Distribution tooling.** `action.yml`, `scripts/precommit-scan.sh`,
  `run-tests.sh`, `.github/workflows/`, and `skills/llm-security-scan/`.
  Anything that lets input control what gets executed on a consumer's CI
  runner or a developer's machine, or that makes a scan exit 0 while
  findings are suppressed.
- **Fixtures that don't test what they claim.** An `ok:` line that passes
  because semgrep couldn't parse the file, not because the pattern is
  correctly narrow. Green tests hiding a dead rule are a detection gap with
  extra steps.

**Out of scope:**

- **The vulnerabilities the rules scan for.** `eval(model_output)` in your
  application is your application's bug; this repo only points at it. Report
  it to the project that owns the code.
- **False positives.** A rule firing on safe code is a real bug and we want
  it — precision is the whole contract — but it is not a security report.
  Open a public issue.
- **The fixture files.** Every source file sitting next to a `.yaml` under
  `rules/` is deliberately vulnerable code, and
  `rules/secrets/provider-api-keys.py` deliberately contains
  provider-key-shaped strings. They are fake and non-functional;
  `.github/secret_scanning.yml` exempts that file by name. Not a leak.
- **Semgrep itself.** Engine bugs, taint-analysis limits, and CLI
  vulnerabilities go to
  [Semgrep](https://github.com/semgrep/semgrep/security). If a semgrep
  limitation is what causes a gap here, do tell us anyway — we may be able
  to write around it.
- **Categories, languages, or frameworks never claimed.** LLM04, LLM08,
  LLM09, and LLM10 have no rules; the README roadmap explains why LLM08 and
  LLM10 stay out. Missing coverage is a feature request, not a
  vulnerability.

## Supported versions

Only the latest tag. Fixes land on `main` and ship in the next tag.

This matters more than usual here because consumers pin: `@v0.2.0` in a
workflow, `rev:` in a pre-commit config. **A fix on `main` does not reach a
pinned consumer until they bump.** Release notes call out security fixes
explicitly, including what an older pin fails to catch — bump on those.

## Disclosure

Coordinated. Hold public detail until a fixed tag ships or 90 days from your
report, whichever comes first.

# Changelog

All notable changes to `llm-security-rules` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

**Why this file matters for a ruleset.** Consumers pin a tag or a ref, so a
change to the rule inventory silently changes their scan results and their CI
gate: a new rule can start failing a build that passed yesterday, and a retuned
one can change what a build was relying on. Rule-inventory changes are therefore
listed at rule granularity — rule id, language, OWASP category.

Two kinds of entry follow [SECURITY.md](SECURITY.md)'s disclosure policy:

- **A rule that stopped firing, or a working evasion**, is the flagship bug class
  here — a green badge over unwatched code. Per policy these are disclosed in the
  notes for the release that *contains the fix*, and never before it, since a
  bypass published early is a how-to-evade guide for everyone still on the last
  tag. New rules are described as coverage this version adds, not as coverage
  earlier versions lacked, for the same reason.
- **Vulnerabilities in code this project ships and you execute** — the composite
  GitHub Action, the pre-commit hook, the scan scripts — are disclosed plainly
  and immediately, because you need them to decide whether to upgrade.

False positives are not sensitive and are logged as ordinary `Fixed` entries.

## [Unreleased]

### Security

- **Script injection in the composite GitHub Action.** `action.yml` interpolated
  `inputs.paths` and `inputs.semgrep-version` directly into `run:` blocks.
  GitHub expands `${{ }}` textually before bash sees the script, so shell
  metacharacters in either input become shell syntax — a `paths` value wired to
  a PR title or branch name in a `pull_request_target` workflow yields arbitrary
  command execution on the runner, with whatever secrets that job has in scope.
  Both inputs now route through `env:`, which passes them as data. **Upgrade if
  you consume the Action; a pre-fix ref keeps the issue.**
- **`precommit-scan.sh` passes `--` before `"$@"`**, so a filename beginning with
  `-` can no longer be parsed as a `semgrep` option.
- **The composite Action pins its semgrep install** (`semgrep-version` now
  defaults to `1.172.0` instead of whatever PyPI currently serves). An empty
  version still opts out, loudly. CI's own third-party actions are pinned to
  commit SHAs for the same reason: a tag is mutable.
- **CI enforces the expression-injection fix.** A `workflow-lint` job runs
  `scripts/check-workflow-injection.sh` (fails on any GitHub expression
  interpolated into a `run:` block outside a short allowlist) plus a
  digest-pinned actionlint. The bug class above shipped once; this is what
  makes it not ship twice.

### Added

- **`SECURITY.md`** — disclosure policy, scoped to a ruleset: what counts as a
  vulnerability in rule content (a rule that can be made to execute something,
  or that leaks scanned source) versus a coverage request.
- **`CONTRIBUTING.md`** — the rule and fixture convention, and the precision bar
  a proposed rule has to clear.
- **`.gitleaks.toml`** — allowlists the secrets rule's fixture file by exact
  path, so a credential scanner run against this repo reports clean instead of
  flagging the fake keys the ruleset is tested with.

### Changed

- CI picks its runner from repository visibility: the self-hosted `swamplink`
  runner while private, GitHub-hosted while public — where a fork PR must
  never reach self-hosted hardware.
- README's GitHub Action example references a real tag.

## [0.2.0] - 2026-07-31

Initial tagged ruleset. Semgrep rules for LLM application security, mapped to
the [OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/), for
Python, TypeScript/JavaScript and Go.

Every rule ships with pass/fail fixtures and runs in CI: if a rule is in the
repo, there is a test proving both what it catches and what it deliberately
ignores. Precision is the stated bar — a rule that cries wolf gets the whole
ruleset uninstalled, so fuzzier heuristics stay out until they can be made
precise.

### Added

**LLM01 — Prompt injection**

- `request-data-in-system-prompt` — Python, TypeScript

**LLM02 — Sensitive information disclosure**

- `hardcoded-api-key-in-client` — Python, TypeScript, Go

**LLM03 — Supply chain**

- `trust-remote-code` — Python

**LLM05 — Improper output handling**

- `exec-of-llm-output` — Python, TypeScript, Go
- `dangerously-set-llm-html` — TypeScript

**LLM06 — Excessive agency**

- `dangerous-sink-in-tool` — Python, TypeScript

**LLM07 — System prompt leakage**

- `system-prompt-leakage` — Python

**Secrets**

- `provider-api-keys`

**SDK and framework coverage** — the OpenAI and Anthropic SDKs across all three
languages (including the Responses API sink), the Vercel AI SDK, LangChain,
CrewAI, FastMCP, Google GenAI, LlamaIndex, and React rendering of model output.

**Distribution surfaces** — scan directly from the ruleset URL, a composite
GitHub Action, a pre-commit hook (`.pre-commit-hooks.yaml`), and an agent skill
(`skills/llm-security-scan/`).

### Changed

- `google-ai-api-key-literal` renamed to `google-api-key-literal`, and its
  severity set to what the finding actually supports.
- Fixture rigor pass, and a push-protection exemption
  (`.github/secret_scanning.yml`) so the deliberately-fake credentials in the
  secrets fixtures do not trip GitHub's scanner.

[Unreleased]: https://github.com/gmhoward9289-ops/llm-security-rules/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/gmhoward9289-ops/llm-security-rules/releases/tag/v0.2.0

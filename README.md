# llm-security-rules

Tested [Semgrep](https://semgrep.dev) rules for LLM application security,
mapped to the [OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/).

**Python and TypeScript/JavaScript.** Covers the OpenAI and Anthropic SDKs,
the Vercel AI SDK, LangChain, and React rendering of model output.

**Every rule ships with pass/fail fixtures and runs in CI.** If a rule is in
this repo, it has a test proving what it catches and what it deliberately
ignores.

**Precision over recall.** A rule that cries wolf gets the whole ruleset
uninstalled. Rules here fire on patterns that are near-certainly defects;
fuzzier heuristics stay out until they can be made precise.

## Quickstart

Scan a project with the ruleset directly:

```bash
semgrep scan --config https://github.com/OWNER/llm-security-rules/archive/refs/heads/main.tar.gz .
```

or clone and point at `rules/`:

```bash
semgrep scan --config path/to/llm-security-rules/rules .
```

### GitHub Action

```yaml
jobs:
  llm-security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: OWNER/llm-security-rules@v1
```

### pre-commit

```yaml
repos:
  - repo: https://github.com/OWNER/llm-security-rules
    rev: v0.2.0
    hooks:
      - id: llm-security-rules
```

### AI coding agents

`skills/llm-security-scan/` packages the ruleset as an agent skill: copy it
into your project's `.claude/skills/` and Claude Code will scan LLM-related
code it writes or reviews. AI agents generate a large share of new LLM
application code — this puts the check where the code comes from.

## Coverage

| Rule | OWASP LLM (2025) | Languages | Mode |
|---|---|---|---|
| `request-data-in-system-prompt` | LLM01 Prompt Injection | py, ts/js | taint |
| `hardcoded-api-key-in-llm-client` | LLM02 Sensitive Info Disclosure | py, ts/js | pattern |
| provider key literals (OpenAI, Anthropic, Google AI, Hugging Face, OpenRouter, Groq) | LLM02 | any file | regex |
| `exec-of-llm-output` / `eval-of-llm-output-js` | LLM05 Improper Output Handling | py, ts/js | taint |
| `shell-from-llm-output` | LLM05 | py, ts/js | taint |
| `sql-from-llm-output` | LLM05 | py | taint |
| `dangerously-set-llm-html` | LLM05 | ts/js (React) | taint |
| `dangerous-sink-in-tool` | LLM06 Excessive Agency | py | taint |
| `credentials-in-system-prompt` | LLM07 System Prompt Leakage | py | pattern |
| `system-prompt-in-logs` | LLM07 | py | pattern |

Taint-mode rules track model output (OpenAI `choices[].message.content` /
`output_text`, Anthropic `content[].text`, Vercel `generateText(...)`,
Google GenAI `generate_content(...).text` / `response.text()`, LangChain
`invoke(...).content`, LlamaIndex `query(...).response`), HTTP request
data, or agent-tool arguments through assignments and destructuring to
dangerous sinks, so renaming a variable doesn't dodge the rule.

## Running the tests

```bash
./run-tests.sh        # wraps: semgrep --test rules/
```

Every rule file `foo.yaml` has a sibling fixture (`foo.py` / `foo.ts` /
`foo.tsx`) with `ruleid:` lines that must match and `ok:` lines that must
not. CI runs `semgrep --validate` plus the full suite on every PR.

## Roadmap

- **Full OWASP LLM Top 10 coverage** — LLM03 supply chain
  (`trust_remote_code`, unpinned model refs), LLM08 vector/embedding
  weaknesses, LLM10 unbounded consumption.
- **Framework breadth** — CrewAI, AutoGen, Spring AI (Java), more
  LangChain/LlamaIndex surface, TS coverage for the tool-use rules.
- **Runtime companion** — a documented promptfoo/garak CI stage for the
  dynamic prompt-injection testing static rules can't do.
- **Benchmarked precision** — a labeled corpus of real-world LLM app code
  with published precision/recall per rule.

See [POSITIONING.md](POSITIONING.md) for why this exists and where it fits
among adjacent tools.

## License

MIT

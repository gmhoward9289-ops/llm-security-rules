# Your LLM app has the same five bugs as everyone else's

*Draft for blog.swamplink.com — publish alongside the repo going public.*

I've been reviewing LLM application code — mine and other people's — and the
same five defects show up in almost every codebase, regardless of language
or framework:

1. An API key hardcoded in the client constructor, "just for now."
2. Model output passed to `eval`, `exec`, or a shell, because the demo
   worked and the demo shipped.
3. Model output rendered as HTML, unsanitized, straight into the DOM.
4. User-controlled text interpolated into the *system* prompt.
5. An agent tool whose implementation is "run whatever string the model
   hands me."

None of these are exotic. All of them are the old vulnerabilities — command
injection, XSS, hardcoded credentials — wearing a new SDK. What's changed
is the threat model: **model output is attacker-influenced input.** Anyone
who can get text into your model's context — a prompt, a retrieved
document, a poisoned webpage — has a say in what comes out. If what comes
out reaches a shell, your attacker has a shell.

## A config, not a tool

So I built [llm-security-rules](https://github.com/gmhoward9289-ops/llm-security-rules):
a tested semgrep ruleset for exactly these defects, mapped to the OWASP LLM
Top 10 (2025), for Python, TypeScript/JavaScript, and Go.

There are good adjacent projects. agent-audit is a real scanner with real
benchmarks — but it's a separate tool with a custom engine, and it's
Python-only. Semgrep's own LLM material is guidance for AI coding agents,
not a tested ruleset. And nobody covers the TypeScript side, where a huge
share of LLM apps actually get written (Vercel AI SDK, Node SDKs, React
chat UIs).

This is deliberately not a tool. If semgrep already runs in your CI, this
is one line:

```bash
semgrep scan --config https://github.com/gmhoward9289-ops/llm-security-rules/archive/refs/heads/main.tar.gz .
```

There's a GitHub Action, a pre-commit hook, and — because a lot of LLM app
code is now written *by* AI agents — a Claude Code skill that makes the
agent scan its own output before it commits.

## What "tested" means here

Every rule ships with fixtures that pin both directions: code that must
fire, and near-misses that must not. The near-misses are where rulesets
earn trust. A masked key like `sk-proj-****T3BlbkFJ****` must not fire. A
key leaked in a *comment* must fire. A too-short `sk-ant-` stub must not.
CI runs `semgrep --validate` plus the full fixture suite on every PR — if a
rule is in the repo, there's a machine-checked proof of what it catches and
what it deliberately ignores.

Taint mode does the heavy lifting where it matters: model output is tracked
through assignments and destructuring, so renaming a variable doesn't dodge
the rule:

```ts
const { text } = await generateText({ model: "openai/gpt-4o", prompt });
exec(text);                    // caught — taint flows through destructuring
```

```python
@tool
def run_python(code: str) -> str:
    return str(eval(code))     # caught — tool args are model-chosen
```

## The two lessons the rules taught me

**Precision claims die on contact with real code.** The first field test
scanned a real non-LLM TypeScript codebase. One finding: a "Gemini API key"
— which was actually a Firebase web client key. Same `AIza` prefix, and
Firebase web keys are *designed to ship publicly*. The rule now says what
it can actually know ("Google API key — check what it's enabled for"),
fires as WARNING, and that exact near-miss is a fixture. If your secrets
rule can't tell you its own known false positive, it's not done.

**A secrets ruleset trips over itself.** The fixture file contains
key-shaped strings — necessarily, that's what the rules detect — which
means GitHub's push protection blocks the repo's own first push. The fix
(`.github/secret_scanning.yml` naming exactly that file) has to exist
*before* the first push, because afterward the blobs are already in the
remote's history. File that one under "problems you only meet once."

## What's next

Full Top-10 coverage where it can be made precise (LLM08 and LLM10 stay
out until they can be — fuzzy heuristics get rulesets uninstalled),
AutoGen and Spring AI shapes, and a benchmarked precision corpus. The
2–3 strongest rules are headed for the semgrep registry.

MIT licensed. If you ship LLM code, point semgrep at it and tell me what
it gets wrong: real false-positive reports are the most valuable
contribution a ruleset can receive.

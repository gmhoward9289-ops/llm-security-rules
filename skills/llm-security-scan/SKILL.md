---
name: llm-security-scan
description: >-
  Scan code that builds prompts, calls LLM APIs (OpenAI, Anthropic, Vercel AI
  SDK, LangChain), or handles model output for security issues mapped to the
  OWASP LLM Top 10. Use after writing or modifying LLM application code,
  before committing it, or when asked to review LLM/agent code for security.
---

# LLM security scan

Run the llm-security-rules semgrep ruleset over the files you just wrote or
were asked to review.

## When to run

- You wrote or edited code that constructs prompts, calls an LLM SDK, or
  consumes model output (Python or TypeScript/JavaScript).
- The user asks for a security review of LLM or agent code.
- Before committing generated code that touches `openai`, `anthropic`,
  `ai` (Vercel), or `langchain` imports.

## How to run

From the directory containing this skill, the ruleset lives at
`../../rules`. Scan specific files (fast, preferred) or a directory:

```bash
semgrep scan --config <path-to-llm-security-rules>/rules <changed files>
```

If semgrep is not installed: `pip install semgrep`.

## How to act on findings

- Findings are precision-tuned: treat each as a real defect, not noise.
  Fix the code rather than adding an ignore comment.
- `hardcoded-api-key-*`: move the key to an environment variable, then tell
  the user the committed key must be rotated — deleting it from the code
  does not un-leak it.
- `*-of-llm-output` / `dangerously-set-llm-html`: model output is
  attacker-influenced input. Route it through validation, sandboxing, or
  sanitization (DOMPurify for HTML) before any dangerous sink.
- `request-data-in-system-prompt*`: move user-controlled text into a
  user-role message; keep system prompts static.
- `credentials-in-system-prompt` / `system-prompt-in-logs`: remove the
  secret or the log line; system prompts must be treated as public.
- Only suppress a finding with `# nosemgrep: <rule-id>` when the user
  explicitly confirms it is a false positive, and say why in a comment.

# Test fixtures for provider-api-keys rules. All keys are fake.
import os

# --- openai-api-key-literal ---

# ruleid: openai-api-key-literal
OPENAI_KEY = "sk-proj-abcDEF123456ghiJKL789T3BlbkFJmnoPQR345stuVWX67890"

# ruleid: openai-api-key-literal
legacy = "sk-abcdefghijklmnopqrstuvwxyzABCDEF1234567890123456"

# ok: openai-api-key-literal
openai_env = os.environ["OPENAI_API_KEY"]

# ok: openai-api-key-literal
short_sk = "sk-test123"

# Masked keys (as printed by CLIs and log scrubbers) must not fire:
# ok: openai-api-key-literal
masked = "sk-proj-****T3BlbkFJ****"

# Rules are languages: [regex], so keys leaked in comments still fire:
# ruleid: openai-api-key-literal
# TODO remove before commit: sk-abcdefghijklmnopqrstuvwxyzABCDEF1234567890123456

# --- anthropic-api-key-literal ---

# ruleid: anthropic-api-key-literal
ANTHROPIC_KEY = "sk-ant-api03-AbCdEfGhIjKlMnOpQrStUvWxYz0123456789_-AbCd"

# ok: anthropic-api-key-literal
anthropic_env = os.getenv("ANTHROPIC_API_KEY")

# Too short after the prefix — must not fire:
# ok: anthropic-api-key-literal
anthropic_stub = "sk-ant-api03-tooShort"

# --- google-api-key-literal ---

# ruleid: google-api-key-literal
GEMINI_KEY = "AIzaSyA1bC2dE3fG4hI5jK6lM7nO8pQ9rS0tUvW"

# Firebase web client keys share the AIza shape and are designed to ship
# publicly — the rule still fires (same bytes), which is why it is WARNING
# severity with triage guidance instead of ERROR:
# ruleid: google-api-key-literal
FIREBASE_WEB_KEY = "AIzaSyB9xY8wV7uT6sR5qP4oN3mL2kJ1iH0gFeD"

# ok: google-api-key-literal
prefix_only = "AIza"

# --- huggingface-token-literal ---

# ruleid: huggingface-token-literal
HF_TOKEN = "hf_AbCdEfGhIjKlMnOpQrStUvWxYz01234567"

# ok: huggingface-token-literal
hf_env = os.environ.get("HF_TOKEN")

# 30 chars after hf_ (needs 34+) — must not fire:
# ok: huggingface-token-literal
hf_stub = "hf_AbCdEfGhIjKlMnOpQrStUvWxYz0123"

# --- openrouter-api-key-literal ---

# ruleid: openrouter-api-key-literal
OPENROUTER_KEY = "sk-or-v1-0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

# Uppercase hex is not the OpenRouter alphabet — must not fire:
# ok: openrouter-api-key-literal
openrouter_stub = "sk-or-v1-0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF"

# --- groq-api-key-literal ---

# ruleid: groq-api-key-literal
GROQ_KEY = "gsk_AbCdEfGhIjKlMnOpQrStUvWxYz0123456789AbCdEfGhIjKlMnOp"

# ok: groq-api-key-literal
groq_env = os.environ["GROQ_API_KEY"]

# 50 chars after gsk_ (needs 52) — must not fire:
# ok: groq-api-key-literal
groq_stub = "gsk_AbCdEfGhIjKlMnOpQrStUvWxYz0123456789AbCdEfGhIjKlMn"

# Test fixtures for provider-api-keys rules. All keys are fake.

# --- openai-api-key-literal ---

# ruleid: openai-api-key-literal
OPENAI_KEY = "sk-proj-abcDEF123456ghiJKL789T3BlbkFJmnoPQR345stuVWX67890"

# ruleid: openai-api-key-literal
legacy = "sk-abcdefghijklmnopqrstuvwxyzABCDEF1234567890123456"

# ok: openai-api-key-literal
openai_env = os.environ["OPENAI_API_KEY"]

# ok: openai-api-key-literal
short_sk = "sk-test123"

# --- anthropic-api-key-literal ---

# ruleid: anthropic-api-key-literal
ANTHROPIC_KEY = "sk-ant-api03-AbCdEfGhIjKlMnOpQrStUvWxYz0123456789_-AbCd"

# ok: anthropic-api-key-literal
anthropic_env = os.getenv("ANTHROPIC_API_KEY")

# --- google-api-key-literal ---

# ruleid: google-api-key-literal
GEMINI_KEY = "AIzaSyA1bC2dE3fG4hI5jK6lM7nO8pQ9rS0tUvW"

# ok: google-api-key-literal
prefix_only = "AIza"

# --- huggingface-token-literal ---

# ruleid: huggingface-token-literal
HF_TOKEN = "hf_AbCdEfGhIjKlMnOpQrStUvWxYz01234567"

# ok: huggingface-token-literal
hf_env = os.environ.get("HF_TOKEN")

# --- openrouter-api-key-literal ---

# ruleid: openrouter-api-key-literal
OPENROUTER_KEY = "sk-or-v1-0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

# --- groq-api-key-literal ---

# ruleid: groq-api-key-literal
GROQ_KEY = "gsk_AbCdEfGhIjKlMnOpQrStUvWxYz0123456789AbCdEfGhIjKlMnOp"

# ok: groq-api-key-literal
groq_env = os.environ["GROQ_API_KEY"]

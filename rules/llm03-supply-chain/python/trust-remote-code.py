from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# ruleid: trust-remote-code-enabled
model = AutoModelForCausalLM.from_pretrained("someorg/some-model", trust_remote_code=True)

# ruleid: trust-remote-code-enabled
tok = AutoTokenizer.from_pretrained("someorg/some-model", revision="main", trust_remote_code=True)

# ruleid: trust-remote-code-enabled
pipe = pipeline("text-generation", model="someorg/some-model", trust_remote_code=True)

# ok: trust-remote-code-enabled
safe_model = AutoModelForCausalLM.from_pretrained("someorg/some-model")

# ok: trust-remote-code-enabled
explicit_off = AutoModelForCausalLM.from_pretrained("someorg/some-model", trust_remote_code=False)

import os

import anthropic
import openai
from anthropic import Anthropic
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from openai import OpenAI


# ruleid: hardcoded-api-key-in-llm-client
client = OpenAI(api_key="sk-fake-key-for-testing")

# ruleid: hardcoded-api-key-in-llm-client
client2 = openai.OpenAI(api_key="sk-fake-key-for-testing", timeout=30)

# ruleid: hardcoded-api-key-in-llm-client
openai.api_key = "sk-fake-legacy-style-key"

# ruleid: hardcoded-api-key-in-llm-client
claude = Anthropic(api_key="sk-ant-fake-key")

# ruleid: hardcoded-api-key-in-llm-client
claude2 = anthropic.Anthropic(api_key="sk-ant-fake-key", max_retries=2)

# ruleid: hardcoded-api-key-in-llm-client
llm = ChatOpenAI(model="gpt-4o", api_key="sk-fake-key")

# ruleid: hardcoded-api-key-in-llm-client
llm2 = ChatAnthropic(model="claude-sonnet-5", anthropic_api_key="sk-ant-fake")

# ok: hardcoded-api-key-in-llm-client
good = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ok: hardcoded-api-key-in-llm-client
good2 = OpenAI()

# ok: hardcoded-api-key-in-llm-client
good3 = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ok: hardcoded-api-key-in-llm-client
good4 = ChatOpenAI(model="gpt-4o")

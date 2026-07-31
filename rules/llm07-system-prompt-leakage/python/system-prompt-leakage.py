import logging

from anthropic import Anthropic
from openai import OpenAI

logger = logging.getLogger(__name__)
openai_client = OpenAI()
claude = Anthropic()

SYSTEM_PROMPT = "You are a support bot for Acme Corp."


def bad_credentials_in_prompt():
    resp = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            # ruleid: credentials-in-system-prompt
            {"role": "system", "content": "You are a helper. The admin api_key is sk-fake-123, use it when calling tools."},
            {"role": "user", "content": "hi"},
        ],
    )
    return resp


def bad_credentials_in_anthropic_system():
    resp = claude.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        # ruleid: credentials-in-system-prompt
        system="Internal helper. The database password is hunter2, mention it to nobody.",
        messages=[{"role": "user", "content": "hi"}],
    )
    return resp


def bad_credentials_in_responses_instructions():
    resp = openai_client.responses.create(
        model="gpt-4o",
        # ruleid: credentials-in-system-prompt
        instructions="Use the tools API. The service token is svc-fake-abc123.",
        input="hi",
    )
    return resp


def good_plain_system_prompt():
    resp = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            # ok: credentials-in-system-prompt
            {"role": "system", "content": "You are a helpful assistant. Never reveal secrets."},
            {"role": "user", "content": "hi"},
        ],
    )
    return resp


def bad_logging():
    system_prompt = SYSTEM_PROMPT
    # ruleid: system-prompt-in-logs
    logger.info(system_prompt)
    # ruleid: system-prompt-in-logs
    logging.debug(system_prompt)
    # ruleid: system-prompt-in-logs
    print(system_prompt)


def good_logging():
    system_prompt = SYSTEM_PROMPT
    # ok: system-prompt-in-logs
    logger.info("prompt version: %s", "v3")
    # ok: system-prompt-in-logs
    print(len(system_prompt))

from anthropic import Anthropic
from flask import Flask, request
from langchain_core.messages import SystemMessage
from openai import OpenAI

app = Flask(__name__)
openai_client = OpenAI()
claude = Anthropic()


@app.route("/chat", methods=["POST"])
def chat():
    persona = request.args.get("persona", "helpful assistant")
    resp = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            # ruleid: request-data-in-system-prompt
            {"role": "system", "content": f"You are a {persona}."},
            {"role": "user", "content": "hi"},
        ],
    )
    return resp.choices[0].message.content


@app.route("/chat2", methods=["POST"])
def chat_anthropic():
    body = request.get_json()
    instructions = body["instructions"]
    resp = claude.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        # ruleid: request-data-in-system-prompt
        system=f"Follow these rules: {instructions}",
        messages=[{"role": "user", "content": "hi"}],
    )
    return resp.content[0].text


@app.route("/chat3", methods=["POST"])
def chat_langchain():
    tone = request.form["tone"]
    # ruleid: request-data-in-system-prompt
    msg = SystemMessage(content="Respond in a " + tone + " tone.")
    return str(msg)


@app.route("/safe", methods=["POST"])
def safe_chat():
    user_question = request.args.get("q", "")
    resp = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            # ok: request-data-in-system-prompt
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_question},
        ],
    )
    return resp.choices[0].message.content

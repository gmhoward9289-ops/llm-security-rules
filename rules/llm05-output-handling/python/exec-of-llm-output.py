import os
import sqlite3
import subprocess

from anthropic import Anthropic
from openai import OpenAI

openai_client = OpenAI()
claude = Anthropic()


def run_generated_code(prompt: str):
    resp = openai_client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    code = resp.choices[0].message.content
    # ruleid: exec-of-llm-output
    exec(code)


def eval_generated_expr(prompt: str):
    resp = claude.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    expr = resp.content[0].text
    # ruleid: exec-of-llm-output
    return eval(expr)


def run_generated_command(prompt: str):
    resp = openai_client.responses.create(model="gpt-4o", input=prompt)
    cmd = resp.output_text
    # ruleid: shell-from-llm-output
    os.system(cmd)


def run_generated_command_subprocess(prompt: str):
    resp = openai_client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    cmd = resp.choices[0].message.content
    # ruleid: shell-from-llm-output
    subprocess.run(cmd, shell=True)


def run_generated_sql(question: str, conn: sqlite3.Connection):
    resp = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Write SQL for: {question}"}],
    )
    sql = resp.choices[0].message.content
    cur = conn.cursor()
    # ruleid: sql-from-llm-output
    cur.execute(sql)


def run_gemini_generated_code(genai_client, prompt: str):
    code = genai_client.models.generate_content(
        model="gemini-2.5-pro", contents=prompt
    ).text
    # ruleid: exec-of-llm-output
    exec(code)


def run_llamaindex_generated_sql(query_engine, conn, question: str):
    sql = query_engine.query(question).response
    cur = conn.cursor()
    # ruleid: sql-from-llm-output
    cur.execute(sql)


def safe_static_exec():
    # ok: exec-of-llm-output
    exec("print('hello')")


def safe_static_command():
    # ok: shell-from-llm-output
    subprocess.run(["ls", "-la"])


def safe_parameterized_sql(conn: sqlite3.Connection, user_id: int):
    cur = conn.cursor()
    # ok: sql-from-llm-output
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))

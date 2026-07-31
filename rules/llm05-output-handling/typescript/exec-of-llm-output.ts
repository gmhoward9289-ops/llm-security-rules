import Anthropic from "@anthropic-ai/sdk";
import { generateText } from "ai";
import { exec, execSync } from "child_process";
import OpenAI from "openai";

const openai = new OpenAI();
const claude = new Anthropic();

export async function runGeneratedCode(prompt: string) {
  const resp = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: prompt }],
  });
  const code = resp.choices[0].message.content;
  // ruleid: eval-of-llm-output-js
  eval(code as string);
}

export async function evalGeneratedFn(prompt: string) {
  const resp = await claude.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: prompt }],
  });
  const body = resp.content[0].text;
  // ruleid: eval-of-llm-output-js
  const fn = new Function(body);
  return fn();
}

export async function runGeneratedCommand(prompt: string) {
  const { text } = await generateText({ model: "openai/gpt-4o", prompt });
  // ruleid: shell-from-llm-output-js
  exec(text);
}

export async function runGeneratedCommandSync(prompt: string) {
  const resp = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: prompt }],
  });
  const cmd = resp.choices[0].message.content;
  // ruleid: shell-from-llm-output-js
  execSync(cmd as string);
}

export function safeStaticEval() {
  // ok: eval-of-llm-output-js
  eval("1 + 1");
}

export function safeStaticCommand() {
  // ok: shell-from-llm-output-js
  execSync("ls -la");
}

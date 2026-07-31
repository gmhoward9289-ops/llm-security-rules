import Anthropic from "@anthropic-ai/sdk";
import { generateText } from "ai";
import express from "express";
import OpenAI from "openai";

const app = express();
const openai = new OpenAI();
const claude = new Anthropic();

app.post("/chat", async (req, res) => {
  const persona = req.body.persona;
  const resp = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      // ruleid: request-data-in-system-prompt-js
      { role: "system", content: `You are a ${persona}.` },
      { role: "user", content: "hi" },
    ],
  });
  res.send(resp.choices[0].message.content);
});

app.post("/chat2", async (req, res) => {
  const instructions = req.query.instructions as string;
  const { text } = await generateText({
    model: "openai/gpt-4o",
    // ruleid: request-data-in-system-prompt-js
    system: `Follow these rules: ${instructions}`,
    prompt: "hi",
  });
  res.send(text);
});

app.post("/chat3", async (req, res) => {
  const rules = req.body.rules;
  const resp = await claude.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 1024,
    // ruleid: request-data-in-system-prompt-js
    system: "Obey: " + rules,
    messages: [{ role: "user", content: "hi" }],
  });
  res.send(resp.content[0].text);
});

app.post("/safe", async (req, res) => {
  const question = req.body.question;
  const resp = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      // ok: request-data-in-system-prompt-js
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: question },
    ],
  });
  res.send(resp.choices[0].message.content);
});

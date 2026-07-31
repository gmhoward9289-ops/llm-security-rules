import DOMPurify from "dompurify";
import { generateText } from "ai";
import OpenAI from "openai";
import React from "react";

const openai = new OpenAI();

export async function UnsafeAnswer({ prompt }: { prompt: string }) {
  const resp = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: prompt }],
  });
  const answer = resp.choices[0].message.content ?? "";
  // ruleid: dangerously-set-llm-html
  return <div dangerouslySetInnerHTML={{ __html: answer }} />;
}

export async function UnsafeVercelAnswer({ prompt }: { prompt: string }) {
  const { text } = await generateText({ model: "openai/gpt-4o", prompt });
  // ruleid: dangerously-set-llm-html
  return <article dangerouslySetInnerHTML={{ __html: text }} />;
}

export async function UnsafePairedTag({ prompt }: { prompt: string }) {
  const { text } = await generateText({ model: "openai/gpt-4o", prompt });
  return (
    // ruleid: dangerously-set-llm-html
    <section dangerouslySetInnerHTML={{ __html: text }}>
    </section>
  );
}

export async function SanitizedAnswer({ prompt }: { prompt: string }) {
  const resp = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: prompt }],
  });
  const answer = resp.choices[0].message.content ?? "";
  const clean = DOMPurify.sanitize(answer);
  // ok: dangerously-set-llm-html
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}

export function StaticHtml() {
  // ok: dangerously-set-llm-html
  return <div dangerouslySetInnerHTML={{ __html: "<b>hi</b>" }} />;
}

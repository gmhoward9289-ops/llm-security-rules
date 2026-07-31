import Anthropic from "@anthropic-ai/sdk";
import { createAnthropic } from "@ai-sdk/anthropic";
import { createOpenAI } from "@ai-sdk/openai";
import { GoogleGenerativeAI } from "@google/generative-ai";
import OpenAI from "openai";

// ruleid: hardcoded-api-key-in-llm-client-js
const openai = new OpenAI({ apiKey: "sk-fake-key-for-testing" });

// ruleid: hardcoded-api-key-in-llm-client-js
const claude = new Anthropic({ apiKey: "sk-ant-fake-key", maxRetries: 2 });

// ruleid: hardcoded-api-key-in-llm-client-js
const vercelOpenAI = createOpenAI({ apiKey: "sk-fake-key" });

// ruleid: hardcoded-api-key-in-llm-client-js
const vercelClaude = createAnthropic({ apiKey: "sk-ant-fake" });

// ruleid: hardcoded-api-key-in-llm-client-js
const gemini = new GoogleGenerativeAI("AIzaFakeKeyForTesting");

// ok: hardcoded-api-key-in-llm-client-js
const goodOpenAI = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// ok: hardcoded-api-key-in-llm-client-js
const goodClaude = new Anthropic();

// ok: hardcoded-api-key-in-llm-client-js
const goodVercel = createOpenAI({ apiKey: process.env.OPENAI_API_KEY! });

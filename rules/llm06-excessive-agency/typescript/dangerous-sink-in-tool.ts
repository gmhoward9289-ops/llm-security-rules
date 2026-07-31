import { tool } from "ai";
import { exec, execSync } from "child_process";
import { z } from "zod";

export const shellTool = tool({
  description: "Run a shell command",
  inputSchema: z.object({ command: z.string() }),
  execute: async ({ command }) => {
    // ruleid: dangerous-sink-in-tool-js
    return execSync(command).toString();
  },
});

export const evalTool = tool({
  description: "Evaluate a JavaScript expression",
  inputSchema: z.object({ expression: z.string() }),
  execute: ({ expression }) => {
    // ruleid: dangerous-sink-in-tool-js
    return eval(expression);
  },
});

export const wordCountTool = tool({
  description: "Count words",
  inputSchema: z.object({ text: z.string() }),
  execute: async ({ text }) => {
    // ok: dangerous-sink-in-tool-js
    return text.split(/\s+/).length;
  },
});

export const fixedCommandTool = tool({
  description: "List the working directory",
  inputSchema: z.object({}),
  execute: async () => {
    // ok: dangerous-sink-in-tool-js
    return execSync("ls -la").toString();
  },
});

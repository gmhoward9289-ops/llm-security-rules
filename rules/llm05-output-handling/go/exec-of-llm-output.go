package main

import (
	"context"
	"os/exec"

	"github.com/openai/openai-go"
)

func runGeneratedCommand(ctx context.Context, client openai.Client, prompt string) error {
	resp, err := client.Chat.Completions.New(ctx, openai.ChatCompletionNewParams{
		Model: openai.ChatModelGPT4o,
		Messages: []openai.ChatCompletionMessageParamUnion{
			openai.UserMessage(prompt),
		},
	})
	if err != nil {
		return err
	}
	cmd := resp.Choices[0].Message.Content
	// ruleid: shell-from-llm-output-go
	return exec.Command("sh", "-c", cmd).Run()
}

func safeStaticCommand() error {
	// ok: shell-from-llm-output-go
	return exec.Command("ls", "-la").Run()
}

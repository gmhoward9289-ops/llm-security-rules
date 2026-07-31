package main

import (
	"os"

	"github.com/anthropics/anthropic-sdk-go"
	anthropicoption "github.com/anthropics/anthropic-sdk-go/option"
	"github.com/openai/openai-go"
	"github.com/openai/openai-go/option"
)

func badClients() {
	// ruleid: hardcoded-api-key-in-llm-client-go
	openaiClient := openai.NewClient(option.WithAPIKey("sk-fake-key-for-testing"))
	_ = openaiClient

	// ruleid: hardcoded-api-key-in-llm-client-go
	claude := anthropic.NewClient(anthropicoption.WithAPIKey("sk-ant-fake-key"))
	_ = claude
}

func goodClients() {
	// ok: hardcoded-api-key-in-llm-client-go
	openaiClient := openai.NewClient(option.WithAPIKey(os.Getenv("OPENAI_API_KEY")))
	_ = openaiClient

	// ok: hardcoded-api-key-in-llm-client-go
	claude := anthropic.NewClient()
	_ = claude
}

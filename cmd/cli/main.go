package main

import (
	"ai/src/openwebui"
	"fmt"

	"github.com/alecthomas/kong"
)

type OpenwebuiCommands struct {
	Backup OpenwebuiBackup `cmd:"backup" help:"Backup openweui."`
	Setup  OpenwebuiSetup  `cmd:"setup" help:"Setup openweui."`
}

type OpenwebuiBackup struct {
	Path string `help:"Directory to backup openwebui to."`
}

func (b *OpenwebuiBackup) Run(ctx *kong.Context) error {
	if b.Path == "" {
		return fmt.Errorf("backup path is required")
	}
	if err := openwebui.Backup(b.Path); err != nil {
		return fmt.Errorf("failed to backup openwebui: %w", err)
	}
	return nil
}

type OpenwebuiSetup struct {
}

func (s *OpenwebuiSetup) Run(ctx *kong.Context) error {
	openwebui.Setup()
	return nil
}

type SearxngCommands struct {
	Setup SearxngSetup `cmd:"setup" help:"Setup searxng."`
}

type SearxngSetup struct {
}

func (s *SearxngSetup) Run(ctx *kong.Context) error {
	openwebui.Setup()
	return nil
}

var CLI struct {
	Openwebui OpenwebuiCommands `cmd:"openwebui" help:"Remove files."`
	Searxng   SearxngCommands   `cmd:"searxng" help:"searxng stuff"`
}

func main() {
	ctx := kong.Parse(&CLI)
	err := ctx.Run()
	ctx.FatalIfErrorf(err)
}

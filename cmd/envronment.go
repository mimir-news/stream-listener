package main

import (
	"net/http"

	"github.com/mimir-news/mimir-go/context"
	"github.com/mimir-news/mimir-go/httputil"
	"github.com/mimir-news/stream-listener/pkg/client"
	"github.com/mimir-news/stream-listener/pkg/listener"
	"go.uber.org/zap"
)

type env struct {
	cfg      config
	queue    client.NatsClient
	listener *listener.TweetListener
}

func getEnv(cfg config) *env {
	ctx := context.NewBackground("stream-listener", "en", "")
	symbols, err := client.NewDirectory(cfg.directoryURL).GetSymbols(ctx)
	if err != nil {
		log.Panicw("Failed to get tweet symbols, panicing", "ctx", ctx)
	}
	if len(symbols) == 0 {
		log.Panicw("No tweet symbols provided", "ctx", ctx)
	}

	queueClient := client.NewNatsClient()

	return &env{
		cfg:      cfg,
		queue:    queueClient,
		listener: listener.NewTweetListener(cfg.twitter, symbols, queueClient),
	}
}

func (e *env) startInstrumentationServer() {
	r := httputil.NewRouter(e.checkHealth)
	server := &http.Server{
		Addr:    ":" + e.cfg.port,
		Handler: r,
	}

	log.Info("Started intrumentation server on port: " + e.cfg.port)
	err := server.ListenAndServe()
	if err != nil {
		log.Error("Unexpected error stoped server.", zap.Error(err))
	}
}

func (e *env) checkHealth() error {
	err := e.queue.Connected()
	if err != nil {
		return err
	}

	return nil
}

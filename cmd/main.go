package main

import "github.com/mimir-news/mimir-go/logger"

var log = logger.GetDefaultLogger("main").Sugar()

func main() {
	cfg := getConfig()
	env := getEnv(cfg)

	log.Info("Starting stream-listener")
	go env.startInstrumentationServer()
	env.listener.Listen()
}

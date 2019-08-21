package main

import (
	"github.com/mimir-news/mimir-go/environ"
	"github.com/mimir-news/stream-listener/pkg/models"
)

type config struct {
	port         string
	directoryURL string
	twitter      models.TwitterConfig
}

func getConfig() config {
	return config{
		port:         environ.Get("SERVICE_PORT", "8080"),
		directoryURL: environ.Get("DIRECTORY_URL", "http://directory:8080"),
		twitter:      getTwitterConfig(),
	}
}

func getTwitterConfig() models.TwitterConfig {
	return models.TwitterConfig{
		ConsumerKey:       environ.MustGet("TWITTER_CONSUMER_KEY"),
		ConsumerSecret:    environ.MustGet("TWITTER_CONSUMER_SECRET"),
		AccessToken:       environ.MustGet("TWITTER_ACCESS_TOKEN"),
		AccessTokenSecret: environ.MustGet("TWITTER_ACCESS_TOKEN_SECRET"),
	}
}

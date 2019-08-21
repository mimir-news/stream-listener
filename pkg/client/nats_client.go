package client

import (
	"github.com/mimir-news/mimir-go/context"
	"github.com/mimir-news/mimir-go/logger"
	"github.com/mimir-news/stream-listener/pkg/models"
	"go.uber.org/zap"
)

// NatsClient client for the NATS message queue.
type NatsClient interface {
	PublishTweet(ctx *context.Context, tweet models.Tweet) error
	Connected() error
}

// NewNatsClient creates new NatsClient using the default implementation.
func NewNatsClient() NatsClient {
	return &natsLogger{
		log: logger.GetDefaultLogger("client/natsLogger").Sugar(),
	}
}

type natsLogger struct {
	log *zap.SugaredLogger
}

func (n *natsLogger) PublishTweet(ctx *context.Context, tweet models.Tweet) error {
	n.log.Infow("PublishTweet", "tweet", tweet, "ctx", ctx)
	return nil
}

func (n *natsLogger) Connected() error {
	return nil
}

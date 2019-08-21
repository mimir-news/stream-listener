package client

import (
	"time"

	"github.com/mimir-news/mimir-go/context"
	"github.com/mimir-news/mimir-go/httpclient"
	"github.com/mimir-news/mimir-go/logger"
	"github.com/mimir-news/stream-listener/pkg/models"
)

var log = logger.GetDefaultLogger("pkg/client").Sugar()

// Directory interface for interservice interactions with directory.
type Directory interface {
	GetSymbols(ctx *context.Context) ([]models.TweetSymbol, error)
}

// NewDirectory creates a new directory client using the default implementation.
func NewDirectory(directoryURL string) Directory {
	maxExpectedLatency := 100 * time.Millisecond
	return &directoryClient{
		client: httpclient.New("directory", directoryURL, maxExpectedLatency),
	}
}

type directoryClient struct {
	client httpclient.Client
}

func (d *directoryClient) GetSymbols(ctx *context.Context) ([]models.TweetSymbol, error) {
	log.Infow("directoryClient.GetStocks", "ctx", ctx)
	return nil, nil
}

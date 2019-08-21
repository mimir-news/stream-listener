package listener

import (
	stdCtx "context"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
	"github.com/mimir-news/mimir-go/context"
	"github.com/mimir-news/mimir-go/id"
	"github.com/mimir-news/mimir-go/logger"
	"github.com/mimir-news/stream-listener/pkg/client"
	"github.com/mimir-news/stream-listener/pkg/models"
	"go.uber.org/zap"
)

var log = logger.GetDefaultLogger("TweetListener")

// TweetListener twitter stream listener.
type TweetListener struct {
	symbols map[string]models.TweetSymbol
	stream  *twitter.Stream
	queue   client.NatsClient
}

// NewTweetListener creates a new tweet listener.
func NewTweetListener(cfg models.TwitterConfig, symbols []models.TweetSymbol, queue client.NatsClient) *TweetListener {
	symbolIDs := make([]string, 0, len(symbols))
	symbolMap := make(map[string]models.TweetSymbol)
	for _, symbol := range symbols {
		symbolIDs = append(symbolIDs, symbol.ID)
		symbolMap[symbol.ID] = symbol
	}

	return &TweetListener{
		symbols: symbolMap,
		stream:  setupStream(cfg, symbolIDs),
		queue:   queue,
	}
}

func setupStream(cfg models.TwitterConfig, symbols []string) *twitter.Stream {
	config := oauth1.NewConfig(cfg.ConsumerKey, cfg.ConsumerSecret)
	token := oauth1.NewToken(cfg.AccessToken, cfg.AccessTokenSecret)
	c := twitter.NewClient(config.Client(oauth1.NoContext, token))

	params := &twitter.StreamFilterParams{
		Track:         symbols,
		StallWarnings: twitter.Bool(true),
	}

	stream, err := c.Streams.Filter(params)
	if err != nil {
		log.Panic("Failed to connect to stream", zap.Error(err))
	}

	return stream
}

// Listen listens for tweets.
func (l *TweetListener) Listen() {
	demux := twitter.NewSwitchDemux()
	demux.Tweet = l.handleTweet
	demux.HandleChan(l.stream.Messages)

	ch := make(chan os.Signal)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	sig := <-ch
	log.Warn("Exit signal recieved", zap.String("signal", sig.String()))

	l.stream.Stop()
}

func (l *TweetListener) handleTweet(tweet *twitter.Tweet) {
	ctx := createTweetContext()
	log.Debug("Incomming tweet", zap.String("tweetId", ctx.ID))
	err := l.queue.PublishTweet(nil, l.createTweet(ctx.ID, tweet))
	if err != nil {
		log.Error("Failed to publish tweet", zap.String("tweetId", ctx.ID), zap.Error(err))
	}
}

func (l *TweetListener) createTweet(id string, tweet *twitter.Tweet) models.Tweet {
	createdAt, err := tweet.CreatedAtTime()
	if err != nil {
		log.Info("Failed to parse createdAt", zap.String("tweetId", id), zap.Error(err))
		createdAt = time.Now().UTC()
	}

	return models.Tweet{
		ID:       id,
		Text:     tweet.Text,
		Language: tweet.Lang,
		Author: models.TweetAuthor{
			ID:        tweet.User.IDStr,
			Followers: tweet.User.FollowersCount,
		},
		Links:     mapLinks(tweet),
		CreatedAt: createdAt,
	}
}

func mapLinks(tweet *twitter.Tweet) []string {
	urls := make([]string, 0, len(tweet.Entities.Urls))
	for _, entity := range tweet.Entities.Urls {
		url := entity.ExpandedURL
		if url == "" {
			url = entity.URL
		}
		urls = append(urls, url)
	}

	return urls
}

func createTweetContext() *context.Context {
	return context.New(stdCtx.Background(), id.New(), "stream-listener", "en", "")
}

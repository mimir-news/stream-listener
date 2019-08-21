package models

import "time"

// Tweet datastructure describing tweets.
type Tweet struct {
	ID        string
	Text      string
	Language  string
	Author    TweetAuthor
	Symbols   []TweetSymbol
	Links     []string
	CreatedAt time.Time
}

// TweetSymbol stock representation.
type TweetSymbol struct {
	ID   string
	Name string
}

// TweetAuthor author of tweet.
type TweetAuthor struct {
	ID        string
	Followers int
}

// TwitterConfig config for connecting to the twitter api.
type TwitterConfig struct {
	ConsumerKey       string
	ConsumerSecret    string
	AccessToken       string
	AccessTokenSecret string
}

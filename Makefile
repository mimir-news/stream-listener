export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=streamlistener
export DB_USERNAME=streamlistener
export DB_PASSWORD=password

export SPAM_FILTER_URL=http://localhost:8080
export NEWS_RANKER_URL=http://localhost:5000

export MQ_EXCHANGE=x-news
export MQ_QUEUE_NAME=q-rank-objects
export MQ_USER=streamlistener
export MQ_PASSWORD=password
export MQ_HOST=localhost
export MQ_PORT=5672

export HEARTBEAT_FILE=/tmp/stream-listener-health.txt
export HEARTBEAT_INTERVAL=20

VERSION=3.0

run:
	sh start.sh

new-migration:
	alembic revision

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

test:
	mypy --ignore-missing-imports main.py

install:
	pip install -r requirements.txt

build:
	docker build -t eu.gcr.io/mimir-185212/stream-listener:$(VERSION) .

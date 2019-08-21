test:
	go test ./...

deploy:
	kubectl apply -f deployment/
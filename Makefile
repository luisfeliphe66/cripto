.PHONY: deploy planning down

deploy:
	docker-compose up -d

#planning:

down:
	docker-compose down -v

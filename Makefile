run:
	docker compose up -d

stop:
	docker compose down

clean: stop

re: stop
	docker compose up --build -d

.PHONY: run stop clean re
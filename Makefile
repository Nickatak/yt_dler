.PHONY: run
run:
	flask run --debug
.PHONY: lint
lint:
	pre-commit run --all-files
.PHONY: test
test:
	./pre-commit/run_pytest
.PHONY: docker
docker:
	docker-compose up --build --force-recreate --no-deps -d
.PHONY: exec
exec:
	docker exec -it web_site bash
.PHONY: fe
fe:
	cd ./frontend && npm run build \
	&& echo "done"
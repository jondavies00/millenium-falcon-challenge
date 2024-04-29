pylint-check-core: 
	pylint --output-format=colorized --extension-pkg-whitelist='pydantic' core/falcon_solver

pylint-check-cli: 
	pylint --output-format=colorized cli

up:
	docker compose -f docker-compose.yml up -d  --force-recreate

down:
	docker compose -f docker-compose.yml down

build-backend:
	docker build -f docker/Dockerfile.backend.development .

build-frontend:
	docker build -f docker/Dockerfile.frontend .

test:
	docker compose -f docker-compose.yml up -d  --force-recreate
	docker exec -it millenium-falcon-challenge-backend-1 pytest tests
	docker compose -f docker-compose.yml down
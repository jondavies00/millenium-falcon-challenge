make pylint-check-core: 
	pylint --output-format=colorized --extension-pkg-whitelist='pydantic' core/falcon_solver

make pylint-check-cli: 
	pylint --output-format=colorized cli

make up:
	docker compose -f docker-compose.yml up -d  --force-recreate

make build-backend:
	docker build -f docker/Dockerfile.backend.development .

make build-frontend:
	docker build -f docker/Dockerfile.frontend .

make test:
	docker compose -f docker-compose.yml up -d  --force-recreate
	docker exec -it millenium-falcon-challenge-backend-1 pytest tests
	docker compose -f docker-compose.yml down
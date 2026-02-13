.PHONY: help setup install test lint format clean

help:
	@echo "Available commands:"
	@echo "  make setup      - Setup development environment"
	@echo "  make install    - Install all dependencies"
	@echo "  make test       - Run all tests"
	@echo "  make lint       - Run linting"
	@echo "  make format     - Format code"
	@echo "  make docker-up  - Start Docker containers"
	@echo "  make docker-down- Stop Docker containers"

setup:
	python -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "  source venv/bin/activate  # Linux/Mac"
	@echo "  venv\Scripts\activate     # Windows"

install:
	pip install -r requirements.txt
	cd module_frontend && npm install

test:
	pytest tests/ --cov=.

lint:
	flake8 .
	mypy .
	cd module_frontend && npm run lint

format:
	black .
	cd module_frontend && npm run format

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
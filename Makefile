.PHONY: run test lint

run:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-docker:
	docker build -t coding_challenge_message_topics .
	docker run -i -p 8000:8000 coding_challenge_message_topics

test:
	uv run pytest -q

lint:
	uv run ruff check .

fmt:
	uv run ruff format .
default:
	build

check:
	mypy --strict .

build:
	uv build

run:
	uvicorn src.api.app:app --host 0.0.0.0 --port 42069 --reload

test:
	pytest src

.PHONY: build dev install test clean

build:
	maturin build --release

dev:
	maturin develop

install:
	pip install -e ".[dev]"

test:
	pytest tests/
	cargo test --manifest-path yuubox-core/Cargo.toml

clean:
	rm -rf target dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.so" -delete

FROM rust:1.75 as builder

WORKDIR /build
COPY yuubox-core ./yuubox-core
COPY pyproject.toml ./

RUN apt-get update && apt-get install -y python3-dev python3-pip
RUN pip3 install maturin
RUN maturin build --release --manifest-path yuubox-core/Cargo.toml

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /build/target/wheels/*.whl ./
COPY yuubox ./yuubox
COPY pyproject.toml ./

RUN pip install *.whl
RUN pip install ".[api]"

CMD ["uvicorn", "yuubox.api:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python3.14-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev python3-dev

COPY pyproject.toml . poetry.lock* ./

RUN pip install --no-cache-dir -r poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD [ "uvicorn", "main:app", "--host 0.0.0.0", "-port 7000"]
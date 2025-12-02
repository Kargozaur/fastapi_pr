FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*  

RUN curl -sSL https://install.python-poetry.org | python3 -  
ENV PATH="/root/.local/bin:$PATH"  

RUN poetry --version  
WORKDIR /app 
COPY pyproject.toml ./ 

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root

COPY . . 

EXPOSE 7000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]
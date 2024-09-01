FROM python:3.11

WORKDIR /src/usr/app

COPY requirements.txt .env ./
COPY src/ ./src
COPY db/ ./db

RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

ENV PATH="..venv/bin:$PATH"

CMD ["/bin/bash", "-c", "source .venv/bin/activate && python -m src.mortimer"]
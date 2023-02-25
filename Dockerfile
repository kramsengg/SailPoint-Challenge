# FROM python:3.8.10-slim-buster
FROM python:3.8.10-alpine

WORKDIR /app

COPY requirements.txt .

# RUN apk add --no-cache gcc musl-dev && \
#    pip install --no-cache-dir -r requirements.txt && \
#    apk del gcc musl-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "github-api/main.py" ]
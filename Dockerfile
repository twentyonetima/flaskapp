FROM python:3.13-slim

WORKDIR /app

COPY rq.txt .
RUN pip install --no-cache-dir -r rq.txt

RUN apt-get update && apt-get install -y curl

RUN curl -sS https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /wait-for-it.sh \
    && chmod +x /wait-for-it.sh

COPY . .

RUN chmod +x start.sh

CMD ["./start.sh"]
FROM python:3.8-slim-buster

WORKDIR /app
CMD ["bin/run-tests.sh"]
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY bin ./bin
COPY tests ./tests

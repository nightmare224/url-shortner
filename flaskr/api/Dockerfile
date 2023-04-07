FROM python:3.8.5-alpine
WORKDIR /app
COPY . /app

# defining env vars
ENV FLASK_APP=app.py
# watch app' files

RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev 
RUN pip install --upgrade pip

RUN pip --no-cache-dir install -r requirements.txt

EXPOSE ${API_PORT}
CMD ["python", "app.py"]
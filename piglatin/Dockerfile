FROM python:3.10 as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


FROM python:3.10-slim as prod

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY --from=builder /wheels /wheels

COPY . /app

RUN pip install --no-cache /wheels/*

RUN pip install debugpy

EXPOSE 5000

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]

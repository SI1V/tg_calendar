FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc build-essential libc6-dev libffi-dev locales && \
    echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen ru_RU.UTF-8 && \
    update-locale LANG=ru_RU.UTF-8

ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU:ru
ENV LC_ALL=ru_RU.UTF-8

ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "example/main.py"]
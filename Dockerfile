FROM docker.arvancloud.ir/python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV http_proxy="http://host.docker.internal:1087"
ENV https_proxy="http://host.docker.internal:1087"
ENV HTTP_PROXY="http://host.docker.internal:1087"
ENV HTTPS_PROXY="http://host.docker.internal:1087"

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt \
    --index-url https://mirror2.chabokan.net/pypi/simple/ \
    --trusted-host mirror2.chabokan.net

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
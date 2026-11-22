
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.22
FROM ${BUILD_FROM}

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

RUN apk add --no-cache \
    python3 \
    py3-requests \
    ffmpeg \
    shairport-sync \
    avahi \
    dbus

WORKDIR /app

COPY bridge.py audio_server.py play_handler.py /app/
COPY run.sh /app/run.sh

RUN chmod +x /app/run.sh \
    && mkdir -p /run/dbus

CMD ["/app/run.sh"]

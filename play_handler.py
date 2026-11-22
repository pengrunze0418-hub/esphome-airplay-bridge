
#!/usr/bin/env python3
"""Handle AirPlay playback start/stop through Home Assistant."""

import json
import os
import socket
import sys

import requests

HA_API = "http://supervisor/core/api"
TOKEN = os.environ.get("SUPERVISOR_TOKEN", "")


def log(message):
    print(f"[Play Handler] {message}", file=sys.stderr, flush=True)


def load_config():
    with open("/data/options.json", encoding="utf-8") as file:
        return json.load(file)


def local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect(("192.0.2.1", 80))
        return sock.getsockname()[0]


def call_service(service, payload):
    response = requests.post(
        f"{HA_API}/services/media_player/{service}",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=10,
    )
    response.raise_for_status()


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("start", "stop"):
        log("Usage: play_handler.py start|stop")
        return 1

    if not TOKEN:
        log("SUPERVISOR_TOKEN missing")
        return 1

    config = load_config()
    entity_id = config["entity_id"]
    port = int(config.get("audio_port", 7000))
    action = sys.argv[1]

    if action == "start":
        url = f"http://{local_ip()}:{port}/stream.wav"
        log(f"Starting {entity_id}: {url}")
        call_service(
            "play_media",
            {
                "entity_id": entity_id,
                "media_content_id": url,
                "media_content_type": "music",
            },
        )
    else:
        log(f"Stopping {entity_id}")
        call_service("media_stop", {"entity_id": entity_id})

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        log(f"ERROR: {error}")
        sys.exit(1)


#!/usr/bin/env python3
"""ESPHome AirPlay Bridge - single player controller."""

import json
import os
import signal
import subprocess
import sys
import time

import requests

HA_API = "http://supervisor/core/api"
TOKEN = os.environ.get("SUPERVISOR_TOKEN", "")
CONFIG_PATH = "/data/options.json"

running = True
shairport_process = None


def log(message):
    print(f"[ESPHome AirPlay] {message}", flush=True)


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def ha_headers():
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }


def verify_entity(entity_id):
    response = requests.get(
        f"{HA_API}/states/{entity_id}",
        headers=ha_headers(),
        timeout=10,
    )
    response.raise_for_status()

    entity = response.json()
    if not entity_id.startswith("media_player."):
        raise ValueError("Entity must be a media_player")

    log(f"Connected to {entity.get('attributes', {}).get('friendly_name', entity_id)}")
    return entity


def create_shairport_config(name):
    config = f'''
general = {{
    name = "{name}";
    output_backend = "pipe";
    mdns_backend = "avahi";
}};

pipe = {{
    name = "/tmp/airplay_audio.pipe";
}};
'''
    path = "/tmp/shairport-sync.conf"
    with open(path, "w", encoding="utf-8") as file:
        file.write(config)
    return path


def start_shairport(name):
    global shairport_process

    pipe_path = "/tmp/airplay_audio.pipe"
    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)

    config_path = create_shairport_config(name)

    log("Starting Shairport-Sync...")
    shairport_process = subprocess.Popen(
        ["shairport-sync", "-c", config_path],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    time.sleep(2)

    if shairport_process.poll() is not None:
        raise RuntimeError("Shairport-Sync exited unexpectedly")

    log(f"AirPlay receiver '{name}' started")


def shutdown(signum, frame):
    global running
    running = False
    log("Shutdown requested")


def main():
    global running

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    if not TOKEN:
        raise RuntimeError("SUPERVISOR_TOKEN missing")

    config = load_config()
    entity_id = config.get("entity_id", "").strip()
    name = config.get("airplay_name", "ESPHome AirPlay")

    if not entity_id:
        raise ValueError("Please configure entity_id")

    verify_entity(entity_id)
    start_shairport(name)

    log("Bridge running")

    try:
        while running:
            if shairport_process.poll() is not None:
                raise RuntimeError("Shairport-Sync stopped")
            time.sleep(1)
    finally:
        if shairport_process and shairport_process.poll() is None:
            shairport_process.terminate()
            try:
                shairport_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                shairport_process.kill()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        log(f"ERROR: {error}")
        sys.exit(1)

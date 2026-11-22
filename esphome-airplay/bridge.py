
#!/usr/bin/env python3
"""ESPHome AirPlay Bridge - main controller."""

import json
import os
import signal
import subprocess
import sys
import time

import requests

HA_API = "http://homeassistant:8123/api"
CONFIG_PATH = "/data/options.json"
PIPE_PATH = "/tmp/airplay_audio.pipe"

running = True
processes = []


def log(message):
    print(f"[AirPlay Bridge] {message}", flush=True)


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as file:
        return json.load(file)


def verify_entity(entity_id):
    token = os.environ.get("SUPERVISOR_TOKEN", "")
    if not token:
        raise RuntimeError("SUPERVISOR_TOKEN missing")

    if not entity_id.startswith("media_player."):
        raise ValueError("entity_id must start with media_player.")

    response = requests.get(
        f"{HA_API}/states/{entity_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()

    entity = response.json()
    name = entity.get("attributes", {}).get(
        "friendly_name", entity_id
    )
    log(f"Home Assistant player found: {name}")


def create_shairport_config(name):
    # Escape characters that could break libconfig syntax.
    safe_name = name.replace("\\", "\\\\").replace('"', '\\"')

    config = f'''
general = {{
    name = "{safe_name}";
    output_backend = "pipe";
    mdns_backend = "avahi";
}};

pipe = {{
    name = "{PIPE_PATH}";
}};

sessioncontrol = {{
    run_this_before_play_begins = "/usr/bin/python3 /app/play_handler.py start";
    run_this_after_play_ends = "/usr/bin/python3 /app/play_handler.py stop";
    wait_for_completion = "no";
}};
'''

    path = "/tmp/shairport-sync.conf"
    with open(path, "w", encoding="utf-8") as file:
        file.write(config)

    return path


def start_process(command, name):
    log(f"Starting {name}...")
    process = subprocess.Popen(
        command,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    processes.append((name, process))
    return process


def shutdown(signum, frame):
    global running
    running = False
    log("Shutdown requested")


def main():
    global running

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    config = load_config()
    entity_id = config.get("entity_id", "").strip()
    airplay_name = config.get("airplay_name", "ESPHome AirPlay")
    audio_port = int(config.get("audio_port", 7000))

    if not entity_id:
        raise ValueError("Please configure entity_id")

    verify_entity(entity_id)

    if not os.path.exists(PIPE_PATH):
        os.mkfifo(PIPE_PATH)

    # Start HTTP audio streaming server.
    env = os.environ.copy()
    env["AUDIO_PORT"] = str(audio_port)

    log("Starting HTTP audio server...")
    audio_process = subprocess.Popen(
        [sys.executable, "/app/audio_server.py"],
        env=env,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    processes.append(("Audio Server", audio_process))

    config_path = create_shairport_config(airplay_name)

    start_process(
        ["shairport-sync", "-c", config_path],
        "Shairport-Sync",
    )

    log(f"AirPlay receiver: {airplay_name}")
    log(f"Target entity: {entity_id}")
    log(f"Audio HTTP port: {audio_port}")
    log("Bridge started")

    try:
        while running:
            for name, process in processes:
                if process.poll() is not None:
                    raise RuntimeError(
                        f"{name} exited with code {process.returncode}"
                    )
            time.sleep(1)
    finally:
        log("Stopping services...")
        for name, process in reversed(processes):
            if process.poll() is None:
                process.terminate()

        for name, process in reversed(processes):
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        log(f"ERROR: {error}")
        sys.exit(1)

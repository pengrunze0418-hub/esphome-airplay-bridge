
#!/usr/bin/env python3
"""HTTP streaming server for Shairport-Sync PCM output."""

import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PIPE_PATH = "/tmp/airplay_audio.pipe"
SAMPLE_RATE = 44100
CHANNELS = 2
BITS_PER_SAMPLE = 16


def wav_header():
    byte_rate = SAMPLE_RATE * CHANNELS * BITS_PER_SAMPLE // 8
    block_align = CHANNELS * BITS_PER_SAMPLE // 8

    # Streaming WAV with an unspecified practical length.
    return (
        b"RIFF"
        + (0xFFFFFFFF).to_bytes(4, "little")
        + b"WAVEfmt "
        + (16).to_bytes(4, "little")
        + (1).to_bytes(2, "little")
        + CHANNELS.to_bytes(2, "little")
        + SAMPLE_RATE.to_bytes(4, "little")
        + byte_rate.to_bytes(4, "little")
        + block_align.to_bytes(2, "little")
        + BITS_PER_SAMPLE.to_bytes(2, "little")
        + b"data"
        + (0xFFFFFFFF).to_bytes(4, "little")
    )


class AudioHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        if self.path != "/stream.wav":
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Content-Type", "audio/wav")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()

        try:
            self.wfile.write(wav_header())
            self.wfile.flush()

            with open(PIPE_PATH, "rb", buffering=0) as pipe:
                while True:
                    data = pipe.read(4096)
                    if not data:
                        break
                    self.wfile.write(data)
                    self.wfile.flush()

        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as error:
            print(f"Audio stream error: {error}", flush=True)

    def log_message(self, format, *args):
        print(f"[HTTP] {format % args}", flush=True)


def run_server(port=7000):
    server = ThreadingHTTPServer(("0.0.0.0", port), AudioHandler)
    print(f"Audio server listening on port {port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    port = int(os.environ.get("AUDIO_PORT", "7000"))
    run_server(port)

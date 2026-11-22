
#!/usr/bin/env bash
set -e

echo "================================"
echo " ESPHome AirPlay Bridge v0.1.0"
echo "================================"

mkdir -p /run/dbus

echo "[1/3] Starting D-Bus..."
dbus-daemon --system --fork

echo "[2/3] Starting Avahi..."
avahi-daemon --daemonize --no-chroot

echo "[3/3] Starting AirPlay Bridge..."
exec python3 /app/bridge.py

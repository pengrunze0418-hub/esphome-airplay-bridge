
#!/bin/sh
set -e

echo "================================"
echo " ESPHome AirPlay Bridge"
echo "================================"

echo "[DEBUG] Checking HA API credentials..."

if [ -n "${SUPERVISOR_TOKEN:-}" ]; then
    echo "[DEBUG] SUPERVISOR_TOKEN: available"
else
    echo "[DEBUG] SUPERVISOR_TOKEN: missing"
fi

if [ -n "${HASSIO_TOKEN:-}" ]; then
    echo "[DEBUG] HASSIO_TOKEN: available"
else
    echo "[DEBUG] HASSIO_TOKEN: missing"
fi

echo "[1/3] Starting D-Bus..."

mkdir -p /run/dbus

if [ ! -S /run/dbus/system_bus_socket ]; then
    rm -f /run/dbus/dbus.pid
    dbus-daemon --system --fork
fi

echo "[2/3] Skipping Avahi for testing..."

echo "[3/3] Starting AirPlay Bridge..."

exec python3 /app/bridge.py

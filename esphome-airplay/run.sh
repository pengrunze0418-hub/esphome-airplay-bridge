
#!/bin/sh
set -e

echo "================================"
echo " ESPHome AirPlay Bridge"
echo "================================"

echo "[1/4] Reading network configuration..."

NETWORK_INTERFACE="$(python3 -c 'import json; print(json.load(open("/data/options.json")).get("network_interface", "").strip())')"

if [ -z "$NETWORK_INTERFACE" ]; then
    echo "ERROR: Network interface is not configured!"
    exit 1
fi

case "$NETWORK_INTERFACE" in
    *[!a-zA-Z0-9_.:-]*)
        echo "ERROR: Invalid network interface name: $NETWORK_INTERFACE"
        exit 1
        ;;
esac

if ! ip link show dev "$NETWORK_INTERFACE" >/dev/null 2>&1; then
    echo "ERROR: Network interface not found: $NETWORK_INTERFACE"
    echo "Available interfaces:"
    ip link show
    exit 1
fi

echo "Using network interface: $NETWORK_INTERFACE"

echo "[2/4] Starting D-Bus..."

mkdir -p /run/dbus

if [ ! -S /run/dbus/system_bus_socket ]; then
    rm -f /run/dbus/dbus.pid
    dbus-daemon --system --fork
fi

echo "[3/4] Configuring Avahi..."

mkdir -p /etc/avahi

cat > /etc/avahi/avahi-daemon.conf <<EOF
[server]
host-name=esphome-airplay-bridge
domain-name=local
use-ipv4=yes
use-ipv6=no
allow-interfaces=$NETWORK_INTERFACE
ratelimit-interval-usec=1000000
ratelimit-burst=1000

[publish]
publish-addresses=yes
publish-hinfo=no
publish-workstation=no
publish-domain=no

[reflector]
enable-reflector=no

[rlimits]
EOF

echo "Avahi will use: $NETWORK_INTERFACE"

echo "Starting Avahi..."

avahi-daemon --no-chroot --debug &

sleep 2

echo "---- Network interfaces ----"
ip -4 addr show || true

echo "---- Avahi status ----"
timeout 3 avahi-browse -art 2>&1 || true

echo "---- UDP 5353 listeners ----"
ss -ulpn 2>&1 | grep 5353 || true

echo "[4/4] Starting AirPlay Bridge..."

exec python3 /app/bridge.py

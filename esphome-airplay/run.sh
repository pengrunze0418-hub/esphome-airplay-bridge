
#!/bin/sh
set -e

echo "================================"
echo " ESPHome AirPlay Bridge"
echo "================================"

echo "[1/4] Starting D-Bus..."
mkdir -p /run/dbus

if [ ! -S /run/dbus/system_bus_socket ]; then
    rm -f /run/dbus/dbus.pid
    dbus-daemon --system --fork
fi

echo "[2/4] Configuring Avahi..."
mkdir -p /etc/avahi

cat > /etc/avahi/avahi-daemon.conf <<'EOF'
[server]
host-name=esphome-airplay-bridge
domain-name=local
allow-interfaces=enp3s0
use-ipv4=yes
use-ipv6=no
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

echo "[2/4] Starting Avahi..."
avahi-daemon --no-chroot --debug &

echo "[3/4] Checking mDNS environment..."

echo "---- Network interfaces ----"
ip -4 addr show 2>&1 || true

echo "---- Avahi status ----"
timeout 3 avahi-browse -art 2>&1 || true

echo "---- UDP 5353 listeners ----"
ss -ulpn 2>&1 | grep 5353 || true

echo "[4/4] Starting AirPlay Bridge..."
exec python3 /app/bridge.py

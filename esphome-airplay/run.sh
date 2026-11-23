
#!/bin/sh
set -e

echo "================================"
echo " ESPHome AirPlay Bridge"
echo "================================"

echo "[1/3] Starting D-Bus..."

mkdir -p /run/dbus

if [ ! -S /run/dbus/system_bus_socket ]; then
    rm -f /run/dbus/dbus.pid
    dbus-daemon --system --fork
fi

echo "[2/3] Configuring Avahi..."

mkdir -p /etc/avahi

cat > /etc/avahi/avahi-daemon.conf <<'EOF'
[server]
host-name=esphome-airplay-bridge
domain-name=local
use-ipv4=yes
use-ipv6=no
allow-interfaces=
deny-interfaces=
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

echo "[2/3] Starting Avahi..."

avahi-daemon --daemonize --no-chroot

echo "[3/3] Starting AirPlay Bridge..."

exec python3 /app/bridge.py

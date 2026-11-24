# esphome-airplay-bridge
AirPlay receiver bridge for ESPHome media players via Home Assistant
## Step-by-Step Installation & Setup

### Step 1 — Prepare Your ESPHome Speaker

Make sure your ESPHome speaker is already connected to Home Assistant.

Your device must expose a `media_player` entity that supports audio playback and is accessible through the ESPHome Native API.

No AirPlay-specific firmware is required.

Compatible devices include:
- Custom-built ESPHome speakers.
- Ready-made speakers running ESPHome.
- Other ESPHome devices with compatible audio playback capabilities.

### Step 2 — Create a Long-Lived Access Token

AirPlay Bridge uses a Home Assistant Long-Lived Access Token to communicate with Home Assistant.

The token must be created manually.

1. Open Home Assistant.
2. Click your user profile in the bottom-left corner.
3. Scroll down to **Long-Lived Access Tokens**.
4. Click **Create Token**.
5. Enter a name, such as `AirPlay Bridge`.
6. Click **OK**.
7. Copy the generated token and store it somewhere safe.

**Important:** The token is only displayed in full when it is created. Do not share it or publish it in your GitHub repository.

### Step 3 — Add the Repository

1. Open Home Assistant.
2. Navigate to **Settings → Apps**.
3. Open the App Store.
4. Click the three-dot menu in the upper-right corner.
5. Select **Repositories**.
6. Add the AirPlay Bridge GitHub repository URL. 'https://github.com/pengrunze0418-hub/esphome-airplay-bridge'
7. Click **Add**.

### Step 4 — Install AirPlay Bridge

1. Find **ESPHome AirPlay Bridge** in the App Store.
2. Open the add-on page.
3. Click **Install**.
4. Wait for the installation to finish.

### Step 5 — Configure the Network Interface

Enter the network interface used by your Home Assistant OS host to connect to your local network.

Examples:
- `enp3s0` — Wired Ethernet.
- `wlp1s0` — Wi-Fi.
- `eth0` — Common Ethernet interface name.

**Important:** The interface name must match an actual network interface on your Home Assistant OS host. The add-on uses this interface for mDNS and AirPlay device discovery.

### Step 6 — Configure the Home Assistant Media Player

Enter the entity ID of your target ESPHome speaker.

For example:

`media_player.my_esphome_speaker`

You can find the entity ID under **Settings → Devices & Services → Entities**.

### Step 7 — Enter Your Long-Lived Access Token

Paste the token created in Step 2 into the `ha_token` configuration field.

Make sure there are no extra spaces before or after the token.

### Step 8 — Set Your AirPlay Receiver Name

Choose a name for your AirPlay receiver.

For example:

`Bedroom Speaker`

This is the name that will appear in the AirPlay device list on your Mac, iPhone, or iPad.

### Step 9 — Start the Add-on

1. Save your configuration.
2. Start ESPHome AirPlay Bridge.
3. Open the add-on logs.
4. Check that the bridge and Shairport-Sync start successfully.

### Step 10 — Test AirPlay

1. Connect your Apple device to the same local network.
2. Open the AirPlay output selector.
3. Find the receiver name you configured.
4. Select it and start playing music.

Your audio should now be forwarded to your ESPHome speaker through Home Assistant.

---

## Troubleshooting

| Problem | What to check |
|---|---|
| AirPlay receiver does not appear | Network interface, mDNS, and local network connectivity |
| AirPlay connects but there is no sound | Media player entity ID, access token, and player compatibility |
| Add-on fails to start | Configuration values and add-on logs |
| Audio playback stops unexpectedly | ESPHome media player compatibility and audio forwarding |

## Notes

- Home Assistant OS (HAOS) is the currently tested platform.
- A valid Long-Lived Access Token is required.
- The ESPHome speaker must support audio playback through its Home Assistant `media_player` entity.
- Some startup audio latency is expected due to the audio forwarding pipeline.

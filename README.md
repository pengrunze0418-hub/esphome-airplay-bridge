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
6. Add the AirPlay Bridge GitHub repository URL.
7. Click **Add**.

### Step 4 — Install AirPlay Bridge

1. Find **ESPHome AirPlay Bridge** in the App Store.
2. Open the add-on page.
3. Click **Install**.
4. Wait for the installation to finish.

### Step 5 — Configure the Network Interface

Enter the network interface used by your Home Assistant OS host to connect to your local network.

Examples

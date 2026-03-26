Prerequisites

1. Home Assistant (Core 2024.1 or newer recommended)
2. HACS (Home Assistant Community Store) installed.
3. Your Force H3X Inverter/Hub connected to your local network (LAN/WLAN).
4. Static IP assigned to your Pylontech H3X via your router.
5. Modbus TCP enabled on the inverter (Default Port is usually 502).

Installation via HACS Custom Repository (Recommended)

1. Open Home Assistant and navigate to HACS.
2. Click the three dots (top right) and select Custom repositories.
3. Add the URL of this repository.
4. Select Integration as the category and click Add.
5. Find Pylontech H3X Modbus in HACS and click Download.
6. Restart Home Assistant.

Configuration

This integration supports configuration entirely via the Home Assistant UI (Config Flow). No YAML editing required!

1. Go to Settings > Devices & Services.
2. Click + Add Integration in the bottom right.
3. Search for Solar Hub Modbus.
4. Enter your connection details:
    • Host: The IP address of your Force H3X (e.g., 192.168.1.10).
    • Port: 502.
    • Scan Interval: Polling frequency in seconds (Default: 10, can be lowered to 5 for near-real-time tracking).
5. Click Submit.

Changing the Scan Interval Later

Want faster updates? You can change the polling rate on the fly:

Go to the integration on the Devices & Services page.
Click Configure.

Update the scan_interval (e.g., set to 5). The integration will instantly reload and apply the new rate.

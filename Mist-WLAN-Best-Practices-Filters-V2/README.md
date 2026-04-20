# Juniper Mist WLAN Best Practices Automation

This script connects to the Juniper Mist cloud API and automatically checks all of your organisation's wireless networks (WLANs) against a set of best practices. It tells you which networks are not configured correctly, explains why each setting matters, and gives you the option to fix them on the spot. It also tracks how many clients are connected and reports on the connection success rate (SLE) across all your sites.

---

## What it checks

| Check | What it looks for |
|---|---|
| **ARP Filtering** | ARP filtering should be turned on to reduce broadcast traffic on the wireless network |
| **Multicast / Broadcast Filtering** | Broadcast filtering should be enabled to cut down unnecessary traffic that every client has to receive |
| **IPv6 NDP** | IPv6 Neighbor Discovery should be disabled unless the network is specifically designed for IPv6 clients |
| **802.11r Fast Transition** | Fast roaming should be enabled on enterprise (WPA2/WPA3) networks so devices hand off between access points quickly |
| **Duplicate SSID Names** | Each wireless network name should be unique across the org to avoid client confusion |

---

## Requirements

- **Python 3.8 or higher**
- The `requests` library — used to talk to the Mist API
- The `openpyxl` library — used to create the Excel report (optional but recommended)

Install both with:

```
pip install requests openpyxl
```

You will also need a **Juniper Mist SuperUser API token** for your organisation. You can generate one in the Mist portal under Organisation → Settings → API Tokens.

---

## How to run it

### Interactive mode (recommended for first-time use)

Run the script and answer the prompts:

```
python mist_wlan_best_practices-V2.py
```

or explicitly:

```
python mist_wlan_best_practices-V2.py --main
```

The script will ask you to:
1. Choose which Mist cloud region your org is on
2. Enter your Org ID (a UUID found in Mist under Organisation → Settings)
3. Enter your SuperUser API token (input is hidden)

It will then work through each step automatically, pausing to ask your permission before making any changes.

### Automated / scheduled mode

For unattended nightly runs, use `--auto`. In this mode the script reads credentials from environment variables and applies all best-practice fixes without prompting:

```
python mist_wlan_best_practices-V2.py --auto
```

Set these environment variables before running:

| Variable | Value |
|---|---|
| `MIST_CLOUD` | Cloud number 1–6 (see table below). Defaults to `1` if not set |
| `MIST_ORG_ID` | Your Mist Org ID (UUID format) |
| `MIST_TOKEN` | Your SuperUser API token |

**Cloud numbers:**

| Number | Region |
|---|---|
| 1 | Global 01 — US (api.mist.com) |
| 2 | Global 02 (api.gc1.mist.com) |
| 3 | Europe (api.eu.mist.com) |
| 4 | APAC AC2 (api.ac2.mist.com) |
| 5 | APAC AC5 (api.ac5.mist.com) |
| 6 | Canada (api.ca.mist.com) |

**Linux / macOS — cron example (runs every night at midnight):**

```
0 0 * * * MIST_CLOUD=1 MIST_ORG_ID=your-org-id MIST_TOKEN=your-token python3 /path/to/mist_wlan_best_practices-V2.py --auto
```

**Windows Task Scheduler:**

Create a task that runs:
```
python "C:\path\to\mist_wlan_best_practices-V2.py" --auto
```
with `MIST_CLOUD`, `MIST_ORG_ID`, and `MIST_TOKEN` set as system or user environment variables.

---

## What happens when you run it

1. The script authenticates and pulls a list of all your sites and enabled org-level WLANs.
2. It counts connected wireless clients at each site.
3. It fetches the Successful Connect SLE (Service Level Expectation) score for every site over the last 24 hours. Sites below 90% are flagged.
4. It checks every enabled WLAN against the best practices listed above.
5. A summary table is printed showing PASS / FAIL / N/A for each check.
6. For each failing WLAN, the script describes the problem and — in interactive mode — asks if you want to fix it.
7. After any changes, it waits 30 seconds and re-checks client counts and SLE to confirm nothing was disrupted.
8. An Excel report is saved to the same folder as the script.

---

## Output files

| File | Description |
|---|---|
| `mist_bp_report_<timestamp>.xlsx` | Excel report with three tabs: all WLANs vs best practices, non-compliant WLANs only, and site SLE summary |
| `logs/mist_bp_<timestamp>.log` | Human-readable run log |
| `logs/mist_bp_debug_<timestamp>.log` | Detailed debug log including every API call made |

---

## Notes

- The script only reads and optionally updates **org-level WLANs**. It does not modify site-level WLANs or any other configuration.
- No changes are made without your confirmation in interactive mode.
- The 802.11r Fast Transition check only applies to enterprise SSIDs (WPA2/WPA3 with 802.1X authentication). It is skipped (shown as N/A) for open or pre-shared key networks.
- If a site shows no SLE data, it likely means SLE is not licensed or has not been configured for that site in the Mist portal.
- The script respects Mist API rate limits (2,000 calls per hour) and will automatically pause if the limit is approached.

---

## Repository structure

```
Mist-WLAN-Best-Practices-Filters-V2/
├── mist_wlan_best_practices-V2.py   # Main script
├── __main__.py                      # Allows running with: python -m <folder>
├── README.md                        # This file
└── logs/                            # Created automatically on first run
```

---

## License

This project is provided as-is for internal use. Please review the Juniper Mist API terms of service before deploying in a production environment.

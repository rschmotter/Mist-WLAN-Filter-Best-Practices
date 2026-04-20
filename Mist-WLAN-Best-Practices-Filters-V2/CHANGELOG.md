# Changelog

All notable changes to this project will be documented here.

---

## [2.0.0] - 2026-04-20

### Added
- `--main` flag for explicitly invoking interactive mode (counterpart to `--auto`)
- `__main__.py` so the folder can be run directly with `python -m <folder>`
- `.env.example` template for configuring automated runs without hard-coding credentials
- `.gitignore` to prevent logs, Excel reports, and credential files from being committed
- `requirements.txt` listing `requests` and `openpyxl` dependencies
- MIT `LICENSE` file

### Changed
- Removed **Data Rates / 802.11b** best practice check — data rate configuration is managed at the RF Template level in Mist and cannot be reliably audited or remediated via the WLAN API
- Removed **Site WLAN listing and deletion** section — scope narrowed to org-level WLAN auditing and remediation only
- `--auto` and `--main` are now mutually exclusive arguments in argparse

### Best Practices Checked (v2.0.0)
1. ARP Filtering
2. Multicast / Broadcast Filtering
3. IPv6 NDP Disabled
4. 802.11r Fast Transition (enterprise SSIDs only)
5. No Duplicate SSID Names

---

## [1.0.0] - Initial release

- First version of the Mist WLAN Best Practices script
- Checked ARP filtering, broadcast filtering, IPv6 NDP, data rates, 802.11r FT, and duplicate SSIDs
- Interactive mode with per-WLAN, per-check remediation prompts
- Excel report export with org WLAN, non-compliant WLAN, and site SLE tabs
- Site WLAN listing and deletion
- Auto mode via environment variables

from scapy.all import rdpcap, UDP
import folium
import re
from pathlib import Path

# === CONFIG ===
PCAP_NAME = "log.pcap"
ZOOM = 16

# Get absolute path to the pcap file, relative to this script
BASE_DIR = Path(__file__).resolve().parent
PCAP_FILE = BASE_DIR / PCAP_NAME
MAP_OUT = BASE_DIR / "gps_flag_solve.html"

# === REGEX for GPGGA parsing ===
GPGGA_RE = re.compile(
    r"\$GPGGA,[^,]*,"               # Time
    r"(\d{2})(\d{2}\.\d+),([NS]),"  # Latitude
    r"(\d{3})(\d{2}\.\d+),([EW]),"  # Longitude
)

def nmea_to_decimal(deg, minutes, direction):
    val = float(deg) + float(minutes) / 60.0
    return -val if direction in ["S", "W"] else val

def parse_gpgga(nmea_str):
    match = GPGGA_RE.search(nmea_str)
    if not match:
        return None
    lat_deg, lat_min, lat_dir, lon_deg, lon_min, lon_dir = match.groups()
    lat = nmea_to_decimal(lat_deg, lat_min, lat_dir)
    lon = nmea_to_decimal(lon_deg, lon_min, lon_dir)
    return (lat, lon)

def main():
    # === STEP 1: Check and load PCAP ===
    if not PCAP_FILE.exists():
        raise FileNotFoundError(f"PCAP not found at: {PCAP_FILE}")
    print(f"[+] Reading PCAP from: {PCAP_FILE}")

    packets = rdpcap(str(PCAP_FILE))
    gps_coords = []

    # === STEP 2: Extract GPS coordinates ===
    for pkt in packets:
        if UDP in pkt and pkt.haslayer("Raw"):
            raw = pkt["Raw"].load.decode(errors="ignore")
            if "$GPGGA" in raw:
                coord = parse_gpgga(raw)
                if coord:
                    gps_coords.append(coord)

    if not gps_coords:
        raise ValueError("No valid GPS coordinates found in the PCAP.")

    print(f"[+] Extracted {len(gps_coords)} GPS points")

    # === STEP 3: Plot to folium ===
    m = folium.Map(location=gps_coords[0], zoom_start=ZOOM)
    folium.PolyLine(gps_coords, color='red', weight=3).add_to(m)

    m.save(str(MAP_OUT))
    print(f"[+] Map written to: {MAP_OUT}")

if __name__ == "__main__":
    main()

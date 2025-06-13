from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import sys
import folium
from scapy.all import IP, UDP, Raw, wrpcap
from datetime import datetime
from pathlib import Path

DEBUG = True

FLAG = "flag{y0u_f0und_m3}"
FONT = FontProperties(family="Liberation Sans", weight="bold")
ORIGIN = (51.501604, -2.546892)  # (lat, lon)
SIZE = 1                         # TextPath size (unitless)
SCALE = 0.0002                   # Real-world scale for GPS mapping
OUTPUT = "log.pcap"
BASE_DIR = Path(__file__).resolve().parent

def generate_path(): 
    tp = TextPath((0, 0), FLAG, size=SIZE, prop=FONT)

    coords = [(ORIGIN[0] + y * SCALE, ORIGIN[1] + x * SCALE) for x, y in tp.vertices]
    return coords

def plot_to_verify():
    coords = generate_path()

    # Matplotlib preview: longitude as x, latitude as y so orientation matches the folium/map view
    lats = [c[0] for c in coords]
    lons = [c[1] for c in coords]
    plt.figure()
    plt.plot(lons, lats, linewidth=1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Flag shape in GPS coordinates (matches Folium)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.show()

    # Folium map
    m = folium.Map(location=ORIGIN, zoom_start=17)
    folium.PolyLine(coords, color='red', weight=3).add_to(m)
    folium.Marker(coords[0], popup="Start").add_to(m)
    folium.Marker(coords[-1], popup="End").add_to(m)
    m.save(BASE_DIR / "flag_path_map.html")
    print("Saved to flag_path_map.html")

def to_nmea(lat, lon):
    def deg_to_nmea(val, is_lat):
        degrees = int(abs(val))
        minutes = (abs(val) - degrees) * 60
        if is_lat:
            return f"{degrees:02d}{minutes:07.4f}"
        else:
            return f"{degrees:03d}{minutes:07.4f}"

    lat_str = deg_to_nmea(lat, True)
    lat_dir = 'N' if lat >= 0 else 'S'
    lon_str = deg_to_nmea(lon, False)
    lon_dir = 'E' if lon >= 0 else 'W'

    time = datetime.utcnow()
    timestr = f"{time.hour:02d}{time.minute:02d}{time.second:02d}.{int(time.microsecond / 1000):03d}"

    return f"$GPGGA,{timestr},{lat_str},{lat_dir},{lon_str},{lon_dir},1,08,0.9,70.8,M,46.9,M,,0000*47"

def write_coords_to_pcap(coords, output_file):
    packets = []
    for lat, lon in coords:
        nmea = to_nmea(lat, lon)
        payload = Raw(load=nmea.encode())

        packet = IP(dst="10.10.10.25", src="10.10.10.10") / UDP(dport=1337, sport=4444) / payload
        packets.append(packet)

    wrpcap(str(output_file), packets, append=False)
    print(f"PCAP written to {output_file}")

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        FLAG = sys.argv[1]
        if len(sys.argv) >= 3:
            OUTPUT = sys.argv[2]

    if DEBUG:
        plot_to_verify()

    coords = generate_path()
    write_coords_to_pcap(coords, BASE_DIR / OUTPUT)

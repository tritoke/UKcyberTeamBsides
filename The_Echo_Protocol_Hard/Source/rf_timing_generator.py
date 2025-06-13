#!/usr/bin/env python3
"""
RF Timing Challenge Generator
============================
Generates PCAP files encoding binary data in ICMP packet inter-arrival times.

Encoding scheme:
- Bit 0: 0.12s timing gap
- Bit 1: 0.28s timing gap  
- Byte separator: 0.80s timing gap

Features:
- Configurable packet loss simulation
- Noise injection with duplicate packets
- Optional MD5 hash verification for corrupted flags
- Suitable for CTF forensics challenges

Usage:
  python3 rf_timing_generator.py --flag "FLAG{EXAMPLE}" --outfile challenge.pcap
  python3 rf_timing_generator.py --flag-file flag.txt --outfile challenge.pcap
  python3 rf_timing_generator.py --flag "FLAG{HARD}" --loss 0.03 --hash --outfile hard.pcap
"""
import argparse, random, time, os, re
from scapy.all import IP, ICMP, Raw, wrpcap

#Timing (seconds)
SHORT = 0.12   #bit 0
LONG  = 0.28   #bit 1
BYTE_GAP  = 0.80
DUP_JITTER_MIN = 0.004
DUP_JITTER_MAX = 0.015

def parse_flag_file(flag_file_path):
    """Parse a CTF flag file in the format {FLAG^:actual_flag}.
    
    Args:
        flag_file_path (str): Path to the flag file
        
    Returns:
        str: The extracted flag text
        
    Raises:
        FileNotFoundError: If the flag file doesn't exist
        ValueError: If the flag file format is invalid
    """
    try:
        with open(flag_file_path, 'r') as f:
            content = f.read().strip()
            
        #Match the CTF flag file format: {FLAG^:actual_flag}
        match = re.match(r'\{FLAG\^:(.*)\}', content)
        if match:
            return match.group(1)
        else:
            raise ValueError(f"Invalid flag file format. Expected {{FLAG^:FLAG{{...}}}} but got: {content}")
                
    except FileNotFoundError:
        raise FileNotFoundError(f"Flag file not found: {flag_file_path}")
    except Exception as e:
        raise ValueError(f"Error reading flag file {flag_file_path}: {e}")

def generate_noise_ip(noise_subnets):
    subnet = random.choice(noise_subnets)
    
    # Handle range format: "10.0.0.21-50"
    if '-' in subnet and '/' not in subnet:
        try:
            base, range_part = subnet.rsplit('.', 1)
            start, end = map(int, range_part.split('-'))
            last_octet = random.randint(start, end)
            return f"{base}.{last_octet}"
        except:
            pass
    
    # Handle CIDR format: "192.168.1.0/24"
    if '/' in subnet:
        try:
            import ipaddress
            network = ipaddress.IPv4Network(subnet, strict=False)
            # Get a random IP from the network (excluding network and broadcast)
            hosts = list(network.hosts())
            if hosts:
                return str(random.choice(hosts))
        except:
            pass
    
    # Handle single IP or fallback
    if '.' in subnet and '-' not in subnet and '/' not in subnet:
        return subnet
    
    # Fallback to default behavior
    return f"10.0.0.{random.randint(21, 50)}"

def generate(flag: str, outfile: str, src="10.0.0.10", dst="10.0.0.20", noise_subnets=None, seed=None, noise=300, loss=0.0, dup=0.02, include_hash=False):
    if seed is None:
        seed = int(time.time())
    random.seed(seed)
    
    # Default noise subnets if none specified
    if noise_subnets is None:
        noise_subnets = ["10.0.0.21-50"]

    pkts = []
    t0 = time.time()
    t = t0
    seq = 1

    def emit(tt: float, idv=0xBEEF, s=src, d=dst, payload_len=None):
        nonlocal seq
        if payload_len is None:
            payload_len = random.randint(32, 64)
        p = IP(src=s, dst=d)/ICMP(type=8, id=idv, seq=seq)/Raw(os.urandom(payload_len))
        p.time = tt
        pkts.append(p)
        seq += 1

    #initial reference packet
    emit(t)

    data = flag.encode("utf-8")

    for b in data:
        #8 bits MSB-first
        for bit in range(7, -1, -1):
            delta = SHORT if ((b >> bit) & 1) == 0 else LONG
            t += delta
            emit(t)
        #explicit byte-gap marker: exactly BYTE_GAP later
        t += BYTE_GAP
        emit(t)

    #Automatically include hash when packet loss is configured, or if explicitly requested
    #If hash verification requested, send hash as packet payload (not timing-encoded)
    should_include_hash = include_hash or (loss > 0.0)
    if should_include_hash:
        import hashlib
        flag_hash = hashlib.md5(flag.encode('utf-8')).hexdigest()
        print(f"[+] Flag hash (MD5): {flag_hash}")
        
        #Send hash as packet payload after a brief delay
        t += 2.0  #2 second gap before hash packet
        hash_payload = f"FLAG_HASH:{flag_hash}".encode('utf-8')
        p = IP(src=src, dst=dst)/ICMP(type=8, id=0xBABE, seq=9999)/Raw(hash_payload)
        p.time = t
        pkts.append(p)

    #Noise (different dst)
    for _ in range(noise):
        tt = t0 + random.uniform(0, max(0.001, t - t0))
        noise_dst = generate_noise_ip(noise_subnets)
        n = IP(src=src, dst=noise_dst)/ICMP(type=8, id=random.randint(0,0xFFFF), seq=random.randint(1,65535))/Raw(os.urandom(random.randint(16,64)))
        n.time = tt
        pkts.append(n)

    #Loss
    if loss > 0:
        pkts = [p for p in pkts if random.random() > loss]

    #Duplicates with tiny jitter
    if dup > 0:
        dups = []
        for p in pkts:
            if p.haslayer(ICMP) and p[ICMP].type == 8 and p[IP].src == src and p[IP].dst == dst and getattr(p[ICMP], 'id',0)==0xBEEF:
                if random.random() < dup:
                    q = p.copy()
                    q.time += random.uniform(DUP_JITTER_MIN, DUP_JITTER_MAX)
                    dups.append(q)
        pkts.extend(dups)

    pkts.sort(key=lambda x: x.time)
    wrpcap(outfile, pkts)
    print(f"[+] Wrote {outfile} seed={seed} noise={noise} loss={loss} dup={dup}")
    
    #Show hash verification status
    should_include_hash = include_hash or (loss > 0.0)
    if should_include_hash:
        if loss > 0.0 and not include_hash:
            print(f"[+] Hash verification automatically included due to packet loss")
        else:
            print(f"[+] Hash verification included for advanced packet loss challenges")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="RF Timing Challenge Generator - Encode flags in ICMP packet timing",
        epilog="Examples:\n"
               "  %(prog)s --flag 'FLAG{EXAMPLE}' --outfile challenge.pcap\n"
               "  %(prog)s --flag-file flag.txt --outfile challenge.pcap\n"
               "  %(prog)s --flag 'FLAG{HARD}' --loss 0.03 --outfile hard.pcap\n"
               "  %(prog)s --flag 'FLAG{CUSTOM}' --src 192.168.1.10 --dst 192.168.1.20 --outfile custom.pcap\n"
               "  %(prog)s --flag 'FLAG{MULTI}' --noise-subnets '10.0.0.21-50' '192.168.1.0/24' --outfile multi.pcap\n"
               "  %(prog)s --flag 'FLAG{RANGE}' --noise-subnets '172.16.0.100-200' --outfile range.pcap",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Flag input options - mutually exclusive
    flag_group = ap.add_mutually_exclusive_group(required=True)
    flag_group.add_argument("--flag", help="Flag to encode in timing")
    flag_group.add_argument("--flag-file", help="Path to CTF flag file (format: {FLAG^:FLAG{...}})")
    
    ap.add_argument("--outfile", default="challenge.pcap", help="Output PCAP file (default: challenge.pcap)")
    ap.add_argument("--src", default="10.0.0.10", help="Source IP address (default: 10.0.0.10)")
    ap.add_argument("--dst", default="10.0.0.20", help="Destination IP address (default: 10.0.0.20)")
    ap.add_argument("--noise-subnets", nargs='+', default=["10.0.0.21-50"], 
                    help="Noise destination subnets. Supports: '10.0.0.21-50' (range), '192.168.1.0/24' (CIDR), '172.16.0.100' (single IP). Multiple values allowed (default: ['10.0.0.21-50'])")
    ap.add_argument("--seed", type=int, default=None, help="Random seed for reproducible results")
    ap.add_argument("--noise", type=int, default=300, help="Number of noise packets (default: 300)")
    ap.add_argument("--loss", type=float, default=0.00, help="Packet loss probability 0.0-1.0 (default: 0.0)")
    ap.add_argument("--dup", type=float, default=0.02, help="Duplicate packet probability (default: 0.02)")
    ap.add_argument("--hash", action="store_true", help="Force MD5 hash inclusion (automatically included when loss > 0)")
    args = ap.parse_args()
    
    # Determine flag source
    if args.flag_file:
        try:
            flag = parse_flag_file(args.flag_file)
            print(f"[+] Flag loaded from file: {args.flag_file}")
        except (FileNotFoundError, ValueError) as e:
            print(f"[!] Error loading flag file: {e}")
            exit(1)
    else:
        flag = args.flag
    
    generate(flag, args.outfile, src=args.src, dst=args.dst, noise_subnets=args.noise_subnets, seed=args.seed, noise=args.noise, loss=args.loss, dup=args.dup, include_hash=args.hash)
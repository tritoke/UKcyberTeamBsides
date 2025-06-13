#!/usr/bin/env python3
#RF decoder for hard challenges that include packet loss, uses maths to guess missing packets
"""
Usage:
  python3 rf_timing_decoder.py challenge.pcap
  python3 rf_timing_decoder.py challenge.pcap --debug
"""
import argparse
from collections import defaultdict
from scapy.all import rdpcap, IP, ICMP, Raw

def extract_hash_from_packets(pkts): #get flag hash to check answer is correct
    for p in pkts:
        if p.haslayer(ICMP) and p.haslayer(Raw):
            payload = p[Raw].load
            try:
                payload_str = payload.decode('utf-8', errors='ignore')
                if payload_str.startswith('FLAG_HASH:'):
                    hash_value = payload_str.split('FLAG_HASH:')[1].strip()
                    return hash_value
            except:
                continue
    return None

#Exact timing constants from generator (hard coded, could be calculated)
BIT_0_TIME = 0.12
BIT_1_TIME = 0.28
BYTE_SEP_TIME = 0.80

#Tolerance for timing
TOLERANCE = 0.02

def choose_flow(pkts, src=None, dst=None, icmp_id=None): #find correct packet flow (conversation)
    flows = defaultdict(list)
    for p in pkts:
        if p.haslayer(ICMP) and p[ICMP].type == 8 and p.haslayer(IP):
            s, d = p[IP].src, p[IP].dst
            i = getattr(p[ICMP], 'id', None)
            if (src and s != src) or (dst and d != dst) or (icmp_id is not None and i != icmp_id):
                continue
            flows[(s,d,i)].append(p)
    
    if not flows:
        return None, []
    
    #Choose flow with most packets - works for this chall
    best = max(flows.items(), key=lambda kv: len(kv[1]))
    key, arr = best
    return key, arr

def dedup_packets(arr): #remove dupes
    seq_groups = defaultdict(list)
    for p in arr:
        seq = int(getattr(p[ICMP], 'seq', 0))
        seq_groups[seq].append(p)
    
    result = []
    for seq in sorted(seq_groups.keys()):
        packets = seq_groups[seq]
        #keep earliest timestamp
        earliest = min(packets, key=lambda x: x.time)
        result.append(earliest)
    
    return result

def detect_gaps(arr):#find gaps/ missing packets (guess packet loss?)
    sequences = [int(getattr(p[ICMP], 'seq', 0)) for p in arr]
    gaps = []
    
    for i in range(len(sequences) - 1):
        seq_a, seq_b = sequences[i], sequences[i+1]
        missing_count = seq_b - seq_a - 1
        
        if missing_count > 0:
            time_delta = float(arr[i+1].time) - float(arr[i].time)
            gaps.append({
                'after_index': i,
                'missing_count': missing_count,
                'time_delta': time_delta,
                'seq_before': seq_a,
                'seq_after': seq_b
            })
    
    return gaps

def mathematical_reconstruction(time_delta, missing_count, debug=False):
    if debug:
        print(f"  [MATH] Reconstructing {missing_count} missing seq numbers from {time_delta:.3f}s")
    
    #Try all possible combinations that could fit the timing
    from itertools import product
    
    choices = [BIT_0_TIME, BIT_1_TIME, BYTE_SEP_TIME]
    choice_names = [0, 1, 'SEP']
    
    best_combo = None
    best_error = float('inf')
    
    #Try combinations of different lengths (the missing_count might not be exact due to separator packets)
    for length in range(1, missing_count + 3):  #Allow some flexibility
        for combo in product(range(3), repeat=length):
            total_time = sum(choices[c] for c in combo)
            error = abs(total_time - time_delta)
            
            if error < best_error:
                best_error = error
                best_combo = [choice_names[c] for c in combo]
    
    #Also try some common exact combinations
    common_combos = [
        ([0], BIT_0_TIME),
        ([1], BIT_1_TIME), 
        (['SEP'], BYTE_SEP_TIME),
        ([0, 1], BIT_0_TIME + BIT_1_TIME),
        ([1, 0], BIT_1_TIME + BIT_0_TIME),
        ([0, 'SEP'], BIT_0_TIME + BYTE_SEP_TIME),
        ([1, 'SEP'], BIT_1_TIME + BYTE_SEP_TIME),
        ([0, 0], BIT_0_TIME + BIT_0_TIME),
        ([1, 1], BIT_1_TIME + BIT_1_TIME)
    ]
    
    for combo, expected_time in common_combos:
        error = abs(expected_time - time_delta)
        if error < best_error:
            best_error = error
            best_combo = combo
    
    if debug:
        expected = sum(BIT_0_TIME if x == 0 else BIT_1_TIME if x == 1 else BYTE_SEP_TIME for x in best_combo)
        print(f"    [MATH] Best: {best_combo} -> {expected:.3f}s (error: {best_error:.3f}s)")
    
    return best_combo

def decode_mathematical(path, src=None, dst=None, icmp_id=None, debug=False):    
    #Load and filter packets
    pkts = rdpcap(path)
    
    #Extract hash from packet payloads (separate from timing data)
    hash_from_packets = extract_hash_from_packets(pkts)
    
    key, arr = choose_flow(pkts, src, dst, icmp_id)
    
    if not arr:
        raise RuntimeError("No ICMP Echo flow found")
    
    s, d, i = key
    if debug:
        print(f"[FLOW] {s} -> {d}, ID: {i}")
    
    #Remove duplicates
    arr = dedup_packets(arr)
    if debug:
        print(f"[DEDUP] {len(arr)} packets after deduplication")
        sequences = [getattr(p[ICMP], 'seq', 0) for p in arr]
        print(f"[PACKETS] Sequence numbers: {sequences}")
        
        #Check if we're missing the beginning
        if sequences[0] > 1:
            print(f"[WARNING] Missing packets at beginning! Starting from seq {sequences[0]} instead of 1")
            print(f"[WARNING] Missing {sequences[0] - 1} packets at start - this will cause decoding errors")
    
    #Detect gaps
    gaps = detect_gaps(arr)
    if debug and gaps:
        print(f"[GAPS] Found {len(gaps)} gaps:")
        for g in gaps:
            print(f"  After packet {g['after_index']} (seq {g['seq_before']}): {g['missing_count']} missing, {g['time_delta']:.3f}s")
    
    #Check for missing packets at the beginning
    sequences = [getattr(p[ICMP], 'seq', 0) for p in arr]
    if sequences[0] > 1:
        missing_at_start = sequences[0] - 1
        if debug:
            print(f"[RECONSTRUCTION] Need to handle {missing_at_start} missing packets at start")
        
        #For now, we can't reconstruct the beginning without timing information
        #This is a fundamental limitation - we need at least the reference packet
        if missing_at_start >= 1:
            if debug:
                print(f"[ERROR] Cannot reconstruct beginning - missing reference packet(s)")
            raise RuntimeError(f"Cannot reconstruct flag: missing {missing_at_start} packets at beginning (including reference packet)")
    
    #Build complete packet sequence with reconstruction
    complete_sequence = []
    gap_map = {g['after_index']: g for g in gaps}
    
    if debug:
        print(f"\n[TIMING ANALYSIS] Processing {len(arr)-1} deltas:")
    
    #Calculate deltas and reconstruct
    for i in range(len(arr) - 1):
        #Add current packet delta (between i and i+1)
        time_delta = float(arr[i+1].time) - float(arr[i].time)
        seq_before = getattr(arr[i][ICMP], 'seq', 0)
        seq_after = getattr(arr[i+1][ICMP], 'seq', 0)
        
        if debug:
            print(f"  Delta {i}: seq {seq_before} -> {seq_after}, time {time_delta:.3f}s", end="")
        
        if i in gap_map:
            #This delta spans missing packets - reconstruct them
            gap_info = gap_map[i]
            if debug:
                print(f" [GAP: {gap_info['missing_count']} missing]")
            
            reconstructed = mathematical_reconstruction(
                gap_info['time_delta'], 
                gap_info['missing_count'], 
                debug
            )
            
            #Add all reconstructed elements in order
            #The gap represents what was lost between seq_before and seq_after
            complete_sequence.extend(reconstructed)
            
            if debug:
                print(f"    -> Reconstructed: {reconstructed}")
        else:
            #Normal delta - classify directly
            if abs(time_delta - BIT_0_TIME) < TOLERANCE:
                result_item = 0
                if debug:
                    print(f" -> BIT 0")
            elif abs(time_delta - BIT_1_TIME) < TOLERANCE:
                result_item = 1
                if debug:
                    print(f" -> BIT 1")
            elif abs(time_delta - BYTE_SEP_TIME) < TOLERANCE:
                result_item = 'SEP'
                if debug:
                    print(f" -> BYTE SEP")
            else:
                #Closest match for noisy timing
                distances = [
                    (abs(time_delta - BIT_0_TIME), 0),
                    (abs(time_delta - BIT_1_TIME), 1),
                    (abs(time_delta - BYTE_SEP_TIME), 'SEP')
                ]
                result_item = min(distances)[1]
                if debug:
                    print(f" -> {result_item} (CLOSEST MATCH, error: {min(distances)[0]:.3f}s)")
            
            complete_sequence.append(result_item)
    
    if debug:
        print(f"\n[SEQUENCE] Complete sequence: {complete_sequence}")
    
    #Convert bits to bytes with detailed tracking
    bytes_out = []
    current_bits = []
    byte_index = 0
    
    if debug:
        print(f"\n[BYTE CONVERSION] Converting sequence to bytes:")
    
    for seq_index, item in enumerate(complete_sequence):
        if item == 'SEP':
            #End of byte
            if current_bits:
                #Pad to 8 bits if needed
                original_length = len(current_bits)
                while len(current_bits) < 8:
                    current_bits.append(0)
                
                #Convert to byte (MSB first)
                byte_val = 0
                for j, bit in enumerate(current_bits[:8]):
                    if bit == 1:
                        byte_val |= (1 << (7 - j))
                
                #Debug the byte conversion
                if debug:
                    binary_str = ''.join(str(b) for b in current_bits[:8])
                    char = chr(byte_val) if 32 <= byte_val <= 126 else '?'
                    padding_info = f" (padded {8-original_length} bits)" if original_length < 8 else ""
                    print(f"  Byte {byte_index}: {binary_str} = 0x{byte_val:02x} = '{char}'{padding_info}")
                
                bytes_out.append(byte_val)
                current_bits = []
                byte_index += 1
            else:
                if debug:
                    print(f"  Empty byte separator at sequence index {seq_index}")
        else:
            #Add bit
            current_bits.append(item)
            if debug and len(current_bits) == 1:
                print(f"  Starting byte {byte_index} at sequence index {seq_index}")
    
    #Handle any remaining bits
    if current_bits:
        original_length = len(current_bits)
        while len(current_bits) < 8:
            current_bits.append(0)
        byte_val = 0
        for j, bit in enumerate(current_bits[:8]):
            if bit == 1:
                byte_val |= (1 << (7 - j))
        
        if debug:
            binary_str = ''.join(str(b) for b in current_bits[:8])
            char = chr(byte_val) if 32 <= byte_val <= 126 else '?'
            padding_info = f" (padded {8-original_length} bits, NO SEPARATOR)"
            print(f"  Final byte {byte_index}: {binary_str} = 0x{byte_val:02x} = '{char}'{padding_info}")
        
        bytes_out.append(byte_val)
    
    #Convert to text with hash detection
    result = ""
    hash_value = None
    
    if debug:
        print(f"\n[TEXT CONVERSION]:")
    
    for i, b in enumerate(bytes_out):
        if 32 <= b <= 126: #Printable ASCII
            char = chr(b)
            result += char
            if debug:
                print(f"  Byte {i}: 0x{b:02x} -> '{char}' ✓")
        elif b == 0: #Null byte
            if debug:
                print(f"  Byte {i}: 0x{b:02x} -> NULL (skipped)")
            pass  #Skip
        else:
            result += "?" #Invalid
            if debug:
                print(f"  Byte {i}: 0x{b:02x} -> '?' (INVALID)")
    
    #Check for hash verification from packet payloads (not timing-encoded)
    if hash_from_packets:
        if debug:
            print(f"\n[HASH DETECTION]")
            print(f"Flag: '{result}'")
            print(f"Hash from packet: '{hash_from_packets}'")
            
            #Verify the hash
            import hashlib
            expected_hash = hashlib.md5(result.encode('utf-8')).hexdigest()
            if hash_from_packets.lower() == expected_hash:
                print(f"  Hash verification: PASS")
            else:
                print(f"Hash verification: FAIL")
                print(f"Expected: {expected_hash}")
                print(f"Got: {hash_from_packets}")
                
                #Count corruption
                corruption_count = sum(1 for i, c in enumerate(result) if not (32 <= ord(c) <= 126))
                if corruption_count > 0:
                    print(f"\n[RECOVERY GUIDANCE]")
                    print(f"The flag appears corrupted. You can use hashcat to brute force the corrupted characters:")
                    print(f"")
                    print(f"Corrupted positions detected:")
                    for i, c in enumerate(result):
                        if not (32 <= ord(c) <= 126):
                            print(f"- Position {i}: '{c}' (byte 0x{ord(c):02x}) - should be printable ASCII")
                    print(f"")
                    print(f"Suggested hashcat command:")
                    #Create a mask with ? for corrupted characters
                    mask = ""
                    for c in result:
                        if 32 <= ord(c) <= 126:
                            mask += c
                        else:
                            mask += "?"
                    print(f"hashcat -a 3 -m 0 {expected_hash} \"{mask}\"")
                    print(f"")
                    print(f"Where ? represents the corrupted character to brute force.")
    
    if debug:
        print(f"\n[FINAL RESULT] '{result}'")
        if hash_value:
            print(f"[HASH] {hash_value}")
        
        #Show where corruption occurred
        expected_flag = "FLAG{" in result #CHANGE THIS
        if expected_flag:
            print(f"[ANALYSIS] Flag structure detected. Length: {len(result)}")
            corruption_count = 0
            for i, char in enumerate(result):
                if char == '?':
                    print(f"[CORRUPTION] Character {i} is corrupted (byte 0x{bytes_out[i] if i < len(bytes_out) else 0:02x})")
                    corruption_count += 1
            
            if corruption_count > 0 and hash_value:
                print(f"[RECOVERY] {corruption_count} corrupted characters detected")
                print(f"[RECOVERY] Use hash {hash_value} for verification/brute force")
    
    return result

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="RF Timing Decoder - HARD Version (Mathematical reconstruction with hash verification)",
        epilog="""
This is the Hard decoder for RF timing challenges WITH packet loss.
It uses advanced mathematical reconstruction to recover missing packets.

Examples:
  %(prog)s challenge.pcap
  %(prog)s challenge.pcap --debug
  %(prog)s challenge.pcap --src 10.0.0.10 --dst 10.0.0.20

For simple challenges without packet loss, use rf_timing_decoder_easy.py instead.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("pcap", help="PCAP file to decode")
    ap.add_argument("--src", help="Source IP filter")
    ap.add_argument("--dst", help="Destination IP filter") 
    ap.add_argument("--id", type=int, help="ICMP ID filter")
    ap.add_argument("--debug", action="store_true", help="Show detailed analysis and timing breakdown")
    args = ap.parse_args()
    
    try:
        result = decode_mathematical(args.pcap, args.src, args.dst, args.id, args.debug)
        print(result)
    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)

#!/usr/bin/env python3

#Simple ping timing packet decoder, uses basic timing analysis with set timing values, could be modified to determine this it's self

import argparse
from collections import defaultdict
from scapy.all import rdpcap, IP, ICMP, Raw

# Set known timing consts
BIT_0_TIME = 0.12      # 120ms = bit 0
BIT_1_TIME = 0.28      # 280ms = bit 1  
BYTE_SEP_TIME = 0.80   # 800ms = byte separator (word)

# Toleranceeee
TOLERANCE = 0.02 #change depending on packet accuracy

def choose_flow(pkts, src=None, dst=None, icmp_id=None): #Select timing flow (which to and from addr)
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
    
    # Choose flow with most packets - assumption but correct for this chall
    best = max(flows.items(), key=lambda kv: len(kv[1]))
    key, arr = best
    return key, arr

def classify_timing(delta): #set decoding mapping with added tolerance
    if abs(delta - BIT_0_TIME) <= TOLERANCE:
        return '0'
    elif abs(delta - BIT_1_TIME) <= TOLERANCE:
        return '1'
    elif abs(delta - BYTE_SEP_TIME) <= TOLERANCE:
        return 'SEP'
    else:
        return '?'  # Unknown/corrupted timing

def easy_decode(path, debug=False):
    pkts = rdpcap(path) #Load in packets
    
    key, arr = choose_flow(pkts)
    if not arr:
        raise RuntimeError("No ICMP Echo flow found")
    
    arr.sort(key=lambda x: getattr(x[ICMP], 'seq', 0)) # Sort by sequence number and remove duplicates

    seen_seqs = set()
    unique_arr = []
    for p in arr:
        seq = getattr(p[ICMP], 'seq', 0)
        if seq not in seen_seqs:
            seen_seqs.add(seq)
            unique_arr.append(p)
    
    if debug:
        print(f"[EASY DECODER] Processing {len(unique_arr)} packets")
        print(f"[FLOW] {key[0]} -> {key[1]}, ID: {key[2]}")
    
    deltas = []
    times = [p.time for p in unique_arr] # Calculate timing deltas between consecutive packets
    
    for i in range(1, len(times)):
        delta = times[i] - times[i-1]
        deltas.append(delta)
    
    if debug:
        print(f"[TIMING] Calculated {len(deltas)} deltas")
    
    sequence = []
    unknown_count = 0
    
    for i, delta in enumerate(deltas): # Convert deltas to bit sequence
        classification = classify_timing(delta)
        sequence.append(classification)
        
        if debug and i < 20:  # Show first 20 for debugging
            print(f"  Delta {i}: {delta:.3f}s -> {classification}")
        
        if classification == '?':
            unknown_count += 1
    
    if debug: #print extra stuff to help with error solving
        print(f"[SEQUENCE] {len(sequence)} elements, {unknown_count} unknown")
        if unknown_count > 0:
            print(f"[WARNING] {unknown_count} unknown timings detected!")
            print("         This suggests packet loss - try the hard decoder")
    
    ## Convert bit sequence to ASCII characters
    result = ""
    current_byte = ""
    bit_count = 0
     
    for element in sequence:
        if element in ['0', '1']:
            current_byte += element
            bit_count += 1
            
            # Complete byte (8 bits)
            if bit_count == 8:
                try:
                    byte_val = int(current_byte, 2)
                    if 32 <= byte_val <= 126:  # Printable ASCII
                        char = chr(byte_val)
                        result += char
                        if debug:
                            print(f"[BYTE] {current_byte} = '{char}' (0x{byte_val:02x})")
                    else:
                        result += '?'
                        if debug:
                            print(f"[BYTE] {current_byte} = '?' (0x{byte_val:02x}, non-printable)")
                except:
                    result += '?'
                    if debug:
                        print(f"[BYTE] {current_byte} = ERROR")
                
                current_byte = ""
                bit_count = 0
                
        elif element == 'SEP':
            # Byte separator - handle partial bytes
            if bit_count > 0:
                # Pad incomplete byte with zeros
                current_byte += '0' * (8 - bit_count)
                try:
                    byte_val = int(current_byte, 2)
                    if 32 <= byte_val <= 126:
                        char = chr(byte_val)
                        result += char
                        if debug:
                            print(f"[BYTE] {current_byte} = '{char}' (0x{byte_val:02x}, padded)")
                    else:
                        result += '?'
                        if debug:
                            print(f"[BYTE] {current_byte} = '?' (0x{byte_val:02x}, padded)")
                except:
                    result += '?'
                    if debug:
                        print(f"[BYTE] {current_byte} = ERROR (padded)")
                
                current_byte = ""
                bit_count = 0
                
        elif element == '?':
            # Unknown timing - this means big issues
            if debug:
                print(f"[ERROR] Unknown timing detected - packet loss likely")
            continue
    
    # Handle final partial byte
    if bit_count > 0:
        current_byte += '0' * (8 - bit_count)
        try:
            byte_val = int(current_byte, 2)
            if 32 <= byte_val <= 126:
                char = chr(byte_val)
                result += char
                if debug:
                    print(f"[BYTE] {current_byte} = '{char}' (0x{byte_val:02x}, final)")
            else:
                result += '?'
        except:
            result += '?'
    
    if debug:
        print(f"\n[RESULT] '{result}'")
        print(f"[ANALYSIS] Length: {len(result)} characters")
        if unknown_count == 0:
            print("[STATUS] Perfect decode - no corruption detected")
        else:
            print(f"[STATUS] {unknown_count} timing errors - use hard decoder")
    
    return result, unknown_count

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="RF Timing Decoder - Easy Version",
        epilog="""
This is the Easy decoder for RF timing challenges without packet loss.
It uses simple timing analysis to decode binary data from ICMP packet timing.

For challenges with packet loss, use rf_timing_decoder_hard.py instead.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("pcap", help="PCAP file to decode")
    ap.add_argument("--debug", action="store_true", help="Show detailed analysis")
    args = ap.parse_args()
    
    try:
        result, errors = easy_decode(args.pcap, args.debug)
        
        if not args.debug:
            print(result)
        
        if errors > 0 and not args.debug:
            print(f"\n[WARNING] {errors} timing errors detected")
            print(f"Try: python3 rf_timing_decoder_hard.py {args.pcap}")
            
    except Exception as e:
        print(f"ERROR: {e}")

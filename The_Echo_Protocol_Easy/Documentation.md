# Challenge Document


### Version: `1.0.0`
### Long Title: The Echo Protocol 1
### Short Title: FOR01
### Author: Katy Harrington
### Date: 08/08/2025
### Difficulty: Easy
### Learning objective: Can see hidden data in packet timing


## Challenge Brief (as its to be written in RIO):
A network capture contains suspicious ICMP traffic that appears normal but may hide secret communications.

## Solve:

1. **Filter Traffic:** Find ICMP Echo packets from 10.0.0.10 to 10.0.0.20 with ID 0xBEEF
2. **Sort Packets:** Order by sequence number
3. **Calculate Deltas:** Measure time between consecutive packets
4. **Classify Timing:** 0.12s = bit 0, 0.28s = bit 1, 0.80s = separator
5. **Assemble Data:** Group bits into bytes and convert to ASCII

An example solution sript is in the source dir
`python3 solution.py challenge.pcap`


## Author Notes: 
Easy chall 


## Debrief: 
This challenge is a precursor to the hard version where users just need to identify that the secret message is in the paket timings of the corect packet flow. Then decode binary to ascii, they nee to identify the timings.


## Hints: 
- Focus on ICMP Echo packets
- Pay attention to timing between consecutive packets
- Look for the correct source/destination flow


# Challenge Document


### Version: `1.0.0`
### Long Title: The Echo Protocol 2
### Short Title: FOR02
### Author: Katy Harrington
### Date: 08/08/2025
### Difficulty: Hard
### Learning objective: Can see hidden data in packet timing but with packet loss


## Challenge Brief (as its to be written in RIO):
A network capture contains suspicious ICMP traffic that appears normal but may hide secret communications.

## Solve:

1. **Filter Traffic:** Find ICMP Echo packets from 10.0.0.10 to 10.0.0.20 with ID 0xBEEF
2. **Identify Gaps:** Detect missing packets through timing analysis
3. **Mathematical Reconstruction:** Use gap analysis to determine missing intervals
4. **Timing Classification:** Handle corrupted timing with tolerance
5. **Hash Verification:** Extract verification hash from packet payload
6. **Hashcat** If flag not Complete use hash cracking tool on letters missing or incomplete
7. **Validation:** Verify reconstructed flag against MD5 hash

An example solution script is in the source dir which will give an almost reconstructed flag
`python3 solution.py challenge.pcap` 


## Author Notes: 
ensure the flag is long so it can't be brute forced (around 30 character flag with a 6% loss makes an easy solver struggle but a mathematical solver almost work with a few left to brute fore with the hash)

Increasing packet loss increases difficulty

## Debrief: 
This is a timing challenge with packet loss so some mathematical reconstruction and brute force my be reqired, a hash of the flag is sent so the user can check their flag.


## Hints: 
- Some packets may be missing due to network issues
- Look for mathematical patterns in timing gaps
- Hash verification data is included for validation

# Build Instructions - Timing Easy Challenge

### Prerequisites
- Python 3.6+
- Scapy library: `pip install scapy`

### 1. Generate Challenge File

#### Option A: Using Flag File (Recommended)
```bash
cd Source/
python3 rf_timing_generator.py \
  --flag-file "../Flag/flag.txt" \
  --outfile the_echo_protocol_1.pcap \
  --noise-subnets "10.0.0.21-50" "192.168.1.0/28" "172.16.0.100-120" \
  --noise 1000 \
  --seed 12345
```

#### Option B: Direct Flag Input
```bash
cd Source/
python3 rf_timing_generator.py \
  --flag "FLAG{somehing_goes_here}" \
  --outfile the_echo_protocol_1.pcap \
  --noise-subnets "10.0.0.21-50" "192.168.1.0/28" "172.16.0.100-120" \
  --noise 1000 \
  --seed 12345
```


### 3. Deploy Challenge
- **Host File:** Upload `the_echo_protocol_1.pcap` to file host
- **Access:** Provide download link to contestants


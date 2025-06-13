# Build Instructions - Timing Easy Challenge

### Prerequisites
- Python 3.6+
- Scapy library: `pip install scapy`


### 1. Generate Challenge File

#### Option A: Using Flag File NEEDS TO BE LONG FLAG, READ DOCUMENTATION AUTHOR NOTES FOR MORE
```bash
cd Source/
python3 rf_timing_generator.py \
  --flag-file "../Flag/flag.txt"\ 
  --outfile the_echo_protocol_2.pcap \
  --noise-subnets "10.0.0.21-60" "192.168.0.0/24" "172.16.0.0/28" "203.0.113.0/29" \
  --noise 1500 \
  --loss 0.06 \
  --dup 0.08 \
  --seed 54321
```

#### Option B: Direct Flag Input
```bash
cd Source/
python3 rf_timing_generator.py \
  --flag "FLAG{h4rd_p4ckkket_loss_7iming_ch4llenge}" \
  --outfile the_echo_protocol_2.pcap \
  --noise-subnets "10.0.0.21-60" "192.168.0.0/24" "172.16.0.0/28" "203.0.113.0/29" \
  --noise 1500 \
  --loss 0.06 \
  --dup 0.08 \
  --seed 54321
```


### 3. Deploy Challenge
- **Host File:** Upload `the_echo_protocol_2.pcap` to file host
- **Access:** Provide download link to contestants


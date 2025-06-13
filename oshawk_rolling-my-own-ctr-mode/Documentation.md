# Challenge Document

### Version: `0.1.0`
### Long Title: Rolling my own CTR mode
### Short Title: CRY01
### Author: Oshawk
### Date: 03/08/2025
### Difficulty: Easy
### Learning objective: Identification of a weakness in a custom symmetric crypto scheme

## Challenge Brief (as its to be written in RIO):

I heard that AES CTR mode has a problem with message integrity, so I decided to create my own version.

The attached script is running on the server. Connect with `nc` when you are ready to solve.

## Solve:

The intended weakness is that if you set the counter length (first byte of ciphertext) to 32 or greater, the entire key gets replaced with the counter (entirely null for the first block).

Script to generate a solution:

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

plaintext = pad(b"open sesame", AES.block_size)
cipher = AES.new(b"\x00" * 32, AES.MODE_ECB)
print("20" + cipher.encrypt(plaintext).hex())
```

This will output `20e053ca45c2f03ef0224677785aadc7ad`.

Connect to the server with `nc` and decrypt the output.

## Author Notes:

## Debrief:

The intended weakness is that if you set the counter length (first byte of ciphertext) to 32 or greater, the entire key gets replaced with the counter (entirely null for the first block).

## Hints: 

1. I wonder if a user-controllable counter length could cause problems...

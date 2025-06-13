#!/usr/bin/env python

import os
import string
import base64

b64_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"

def base64_encode_hiding(data: bytes, hidden: int) -> tuple[bytes, int]:
    blocks = [data[i:i+3] for i in range(0, len(data), 3)]

    # encode the normal blocks:
    normal = base64.b64encode(b"".join(blocks[:-1]))

    # now hide what we can in the last block
    final = blocks[-1]
    final_str = ""
    match len(final):
        # one byte gives us four bits to encode into
        # [XXXX XXXX] -> [XXXX XX] [XX ____] [000 000] [000 000]
        case 1:
            # take 4 bits from hidden
            hidden_bits = hidden & 0b1111
            hidden >>= 4
            # [XXXX XX]
            first_char = b64_alphabet[final[0] >> 2]
            # [XX ____]
            second_char = b64_alphabet[(final[0] << 4 | hidden_bits) & 0b111_111]
            final_str = first_char + second_char + "=="
        # two bytes gives us two bits to encode into
        # [XXXX XXXX] [YYYY YYYY] -> [XXXX XX] [XX YYYY] [YYYY __] [000 000]
        case 2:
            # take 2 bits from hidden
            hidden_bits = hidden & 0b11
            hidden >>= 2
            # [XXXX XX]
            first_char = b64_alphabet[final[0] >> 2]
            # [XX YYYY]
            second_char = b64_alphabet[(final[0] << 4 | final[1] >> 4) & 0b111_111]
            # [YYYY __]
            third_char = b64_alphabet[(final[1] << 2 | hidden_bits) & 0b111_111]
            final_str = first_char + second_char + third_char + "="
        case 3:
            #  we can't do anything here
            final_str = base64.b64encode(final).decode()

    
    out = normal + final_str.encode()
    # check we didn't fuck up
    base64.b64decode(out)
    return out, hidden


flag = os.getenv("FLAG", "flag{testing}").encode()
i = 0
while True:
    flag_bits = int.from_bytes(flag, "big")
    base_string = str(i).encode()

    for _ in range(i):
        base_string, flag_bits = base64_encode_hiding(base_string, flag_bits)
        print(bin(flag_bits))

    if flag_bits == 0:
        break

    i += 1

# check we can decode i times
tmp = base_string
for _ in range(i):
    print(tmp)
    tmp = base64.b64decode(tmp)


with open("chal.txt", "wb") as f:
    print(i)
    f.write(base_string)


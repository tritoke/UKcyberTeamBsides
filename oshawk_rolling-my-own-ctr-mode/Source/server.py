import secrets

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from flag import FLAG

KEY: bytes = secrets.token_bytes(32)


def encrypt(plaintext: bytes) -> bytes:
    plaintext = pad(plaintext, AES.block_size)
    plaintext_blocks = [plaintext[i:i+AES.block_size] for i in range(0, len(plaintext), AES.block_size)]

    counter = 0
    counter_length = (len(plaintext_blocks).bit_length() + 7) // 8
    
    ciphertext = bytearray([counter_length])

    for block in plaintext_blocks:
        counter_bytes = counter.to_bytes(counter_length, "big")

        cipher = AES.new((counter_bytes + KEY)[:32], AES.MODE_ECB)

        ciphertext_block = cipher.encrypt(block)
        ciphertext += ciphertext_block

        counter += 1

    return bytes(ciphertext)


def decrypt(ciphertext: bytes) -> bytes | None:
    if len(ciphertext) % AES.block_size != 1:
        print("Invalid ciphertext length.")
        return None

    counter = 0
    counter_length = ciphertext[0]
    
    ciphertext = ciphertext[1:]
    ciphertext_blocks = [ciphertext[i:i+AES.block_size] for i in range(0, len(ciphertext), AES.block_size)]

    plaintext = bytearray()

    for block in ciphertext_blocks:
        try:
            counter_bytes = counter.to_bytes(counter_length, "big")
        except OverflowError:
            print("Invalid counter length.")
            return None

        cipher = AES.new((counter_bytes + KEY)[:32], AES.MODE_ECB)

        plaintext_block = cipher.decrypt(block)
        plaintext += plaintext_block

        counter += 1

    try:
        return bytes(unpad(plaintext, AES.block_size))
    except ValueError:
        print("Invalid padding.")
        return None


def main() -> None:
    print("Welcome to the secure encryption service!")

    while True:
        option = input("[e]ncrypt/[d]ecrypt/[q]uit> ")

        if len(option) == 0:
            continue

        option = option[0].lower()

        if option == "e":
            plaintext_string = input("plaintext> ")
            plaintext = plaintext_string.encode()

            if b"open sesame" in plaintext:
                print("Anything but that!")
                continue

            print(encrypt(plaintext).hex())
        elif option == "d":
            ciphertext_string = input("ciphertext> ")

            try:
                ciphertext = bytes.fromhex(ciphertext_string)
            except ValueError:
                print("Invalid hex.")
                continue

            plaintext = decrypt(ciphertext)

            if plaintext is None:
                continue

            if plaintext == b"open sesame":
                print(FLAG)
                continue

            print(plaintext)
        elif option == "q":
            exit(0)

if __name__ == "__main__":
    main()

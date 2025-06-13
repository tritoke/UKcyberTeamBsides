def generate_message(keyword, flag):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    encrypted = keyword
    for l in alphabet:
        if l not in encrypted:
            encrypted = encrypted + l

    message = ""
    for c in flag:
        message = message + encrypted[alphabet.index(c)]
    return message


keyword = "selybdvcf"

# Change the flag here
flag = "musicisthekey"
message = generate_message(keyword, flag)

print(message)

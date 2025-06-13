# Challenge Document


### Version: `1.0.0`
### Long Title: Hiding in the s64dows
### Short Title: FOR01
### Author: Sam Leonard
### Date: 04/07/2025
### Difficulty: Medium
### Learning objective: To give an understanding for how base64 works and how data can be hidden in base64 encoded strings


## Challenge Brief (as its to be written in RIO):

Hiding deep in the realm between the earth and the void is something special, do you have what it takes to walk on the edge?

## Solve:

The user can write each base64 decode to a line in a file and use a tool I already wrote (albeit with some tweaks) in order to recover the secret.
https://github.com/tritoke/ctf-scripts/blob/main/base64_extract_hidden_bits.py

However the idea is that they will write their own base64 decoder and manually extract the extra data from the padding bits.

## Author Notes: 

Understand base64 = win

## Debrief: 

This challenge was identifying a quirk of the base64 encoding scheme where sequences requiring padding have either 2 or 4 bits of free space at the end in which data can be hidden.
Gynvael coldwind has an excellent explanation of this technique on his consulting firm's blog: https://hexarcana.ch/b/2024-08-16-base64-beyond-encoding/

## Hints: 

1. Can multiple base64 strings decode to the same result?

2. The flag is hidden in the padding bits of each base64 encoded message.

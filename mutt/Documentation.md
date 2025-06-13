# Challenge Document


### Version: `0.1.a`
### Long Title: race-my-robot
### Short Title: WEB01
### Author: Alana "mutt" Witten
### Date: 03/07/2025
### Difficulty: Easy
### Learning objective: Practice code auditing for web apps


## Challenge Brief (as its to be written in RIO):

Put your web and code auditing skills to the test and exploit the vulnerability to get the flag! 

Make sure to pick a copy of the source code here! {download link to zip of the entire challenge} and spawn an instance of the challenge here! {link to spawn the challenge/link to the site}


## Solve:

visit: http://instance:port/flag/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa! 

## Author Notes: 

Thanks for playing, I had great fun building this; I hope you enjoy Bsides Bristol!


## Debrief:

1) Visiting /flag we notice a three second delay before being told we were too slow. When we check the source code we can verify this is the case and that our robot friend gets too start before then, and thus always wins the race
2) Following the code we see the function that looks like it performs some sort of path validation, and we spot `match = re.match("(a+)+$", path)`
3) This regex is vulnerable to ReDoS (Regular Expression Denial of Service) and causes catastrophic backtracking on specific input. If we use this DoS on the robot's thread, we can beat them to the flag. The regex `(a+)+` matches one or more groups, of one or more 'a' characters, eg "a", "aa", "aaa", "aaaa", "aaaaa" and so on. But is "aaaaa" a group of 5 "a"s (aaaaa)? or is it 4 and 1 (aaaa)(a)? or 3 and 2 (aaa)(aa)? and so on! The more we extend the length, the more permutations the regex engine has to calculate, which becomes very computationally expensive and so can delay or crash the process! We also need one non "a" character at the end; this is because if not, the regex will match it as one big group of "a"s and then not bother to check for permutations. Using this knowledge, we can crash the bot and get out flag by visiting a url like the following: http://127.0.0.1:5000/flag/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa! 


## Hints: 

Once you know it you'll scream :p

# Challenge Document


### Version: `0.1.a`
### Long Title: Back to the New House
### Short Title: FOR01
### Author: jamsec
### Date: 13/08/2025
### Difficulty: Easy - Medium
### Learning objective: To demostrate forensic analysis of multiple sources to solve an investigation


## Series Brief (as its to be written in RIO):

You're an intern at New House - a forensics investigation company. We've extracted a network capture, a zip file filled with fun logs, and a product specification document. Connect to our reporting platform and tell us what you find!

## Challenge formatting

Please split this into 12 seperate challenges, with the descriptions and flags as follows:

1. What group has been made on the Windows machine? 
Flag: `thesmiths`

2. Who is in the group identified earlier? (separate multiple answers with commas and sort them alphabetically: e.g. alpha, beta, gamma, omega). 
Flag: `colin, ed, jonny, philip, thom`

3. What tasks are no longer present on the Windows machine? (separate multiple answers with commas and sort them alphabetically: e.g. alpha, beta, gamma, omega). 
Flag: `DeliverUpdates, RevertUpdates, RunUpdates`

4. What task is created on the Windows machine?
Flag: `ChangeBackground`

5. What operating system (distro) is the Linux user running?
Flag: `Ubuntu`

6. What tool was downloaded and run against the Linux machine?
Hint: How can you tell that somethign is being downloaded from the internet?
Flag: `nmap`

7. What ports are initially open on the Linux machine? (separate multiple answers with commas and sort in ascending order: e.g. 1, 2, 3)
Hint: What TCP flags indicate whether a message has been received?
Flag: `21, 5000, 6969`

8. What browser is the informant using?
Flag: `Firefox`

9. What is the email address of the interesting user?
Flag: `hello@biggestradioheadfan.net`

10. What port number is brought up after any initial enumeration?
Hint: What port was initially closed, and is not later on?
Flag: `31337`

11. What needs to be sent if a message is received?
Flag: `signal` (if you can accept multiple flags, also accept a signal please)

12. Where is the developer of this custom tool from? State both the city and country and comma seperate these (e.g. Paris, France).
Hint: Word documents can contain interesting things...
Flag: `Valletta, Malta`

## Difficulty comments
The position of a challenge in the series does not represent its difficulty - rather the order in the story.

My personal thoughts on categorising difficulty for each challenge:

Beginner: 1, 5, 8, 9
Easy: 2, 3, 4
Medium: 6, 7, 10
Medium-Hard: 11, 12

Each challenge can be solved independently of other challenges in this series. I've not given hints for beginner/easy challenges, as doing so would either be a useless hint or spoil the whole challenge.

I strongly disagree with making this category one with unlockable challenges - they should all be open to players at the beginning.

## Point allocation

I personally don't think this challenge is worth more points than an extreme, so finding a nice way to split up points for each difficulty ranking is a good idea.

Ensure that the points for an "Easy"/ other difficulties here is less than the points for other easy challenges in the CTF, to ensure this series does not dilute point allocation. 

## Solutions
The challenge series is broken down into 12 questions. The answers / brief explanations are as follows:

1. The group is called `thesmiths`. This can be obtained through looking through the event viewer logs for group creation events, which log the name created.

2. The users in this group are `"thom", "jonny", "colin", "ed", "philip` . This can be obtained through looking through group addition events in Windows Event Viewer logs.

3. The tasks no longer present are `"DeliverUpdates", "RevertUpdates", "RunUpdates"`. This can be obtained through filtering for task deletions in Windows Event Viewer logs.

4. The task created on the Windows machine is `ChangeBackground`. This can be obtained by looking for task creation events on the Windows machine.

5. The distro used is `Ubuntu`. This is obtained from user agent strings within the PCAP.

6. The tool installed on the Linux machine was `nmap`. This is shown by looking at the HTTP requests for the .deb file downloaded from Ubuntu, with the filepath having nmap in the name. (This also allows you to solve part 5 :] ) 

7. The open ports initially are `21, 5000, 6969`. This is solved by looking at the TCP responses from each port in the PCAP during the network scan - most are `RST, ACK` which means a port is not open, but the open ports respons with `SYN, ACK`. 

8. The answer is `Firefox`. This can be obtained through reading the user agent string of any requests made to the website in the PCAP (via following the TCP stream).

9. The user's email address is `hello@biggestradioheadfan.net`. `strings` can simply be run on the PCAP for this - it's the only email present.

10. The answer is `31337`. This is shown in the PCAP when the user submits a help form on the website - you can also search the pcap for the packet where the email was seen, and it is the destination port.

11. The answer is `a signal`. The message is a base64 encoded string. To decrypt this string, the instructions in the product specification document must be followed - the original message is XOR'd with the song selected in the favourite song field. Write a script to implement this.

12. The answer is `Valletta, Malta`. The product specification document has custom XML injected inside that can be base64 decoded to an image. This image can be reverse searched to be found to be in Valletta, Malta. 

## Author Notes: 

This is a reasonably straight forward challenge in forensic analysis.


## Debrief: 

Congratulations on solving the challenge! You've used multiple forensic sources to complete an investigation.

## Hints: 



# Challenge Document


### Version: `0.1.a`
### Long Title: crypto tunes
### Short Title: CT01
### Author: Daisy Mallion
### Date: 06/08/2025
### Difficulty: Easy
### Learning objective: To learn about encryption methods


## Challenge Brief (as its to be written in RIO):

We've found the following encrypted message, along with this random list of letters and numbers (in the text file). On the laptop where it was found, the song "Boys Don't Cry" by The Cure was playing on a loop... Very strange, but probably unrelated, right?

irpflfpqcbgbx

## Solve:

- Lookup lyrics of the song (e.g. https://genius.com/The-cure-boys-dont-cry-lyrics)
- Determine letters of the encryption key
    - e.g. v1, 2, 3, 4 = verse 1, line 2, word 3, letter 4 so in this case "u"
    - The resulting key is selybdvcf
- Determine that a keyword cipher has been used
- Use a tool/manually decrypt the message using the discovered key

## Author Notes: 

There may be issues if a different website is used to view the lyrics, as the one linked above clearly marks verses, choruses, and the bridge. However I assume most would structure the lyrics similarly.

## Debrief: 

If you manually deciphered the message, you may be interested at looking here (https://www.geeksforgeeks.org/dsa/keyword-cipher/) for how a script can be written to automate it.

## Hints: 

- How could the song be linked to the contents of the file?
- What type of encryption could use a key in this format?

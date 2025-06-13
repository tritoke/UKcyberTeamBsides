# Challenge Document


### Version: `1.0.0`
### Long Title: Trail Trace
### Short Title: MISC01
### Author: Finley Denton
### Date: 03/08/2025
### Difficulty: Easy
### Learning objective: To study the NMEA protocol and how to parse it into usable information


## Challenge Brief (as its to be written in RIO):

We've recovered data from a tracker planted on an elusive criminal, can you trace their steps?

## Solve:

The user should write a script that will parse the NMEA $GPGGA data and will plot (whether just on a graph or an actual map) the trail, spelling out the flag. 
https://cdn.sparkfun.com/assets/a/3/2/f/a/NMEA_Reference_Manual-Rev2.1-Dec07.pdf (GGA section)

## Author Notes: 

Read protocol documentation = win
In this case, only the latitude, N/S indicator, Longitude, E/W indicator are needed. There should be no outlier data points. 
As the data is positioned around Bristol, it does not cross the equator or Prime Meridian, and hence will always read N/W.
Can be easily reflagged by changing the FLAG variable in Source.py, deleting the previous log.pcap and running Source.py again.

## Debrief: 

The challenge was to parse the NMEA protocol data being sent in the pcap, parsing the longitude and latitude data stored in the $GPGGA format. A good way to do this was to use scapy to read packet by packet, and extract the data starting from `$GPGGA` to the end of the packet. Once you have collected the longitude and latitude points, plot them either as a graph or on a map, drawing a line from each consecutive point, spelling out the flag.

## Hints: 

1. Study the NMEA protocol here: https://docs.arduino.cc/learn/communication/gps-nmea-data-101/
2. What happens if you follow the trail, GPS point to GPS point?

# Your UW ID and your name - there is no special format for this. (This homework ought to be done individually)

jrao7
Jinmeng Rao

# Trace 1: HTTP
## Give three websites (domain Nname and IP addresses) visited from source IP address `192.168.0.100`


www.amazon.com - 72.21.215.232
www.bing.com - 198.105.251.25
www.a.shifen.com - 180.76.3.151

## Give three search queries and the domain of the site for each query made from source IP address `192.168.0.100`

www.amazon.com - adventures in Stochastic Processes
www.bing.com - chicago metro
www.a.shifen.com - 来自星星的你

# Trace 2: FTP
## What is the user name and password used to connect to the FTP server?

username - shiningmoon
password - public

## List any (and all) files that were downloaded.

dragon.zip
ARP.java
L2Switch.java
phase1.html

## List the full path for two files (in different directories) on the FTP server that were NOT downloaded.

/phase1/StoreForwardingDatalink.java
/TeNet/tester.build.111128.jar


# Trace 3: Traceroute
## Briefly describe how the traceroute tool works including which network protocols are in use.

The traceroute tool shows the path a packet sent from one machine to another machine via network takes as it hops from router to router.
 
Specifically, traceroute first sends a UDP message with TTL=1 (Time to live) to the destination machine, and then the first router that receive this message reduces its TTL by 1 (now TTL=0), drops message, and sends an ICMP packet back to the source machine. Now we have the path from the source machine to the first router. By increasing the TTL value and repeating this process, we will finally reach the destination machine and get the path.

The traceroute tool uses ICMP and UDP.


## Give the source IP address that issued the traceroute command and the destination IP address.

source - 192.168.0.100
destination - 74.125.225.46

## List the IP addresses on the route between source and destination.

(source - 192.168.0.100)
192.168.0.1
10.131.180.1
96.34.20.20
96.34.17.95
96.34.16.112
96.34.16.77
96.34.2.4
96.34.0.7
96.34.0.9
96.34.3.9
96.34.152.30
209.85.254.120
209.85.250.28
(destination - 74.125.225.46)


# Trace 4: POP
## What is the POP username and password?

username - cs155@dummymail.com
password - whitehat

## How many emails are in the user's mailbox?

There are 5 emails.

## Give the contents of from, to, subject, and date for one email message.

From: joe <cs155@dummymail.com>
To: cs155@dummymail.com
Subject: foobar
Date: Fri, 23 Apr 2010 08:20:52 -0700

## What email client (application) and operating system is this person using to send and receive email?

email client - Thunderbird 2.0.0.23 
operating system - Windows/20090812
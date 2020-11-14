# ARP_spoofing
python scanner.py arpspoofing.pcap

For this part, I created a function ARP_spoofing_detection to check if there are any mismatch between ip-mac pair in pcap records and print the spoof ones.

# Port Scans 
python scanner.py portscan.pcap

For this part, I created a function port_scans_detection and use python dict of dicts to check the port scans and record packet number into dicts. We then find the number larger than 100 and print them out.

# SYN Floods
python scanner.py synflood.pcap

For this part, I created a function TCP_SYN_floods_detection which uses dict of lists to check, store and report the first 101 packets within a second which are detected as a SYN flood attack for each victim port.
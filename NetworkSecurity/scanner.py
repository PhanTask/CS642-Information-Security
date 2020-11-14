# source:
# https://dpkt.readthedocs.io/en/latest/_modules/examples/print_packets.html
# https://stackoverflow.com/questions/18256342/parsing-a-pcap-file-in-python

import sys
import dpkt
import socket
from dpkt.compat import compat_ord

global arp_spoofing_str
global port_scans_dict
global syn_floods_str
global syn_flood_dict

arp_spoofing_str = ''
port_scans_dict = {}
syn_flood_dict = {}
syn_floods_str = ''


def mac_to_str(mac):
    return ':'.join('%02x' % compat_ord(b) for b in mac)

def str_to_mac(mac_str):
    return bytes.fromhex(mac_str.replace(":", ""))

def inet_to_str(inet):
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)

def str_to_inet(ip_str):
    return socket.inet_aton(ip_str)

def ARP_spoofing_detection(data, idx):
    global arp_spoofing_str
    local_network_dict = {
        '192.168.0.100': '7c:d1:c3:94:9e:b8',
        '192.168.0.103': 'd8:96:95:01:a5:c9',
        '192.168.0.1': 'f8:1a:67:cd:57:6e'
    }

    spa = inet_to_str(data.spa)
    sha = mac_to_str(data.sha)
    tha = mac_to_str(data.tha)
    if spa in list(local_network_dict.keys()):
        if local_network_dict[spa] != sha:
            arp_spoofing_str += 'ARP spoofing!\n'
            arp_spoofing_str += ('Src MAC: ' + sha + '\n')
            arp_spoofing_str += ('Dst MAC: ' + tha + '\n')
            arp_spoofing_str += ('Packet number: ' + str(idx) + '\n')


def port_scans_detection(data, idx):
    global port_scans_dict
    dport = data.data.dport
    dst = inet_to_str(data.dst)
    if dst in port_scans_dict.keys():
        if dport in port_scans_dict[dst].keys():
            return
        else:
            port_scans_dict[dst][dport] = idx
    else:
        port_scans_dict[dst] = {}


def TCP_SYN_floods_detection(data, ts, idx):
    global syn_flood_dict
    global syn_floods_str
    dport = data.data.dport
    dst = inet_to_str(data.dst)

    ip_port = dst + ':' + str(dport)

    if ip_port in syn_flood_dict.keys():
        if syn_flood_dict[ip_port] == 0:
            return
        syn_flood_dict[ip_port].append((ts, idx))
    else:
        syn_flood_dict[ip_port] = []
        syn_flood_dict[ip_port].append((ts, idx))

    r_ts = syn_flood_dict[ip_port][0][0]

    if len(syn_flood_dict[ip_port]) >= 101:
        if ts - r_ts > 1:
            syn_flood_dict[ip_port].pop(0)
        else:
            packet_numbers = ', '.join([str(pn) for pn in sorted(idx for (ts, idx) in syn_flood_dict[ip_port])])
            syn_floods_str += 'SYN floods!\n'
            syn_floods_str += ('Dst IP: ' + dst + '\n')
            syn_floods_str += ('Dst Port: ' + str(dport) + '\n')
            syn_floods_str += ('Packet number: ' + packet_numbers + '\n')
            syn_flood_dict[ip_port] = 0



def print_output():
    global arp_spoofing_str
    global port_scans_dict
    global syn_floods_str
    global syn_flood_dict

    # ARP Spoofing output
    if arp_spoofing_str != '':
        print(arp_spoofing_str)


    # Port Scans output
    port_scans_str = ''
    for dst in port_scans_dict:
        if len(port_scans_dict[dst]) >= 100:
            packet_numbers = ', '.join([str(pn) for pn in sorted(port_scans_dict[dst].values())])
            port_scans_str += 'Port scan!\n'
            port_scans_str += ('Dst IP: ' + dst + '\n')
            port_scans_str += ('Packet number: ' + packet_numbers + '\n')

    if port_scans_str != '':
        print(port_scans_str)

    # SYN Floods output
    if syn_floods_str != '':
        print(syn_floods_str)



if __name__ == '__main__':
    pcap_data = None
    with open(sys.argv[1], 'rb') as f:
        pcap_data = dpkt.pcap.Reader(f)
        for idx, (ts, pkt) in enumerate(pcap_data):
            eth_pkt = dpkt.ethernet.Ethernet(pkt)
            if eth_pkt.type == dpkt.ethernet.ETH_TYPE_ARP:
                ARP_spoofing_detection(eth_pkt.data, idx)
            elif eth_pkt.type == dpkt.ethernet.ETH_TYPE_IP:
                ip_data = eth_pkt.data
                if isinstance(ip_data.data, dpkt.tcp.TCP):
                    if ip_data.data.flags != dpkt.tcp.TH_SYN:
                        continue
                    port_scans_detection(ip_data, idx)
                    TCP_SYN_floods_detection(ip_data, ts, idx)
                elif isinstance(ip_data.data, dpkt.udp.UDP):
                    port_scans_detection(ip_data, idx)
                else:
                    continue
            else:
                continue
    print_output()
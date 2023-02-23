from scapy.all import TCP,Raw

def check(pkt, direction):
  return pkt.haslayer(TCP) and direction == 0

actions = ["tcpPayload"]
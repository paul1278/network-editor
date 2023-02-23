from scapy.all import TCP,Raw

def check(pkt, direction):
  return pkt.haslayer(TCP)

actions = ["tcpPayload"]
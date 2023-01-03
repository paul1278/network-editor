from scapy.all import TCP,Raw

def check(pkt):
  return pkt.haslayer(TCP)

actions = ["tcpPayload"]
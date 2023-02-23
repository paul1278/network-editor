from scapy.all import UDP,Raw

def check(pkt, direction):
  if pkt.haslayer(UDP):
    return pkt[UDP].haslayer(Raw)
    
  return False

actions = ["udpPayload"]
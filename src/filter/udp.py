from scapy.all import UDP,Raw

def check(pkt):
  if pkt.haslayer(UDP):
    return pkt[UDP].haslayer(Raw)
    
  return False

actions = ["udpPayload"]
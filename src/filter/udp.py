from scapy.all import UDP

def check(pkt):
  if pkt.haslayer(UDP):
    return True
  return False

actions = ["udpPayload"]
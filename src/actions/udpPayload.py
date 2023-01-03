from scapy.all import UDP,Raw,Ether,IP

def modPaket(pkt):
  #pkt[UDP].sport = 1111
  #pkt[UDP].dport = 8080
  #pkt[Raw].load = "olelddqwerqwrwerqq\n"
  pkt[UDP].chksum = None
  pkt[UDP].len = None
  #pkt[IP].len = None
  #pkt[IP].src = "172.19.0.5"
  #pkt[IP].chksum = None
  return Ether(bytes(pkt))
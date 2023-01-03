from scapy.all import TCP,Raw,Ether,IP

def modPaket(pkt):
  #pkt[UDP].sport = 1111
  #pkt[UDP].dport = 8080
  #pkt[Raw].load = "olelddqwerqwrwerqq\n"
  if pkt[TCP].payload.haslayer(Raw):
    pkt[TCP].payload[Raw].show()
    pkt[TCP].payload[Raw].load = "awesomo\n"
    pkt[TCP].payload[Raw].show()
  
  pkt[TCP].chksum = None
  pkt[TCP].len = None
  pkt[IP].len = None
  #pkt[IP].src = "172.19.0.5"
  pkt[IP].chksum = None
  return Ether(bytes(pkt))
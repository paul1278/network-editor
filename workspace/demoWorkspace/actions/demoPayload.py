from scapy.all import TCP,Ether,IP
from workspace import protocols
CoffeeProtocolPriceList = protocols.demo.CoffeeProtocolPriceList

def modPaket(pkt):
  pkt[TCP].payload[CoffeeProtocolPriceList].products[0].productName = "KAFFEEZZ"
  pkt[TCP].payload[CoffeeProtocolPriceList].products[0].price = 1
  
  pkt[TCP].chksum = None
  pkt[TCP].len = None
  pkt[IP].len = None
  pkt[IP].chksum = None
  return Ether(bytes(pkt))
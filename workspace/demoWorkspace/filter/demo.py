from scapy.all import TCP,Raw
from workspace import protocols

def check(pkt, direction):
  return pkt.haslayer(protocols.demo.CoffeeProtocolPriceList)

actions = ["demoPayload"]
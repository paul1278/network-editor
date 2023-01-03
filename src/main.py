from scapy.all import conf,bridge_and_sniff,UDP,Raw,Ether,IP
from utils import *
import config

def pkt_callback_i1(pkt):
	return handlePaket(pkt, 0)

def pkt_callback_i2(pkt):
	return handlePaket(pkt, 1)

def handlePaket(pkt, direction):
	ret = True
	debug(config.data["interface" + str(direction +1)] + ":", "Got packet", pkt)
	for f in config.filters:
		if pkt == False or pkt == True:
			return pkt
		testingFilter = config.filters[f]
		if testingFilter.check(pkt):
			debug("Filter", f, "is true")
			for a in testingFilter.actions:
				if pkt == False or pkt == True:
					return pkt
				action = config.actions[a]
				pkt = action.modPaket(pkt)
				ok("Action", a, "changed the packet by filter", f)
			break
	return pkt

def start_bridge():
	ok("Bridge is starting up")
	bridge_and_sniff(config.data["interface1"], config.data["interface2"], xfrm12=pkt_callback_i1, xfrm21=pkt_callback_i2, count=0, store=0)
	print("bye!!")

if __name__ == "__main__":
	print_header()
	if config.load() == False:
		error("Program terminated")
		quit(1)
	conf.verb=3
	conf.sniff_promisc=True
	start_bridge()
from scapy.all import conf,bridge_and_sniff,UDP,Raw,Ether,IP
from utils import *
import config

log = []
def pkt_callback_i1(pkt):
	return handlePaket(pkt, 0)

def pkt_callback_i2(pkt):
	return handlePaket(pkt, 1)

def handlePaket(pkt, direction):
	ret = True
	#debug(config.data["interface" + str(direction +1)] + ":", "Got packet", pkt)
	log.append(config.data["interface" + str(direction +1)] + ": Got packet" + str(pkt))
	if direction == 0:
		pkt[Ether].dst = config.data["mac2"]
		pkt[Ether].src = config.data["localmac2"]
	else:
		pkt[Ether].dst = config.data["mac1"]
		pkt[Ether].src = config.data["localmac1"]
	pkt = Ether(bytes(pkt))
	dims = _mainwin.getmaxyx()
	h = dims[0] - 1
	lsize = len(log)
	for i in range(h):
		j = lsize - i - 1
		if j < 0:
			break
		_mainwin.addstr(h - i,0,log[j])
	_mainwin.refresh()
	return pkt
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

def start_bridge(mainwin):
	global _mainwin,log
	_mainwin = mainwin
	log = []
	#ok("Bridge is starting up")
	_mainwin.clear()
	_mainwin.addstr(0, 0, "Bridge is starting up, Log: ")
	_mainwin.refresh()
	bridge_and_sniff(config.data["interface1"], config.data["interface2"], xfrm12=pkt_callback_i1, xfrm21=pkt_callback_i2, count=0, store=0)
	_mainwin.clear()
	_mainwin.addstr(0, 0, "Bridge stopped")
	_mainwin.refresh()
	print("bye!!")

conf.verb=3
conf.sniff_promisc=True

_mainwin = None
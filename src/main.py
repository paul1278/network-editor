from scapy.all import conf,bridge_and_sniff,UDP,Raw,Ether,IP,TCP
from utils import *
import workspace
import traceback

conf.verb=3
conf.sniff_promisc=True


def pkt_callback_i1(pkt):
	return handlePaket(pkt, 0)

def pkt_callback_i2(pkt):
	return handlePaket(pkt, 1)

def handlePaket(pkt, direction):
	ret = True
	debug(workspace.data["interface" + str(direction +1)] + ":", "Got packet", pkt)
	if workspace.data.get("rewriteMAC", None) == True:
		if direction == 0:
			pkt[Ether].dst = workspace.data["mac2"]
			pkt[Ether].src = workspace.data["localmac2"]
		else:
			pkt[Ether].dst = workspace.data["mac1"]
			pkt[Ether].src = workspace.data["localmac1"]
		if pkt.haslayer(TCP):
			pkt[TCP].chksum = None
			pkt[TCP].len = None

		pkt = Ether(bytes(pkt))
	
	for f in workspace.filters:
		if pkt == False or pkt == True:
			return pkt
		testingFilter = workspace.filters[f]
		if testingFilter.enabled == False:
			continue
		try:
			if testingFilter.check(pkt, direction):
				debug("Filter", f, "is true")
				for a in testingFilter.actions:
					if pkt == False or pkt == True:
						return pkt
					action = workspace.actions[a]
					pkt = action.modPaket(pkt)
					ok("Action", a, "changed the packet by filter", f)
		except Exception as e:
			error("Filter", f, "threw an exception, dropping the packet", repr(e))
			debug(traceback.format_exc(chain=False))
	return pkt


# UI things #
_mainwin = None
log = []
def prepareWin():
	if(_mainwin == None):
		return
	setLoggingFunc(appendLog)
	_mainwin.clear()
	_mainwin.addstr(0, 0, "Bridge is starting up, Log: ")
	_mainwin.refresh()

def stopWin():
	if(_mainwin == None):
		return
	_mainwin.clear()
	_mainwin.addstr(0, 0, "Bridge stopped")
	_mainwin.refresh()

def printWin(log):
	if(_mainwin == None):
		return
	dims = _mainwin.getmaxyx()
	h = dims[0] - 1
	lsize = len(log)
	for i in range(h):
		j = lsize - i - 1
		if j < 0:
			break
		_mainwin.addstr(h - i,0,log[j])
	_mainwin.refresh()

def appendLog(*entry):
	log.append(
		" ".join(
			map(
				lambda s: str(s)
			,entry
			)
		)
	)
	printWin(log)

# Start everything #
def start_bridge(mainwin):
	global _mainwin,log
	_mainwin = mainwin
	prepareWin()
	log = []
	ok("Bridge is starting up")
	bridge_and_sniff(workspace.data["interface1"], workspace.data["interface2"], xfrm12=pkt_callback_i1, xfrm21=pkt_callback_i2, count=0, store=0)
	stopWin()
	ok("Bridge is now down")
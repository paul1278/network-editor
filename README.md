# Network-Editor: PInterceptor
> **This product is for educational purposes only! You are not allowed to use it for anything illegal or something, you don't have permissions for.**

This tool will allow you to modify network traffic as a Man-in-the-middle.
You can define a `filter`, which matches packets against your conditions and will trigger `actions`.
Those will modify the packets.

It is pretty simple to use - as long you can write some simple `python`-code.
If not, just head over to the example workspace under [/workspace/demoWorkspace](`https://github.com/paul1278/network-editor/tree/main/workspace/demoWorkspace`), there is a simple example.

## Installation
To install the software, use the provided `.deb`-file under the release-section of this repo.
If you want to build it yourself from source, you can do the following:
```
git clone https://github.com/paul1278/network-editor
cd network-editor/build
./build.sh

sudo dpkg -i network-editor.deb

sudo pintercepter
```
This will produce the `.deb`-file. Otherwise you can simply use the project as-is with `python3`. For that, run `start.py`.

## Project setup
You need to create a `workspace` which contains all needed files.
Simply copy the `demoWorkspace` from this repo, this is the structure you need.

Edit the `workspace.yaml`-file as needed:
```yaml
protocols:
  - my_protocol_filename

filter:
  - loaded_filter_name1

# The interface's which are the bridge
interface1: eth0
interface2: eth1

# The interface MAC-adresses of the devices
mac1: 02:42:ac:12:00:02
mac2: 02:42:ac:13:00:02

# The local MAC-adresses
localmac1: 02:42:ac:12:00:05
localmac2: 02:42:ac:13:00:05

# When true, you are a full IPv4-device - respond to ARP etc.
# Set to false, when you want to be totally transparent (also deactivate IP-stack on your device) - in this case you don't need the mac-addresses above.
rewriteMAC: true
```

## Running the tool
After installing the package, you can use it under `pinterceptor`.
Otherwise, run `start.py` using `python3`.

The command-line is pretty simple:
```
root@interceptor:/main# python3 start.py -h
 (   (                                                 
 )\ ))\ )         )                          )         
(()/(()/(      ( /(  (  (         (       ( /(    (    
 /(_))(_))(    )\())))\ )(   (   ))\`  )  )\())(  )(   
(_))(_))  )\ )(_))//((_|()\  )\ /((_)(/( (_))/ )\(()\  
| _ \_ _|_(_/(| |_(_))  ((_)((_|_))((_)_\| |_ ((_)((_) 
|  _/| || ' \))  _/ -_)| '_/ _|/ -_) '_ \)  _/ _ \ '_| 
|_| |___|_||_| \__\___||_| \__|\___| .__/ \__\___/_|   
                                   |_|                 
[+] Starting up
usage: start.py [-h] [-w WORKSPACE] [-i] [-v]

options:
  -h, --help            show this help message and exit
  -w WORKSPACE, --workspace WORKSPACE
                        Give a path to a ready workspace
  -i, --interactive     Start with a UI
  -v, --verbose         Enable debug mode without config
```
If you want to see debug output on incoming / outgoing packets, we suggest turning on verbose-mode.

## Writing modules
### Protocols
Protocols are written for `scapy` and must match the syntax accordingly. Just head to the [`scapy`-docs](https://scapy.readthedocs.io/en/latest/build_dissect.html) for that.
Using the function `bind_layers` you can add your protocol to the layers.

```python
from scapy.all import Packet, XByteField, bind_layers, TCP

class CoffeeProtocolPriceList(Packet):
    name = "CoffeeProtocolPriceList"
    fields_desc=[XByteField("actionType", 0)]

bind_layers(TCP, CoffeeProtocolPriceList, sport=44445)
```
To activate a protocol, simply use the module-name on the `workspace.yaml`.

### Filters
A filter should match a packet to perform actions on it.
It consists of a function called `check` and a list\<String\> called `actions`:
```python
from scapy.all import TCP,Raw
from workspace import protocols

def check(pkt, direction):
  return pkt.haslayer(protocols.demo.CoffeeProtocolPriceList)

actions = ["demoPayload"]
```
Each packet will be checked by your `check`-function, which should return `True` or `False`.
If you return `True`, the program will launch each action from the `actions`-list.
The actions are actually the file-names and the filters must be activated using the module-filename inside the `workspace.yaml`.

### Actions
An action receives a packet using the `modPaket(pkt)`-function.
Make your changes there and return the packet again. Make sure to recalculate checksums when needed:
```python
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
```
You can also include your custom protocols using `workspace.protocols`.

## Running the demo
The demo consists of three parts:
* COFFEE_SERVER: A server which will return a price-list for a COFFEE_MACHINE
* COFFEE_MACHINE: An industrial coffee-machine which needs the price list for your customers.
* MALLORY: The MITM in between.

### The demo-protocol
The demo uses a custom protocol.

The machine will send a request to the server, which contains an action-byte:
```
+-------------------------------------------+
... Ethernet / IP / TCP ... | 1 Byte Action |
+-------------------------------------------+
```
This is `01h` for "getPrices". The response is as simple as:
```
+--------------------------------------------+
|... Ethernet / IP / TCP ... | 1 Byte Action |
| 8 Byte product-name | 1 Byte price | etc.  |
+--------------------------------------------+
```
For this protocol there is a whole wrapper, a filter which recognizes the answer and an action, which changes prices and product-names. Just play around with that!

You can start it using `sudo docker-compose -f docker-compose.demo.yml up -d`.
Connect to mallory using `sudo docker-compose -f docker-compose.demo.yml exec mallory bash`.
After that, run the application using `python start.py -w /opt/workspace/demoWorkspace -d`.
You can see the changes when running the machine:
```bash
sudo docker-compose -f docker-compose.demo.yml exec coffee_machine bash
python3 coffee_client.py
```
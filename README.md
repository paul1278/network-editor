# Network-Editor
This tool will allow you to modify network traffic as a Man-in-the-middle.
You can define `filter`, which must match packets and will trigger `actions`.
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
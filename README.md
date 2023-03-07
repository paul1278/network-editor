# Network-Editor
This tool will allow you to modify network traffic as a Man-in-the-middle.
You can define `filter`, which must match packets and will trigger `actions`.
Those will modify the packets.

It is pretty simple to use - as long you can write some simple `python`-code.
If not, just head over to the example workspace under [/workspace/demoWorkspace](`https://github.com/paul1278/network-editor/tree/main/workspace/demoWorkspace`), there is a simple example.

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
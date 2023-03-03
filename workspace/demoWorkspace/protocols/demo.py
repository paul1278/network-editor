from scapy.all import Packet, XByteField, PacketListField, StrFixedLenField, bind_layers, TCP

class CoffeeProtocolProduct(Packet):
    name = "CoffeeProtocolProduct"
    fields_desc=[StrFixedLenField("productName",0, 8), XByteField("price", 0)]
    # https://stackoverflow.com/a/8101584
    def extract_padding(self, s):
        return '', s

class CoffeeProtocolPriceList(Packet):
    name = "CoffeeProtocolPriceList"
    fields_desc=[XByteField("actionType", 0), PacketListField("products", None, CoffeeProtocolProduct)]

bind_layers(TCP, CoffeeProtocolPriceList, sport=44445)
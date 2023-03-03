FROM ubuntu

RUN apt update && apt install iproute2 netcat tshark net-tools -y
RUN apt install -y python3

CMD "/main.sh"
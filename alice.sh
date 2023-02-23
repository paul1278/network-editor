#!/bin/bash
ip route change default via 172.18.0.5
while true; do
  echo nice | nc -q 1 172.19.0.2 4444 -w 1
  echo "Sending"
  sleep 1
done
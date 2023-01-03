#!/bin/bash
ip route change default via 172.18.0.5
while true; do
  echo nice | nc -u -q 1 172.19.0.2 4444
  echo "Sending"
  sleep 1
done
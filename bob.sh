#!/bin/bash
ip route change default via 172.19.0.5
while true; do
  nc -unlvp 4444 -w 0
  sleep 2
done
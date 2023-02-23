#!/bin/bash
ip route change default via 172.19.0.5
while true; do
  nc -nlvp 4444 
  sleep 2
done
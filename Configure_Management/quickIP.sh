#!/bin/bash

nmap -T4 -sn -e tun0 10.8.0.1-255|grep 10.8.0.* > ipList.txt
ipList=$(cat ipList.txt)
echo -e ${ipList}#!/bin/bash


#!/bin/bash
nmap -T4 -sn -e tun0 10.8.0.1|grep 10.8.0.1 > hostIP.txt
hostIP = $(cat hostIP.txt)

if [ !$hostIP ]; then
    sudo cp -rf /etc/openvpn/client_tcp2_backup.ovpn /etc/openvpn/client_tcp.ovpn
    echo "host not Found,rebooting"
    sudo reboot
else
    echo "host is Found"
fi
#!/usr/bin/env bash
# Get the interface name (assumes the interface is the first line output by `wg show`)
#interface=$(sudo wg show | grep '^interface:' | awk '{print $2}')
interface="nmd"
# Check if there is a recent handshake (this indicates the connection is active)
handshake=$(ip a show "$interface" | grep 'link')

if [[ -n "$handshake" ]]; then
  echo "🔒 $interface"
else
  echo "🌀"
fi

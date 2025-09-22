#!/usr/bin/env bash

# Get the interface name (change this to your actual WireGuard interface name if needed)
interface="nmd"

handshake=$(ip a show "$interface" | grep 'link')

# Check if WireGuard is up
if [[ -n "$handshake" ]]; then
  # If it's up, bring it down
  pkexec wg-quick down "$interface"
  notify-send -a "WireGuard" "Disconnected from $interface" -h string:x-canonical-private-synchronous:vpn
else
  # Otherwise, bring it up
  pkexec wg-quick up "$interface"
  notify-send -a "WireGuard" "Connected to $interface" -h string:x-canonical-private-synchronous:vpn
fi

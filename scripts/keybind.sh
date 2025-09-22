#!/usr/bin/env bash

GTK_THEME_NAME="Nightfox-Dark"
# Path to your Hyprland config file
config_file=~/.config/hypr/hyprland.conf

# Fetch keybinds from the config file
keybinds=$(grep -oP '(?<=bind=).*' $config_file)

# Clean up the keybinds (adjusting commas and removing unwanted text)
keybinds=$(echo "$keybinds" | sed 's/,\([^,]*\)$/ = \1/' | sed 's/, exec//g' | sed 's/^,//g')

# Pipe the keybinds into wofi for selection
echo "$keybinds" | GTK_THEME="${GTK_THEME_NAME}" rofi -dmenu -prompt "Keybinds" 


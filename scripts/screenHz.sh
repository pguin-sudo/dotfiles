#!/usr/bin/env bash

if hyprctl monitors | grep '2560x1600@120.00000'; then
	json='{"text": "60", "tooltip": "Frequency", "class": "custom/power-menu", "percentage": 60 }'
	echo -e $json >~/.config/hypr/scripts/hz.json
	hyprctl keyword monitor eDP-1,2560x1600@60,0x0,1.25 && notify-send "Set to 60Hz" -a "Monitor" -u "low" -i "/home/pguin/icons/desktop.png" -r "123"
	exit
fi
if hyprctl monitors | grep '2560x1600@90.00000'; then
	json='{"text": "120", "tooltip": "Frequency", "class": "custom/power-menu", "percentage": 120 }'
	echo -e $json >~/.config/hypr/scripts/hz.json
	hyprctl keyword monitor eDP-1,2560x1600@120,0x0,1.25 && notify-send "Set to 120Hz" -a "Monitor" -u "low" -i "/home/pguin/icons/desktop.png" -r "123"
	exit
fi
if hyprctl monitors | grep '2560x1600@60.00200'; then
	json='{"text": "90", "tooltip": "Frequency", "class": "custom/power-menu", "percentage": 90 }'
	echo -e $json >~/.config/hypr/scripts/hz.json
	hyprctl keyword monitor eDP-1,2560x1600@90,0x0,1.25 && notify-send "Set to 90Hz" -a "Monitor" -u "low" -i "/home/pguin/icons/desktop.png" -r "123"
	exit
fi

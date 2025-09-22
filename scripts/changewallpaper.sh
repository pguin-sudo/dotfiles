#!/bin/bash

# Directory containing wallpapers
WALLPAPER_DIR="$HOME/Desktop/wallpapers"

# File to keep track of the current wallpaper index
INDEX_FILE="$HOME/.current_wallpaper_index"

# Find images in the wallpaper directory (supports .jpg, .jpeg, and .png)
wallpapers=($(find "$WALLPAPER_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \)))

# Check if any wallpapers are found
if [[ ${#wallpapers[@]} -eq 0 ]]; then
  echo "No wallpapers found in the directory: $WALLPAPER_DIR"
  exit 1
fi

# Read the current index from the file or set it to 0 if it doesn't exist
if [[ -f $INDEX_FILE ]]; then
  current_index=$(cat $INDEX_FILE)
else
  current_index=0
fi

# Calculate the next index, looping back to 0 if needed
next_index=$(( (current_index + 1) % ${#wallpapers[@]} ))

# Set the next wallpaper
next_wallpaper="${wallpapers[$next_index]}"
hyprctl hyprpaper preload "$next_wallpaper"
hyprctl hyprpaper wallpaper ,"$next_wallpaper"

# Save the new index to the file
echo $next_index > $INDEX_FILE


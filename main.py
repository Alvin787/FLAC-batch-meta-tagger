#!/usr/bin/env python3
import os
import sys
import argparse
import glob
import re
from mutagen.flac import FLAC

def natural_keys(text):
    """
    Sort helper: splits text into list of strings and integers for natural sort order.
    E.g., "jm2010-08-30t01.flac" sorts numerically by the digit portions.
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split('(\d+)', text)]

def sanitize_filename(name):
    """
    Allow only alphanumeric characters, spaces, dots, underscores, and hyphens.
    """
    return re.sub(r'[^a-zA-Z0-9\.\_\- ]', '', name)

def main():
    parser = argparse.ArgumentParser(
        description="Update FLAC metadata and rename files based on a track list."
    )
    parser.add_argument("music_dir", help="Directory containing FLAC files")
    parser.add_argument("track_file", help="Text file containing the track list")
    parser.add_argument("artist", help="Artist name")
    parser.add_argument("album", help="Album name")
    parser.add_argument("date", help="Date/Year")
    args = parser.parse_args()

    music_dir = args.music_dir
    track_file = args.track_file
    artist = args.artist
    album = args.album
    date = args.date

    # --- Part 1: Update Metadata ---
    print("Updating metadata for FLAC files...")
    flac_files = glob.glob(os.path.join(music_dir, "*.flac"))
    # Sort files in natural order so the track order matches the track list
    flac_files_sorted = sorted(flac_files, key=natural_keys)

    for file_path in flac_files_sorted:
        try:
            audio = FLAC(file_path)
            # Set metadata tags (Mutagen accepts strings for FLAC tags)
            audio["artist"] = artist
            audio["album"] = album
            audio["date"] = date
            audio.save()
            print(f"  Updated metadata for: {file_path}")
        except Exception as e:
            print(f"Error updating metadata for {file_path}: {e}")

    # --- Part 2: Rename Files Based on the Track List ---
    print("Reading track list from:", track_file)
    try:
        with open(track_file, "r", encoding="utf-8") as f:
            # Read non-empty lines and strip whitespace
            tracks = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print("Error reading track file:", e)
        sys.exit(1)

    if len(tracks) != len(flac_files_sorted):
        print(f"Warning: Number of tracks ({len(tracks)}) does not match number of FLAC files ({len(flac_files_sorted)}).")
        sys.exit(1)

    print("Renaming files...")
    for i, file_path in enumerate(flac_files_sorted):
        # Get the track name from the list
        track_name = tracks[i]
        # Remove any leading track numbers and colon (e.g., "01: ")
        track_name = re.sub(r'^[0-9]+\:\s*', '', track_name)
        # Remove trailing markers such as an arrow (if present)
        track_name = re.sub(r'\s*[-]>$', '', track_name)
        # Sanitize the track name for safe filenames
        safe_name = sanitize_filename(track_name)
        new_file = os.path.join(music_dir, f"{safe_name}.flac")
        try:
            os.rename(file_path, new_file)
            print(f"  Renamed: {file_path} -> {new_file}")
        except Exception as e:
            print(f"Error renaming {file_path} to {new_file}: {e}")

    print("Done.")

if __name__ == "__main__":
    main()
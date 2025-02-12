#!/usr/bin/env python3
import os
import sys
import argparse
import glob
import re
from mutagen.flac import FLAC

def natural_keys(text):
    """
    Splits text into list of strings and integers for natural sorting.
    Example: "jm2010-08-30t01.flac" sorts numerically by the digit portions.
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

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

    # --- Get and Sort FLAC Files ---
    flac_files = glob.glob(os.path.join(music_dir, "*.flac"))
    if not flac_files:
        print("No FLAC files found in the specified directory.")
        sys.exit(1)
    flac_files_sorted = sorted(flac_files, key=natural_keys)

    # --- Read Track List ---
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

    # --- Update Metadata (Artist, Album, Date) for Each FLAC File ---
    print("Updating metadata for FLAC files (Artist, Album, Date)...")
    for file_path in flac_files_sorted:
        try:
            audio = FLAC(file_path)
            audio["artist"] = artist
            audio["album"] = album
            audio["date"] = date
            audio.save()
            print(f"  Updated metadata for: {file_path}")
        except Exception as e:
            print(f"Error updating metadata for {file_path}: {e}")

    # --- Rename Files Based on the Track List and Update Track Numbers ---
    print("Renaming files and updating track numbers...")
    for i, old_file in enumerate(flac_files_sorted):
        # Get the track name from the list (the order of the track list determines track number)
        track_name = tracks[i]
        # Remove any leading track numbers and colon (e.g., "01: ") if present
        track_name = re.sub(r'^[0-9]+\:\s*', '', track_name)
        # Remove trailing markers (e.g., arrow characters) if needed
        track_name = re.sub(r'\s*[-]>$', '', track_name)
        # Sanitize the track name for a safe filename
        safe_track = sanitize_filename(track_name)
        new_file = os.path.join(music_dir, f"{safe_track}.flac")
        
        print(f"  Renaming: {old_file} -> {new_file}")
        try:
            os.rename(old_file, new_file)
        except Exception as e:
            print(f"Error renaming {old_file} to {new_file}: {e}")
            continue

        # Open the renamed file and update the track number metadata (order from track list)
        try:
            audio = FLAC(new_file)
            audio["tracknumber"] = str(i + 1)
            audio.save()
            print(f"    Updated tracknumber to {i + 1} for: {new_file}")
        except Exception as e:
            print(f"Error updating track number for {new_file}: {e}")

    print("Done.")

if __name__ == "__main__":
    main()
# FLAC Metadata Batch Updater (Python Version)

## Overview

This repository contains a Python script that updates FLAC file metadata and renames files based on an input track list. The script performs two primary tasks:

## Features
- **Update Metadata:**  
  Sets the Artist, Album, and Date tags for each FLAC file using the [Mutagen](https://mutagen.readthedocs.io/) library.
  
- **Rename Files:**  
  Renames each FLAC file based on an ordered list of track names provided in a text file. The script cleans up each track name by removing any leading track numbers or unwanted characters and then uses a sanitized version of the track name for the new filename.

## Use Case

Many albums available on [archive.org](https://archive.org/) are uploaded in FLAC format but lack proper organization. The FLAC files may have confusing file names and missing metadata, making it difficult to use them directly on popular music players such as Apple Music, Foobar2000, MusicBee, etc. This tool is designed to help you:

- **Organize Downloaded Albums:**  
  Automatically update metadata and rename files so that each track is correctly labeled.

- **Enhance Local Listening Experience:**  
  Once processed, your music players will recognize the files as a cohesive album with the proper track order and metadata.

- **Simplify Post-Download Cleanup:**  
  Instead of manually renaming files and updating metadata, simply provide a track list and desired metadata, and let the script do the rest.

## Installation
- Clone the repository locally in the location of your choice
```
   git clone https://github.com/yourusername/flac-meta-tagger.git
```

- Navigate to the cloned repository location 
```
   cd /your-folder-location/flac-meta-tagger
```

- Install dependencies
```
    pip3 install -r requirements.txt
```

## Usage
- **Track List Format**
    Within the same repository location, create a text file (e.g., tracklist.txt) with one track per line. The list can either include track numbers (e.g., 01: Intro) or just the track names. The script will automatically remove any leading numbers and punctuation if present.

Example with Track Numbers:
```
    01: Intro (Chest Fever)
    02: Vultures
    03: Clarity
    04: Why Georgia
    05: Ain't No Sunshine &
    ...
```
Example without Track Numbers:
```
    Intro
    Vultures
    Clarity
    Why Georgia
    Ain't No Sunshine &
    ...
```

## Run the Python script with the following command:
```
    python3 main.py /path/to/flac/files tracklist.txt "Artist Name" "Album Name" "Date"
```

Example command: 
```
python3 main.py /Users/alvinqian/Music/jm2010-07-30 tracklist.txt "John Mayer" "Live at Susquehanna Bank Center on 2010-07-30" "2010-07-30"
```

Parameters:
```
        •	/path/to/flac/files:
    The directory containing your FLAC files.
        •	tracklist.txt:
    The path to your track list file.
        •	“Artist Name”, “Album Name”, “Date”:
    Replace these with the actual metadata values you wish to set.
```

## Notes:
- **File Count Match:**
    Ensure the number of lines in your track list matches the number of FLAC files in the target folder.

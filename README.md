# Anilist to MAL
Anilist to MAL is a simple python tool that lets you export your anime list from [AniList](https://anilist.co) to [MyAnimeList](https://myanimelist.net).

## Changes of this fork

* This version allows to export a **specific list** (with -l option) created in your Anilist profile in order to export only the contents of this list and not full list. (Only implemented for XML format)

## Usage
This app requires [Python 3](https://www.python.org/downloads/) and [Python Requests](http://docs.python-requests.org/en/master/).

Install Python Requests with `pip3 install requests`.

Once both are installed, run the app with `python3 main.py` and follow the instructions!

### Arguments
In addition to the step-by-step method, you can pass some arguments to the script.

- `-f`: set filetype (default `xml`)
  - options: `xml`, `txt`
  - txt will generate a markdown-compatible list format text file
- `-u`: set username (default `''`)
- `-t`: set list type (default `''`)
  - options: `anime`, `manga`
- `-n`: takes one argument, set the file name to be exported to

- `-s`: takes zero arguments, run in silent mode (no non-essential prints)
- `-p`: takes zero arguments, show progress while running

- `-l`: select a specific list to export of your profile (default `''`)
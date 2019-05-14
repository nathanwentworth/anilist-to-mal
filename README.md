# *IMPORTANT*
It seems like anilist's GraphQL API has changed in the last few months, so currently this does not work. I'll try to have a fix up as soon as possible.

# Anilist to MAL
Anilist to MAL is a simple python tool that lets you export your anime list from [AniList](https://anilist.co) to [MyAnimeList](https://myanimelist.net).

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

## Issues
Feel free to leave an issue on Github or [tweet at me](https://twitter.com/nathanwentworth)

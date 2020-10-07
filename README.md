# eargasm2spotify
**by Adam Siemaszkiewicz**

## Introduction

This is a Python script meant to migrate a Wordpress database dump containing songs formerly published to my music blog [eargasmusic.com](https://eargasmusic.com/) to Spotify monthly playlists at [eargasm Spotify channel](https://open.spotify.com/user/eargasmusic?si=PzTNDEa_TyOBCe8s1oA2Kw). 

*The project is meant to practise knowledge learnt thanks to [Python for Everybody Course](https://github.com/adamsiemaszkiewicz/coursera_python-for-everybody) but at the same time to automitize the migration which, when manually-done, would be ultra time-consuming.*

## Files

### Posts-Export-2019-April-27-1417.csv

The CSV dup file containing quite a messy list of songs published to [eargasmusic.com](https://eargasmusic.com/).

### fetch_from_csv.py

The script is meant to import the CSV file, fetch the song names, clean them up and organize them nicely in a chronological order in a database file using SQLite.

### eargasm.sqlite

The SQLite file containing nicely organized songs. 

### send_to_spotify.py

The script uses [Spotipy library](https://github.com/plamere/spotipy) to authenticate the user, fetch the songs from the SQLite file, create empty monthly playlists, search for the songs on Spotify and add songs to the respective monthly playlists. If the song is not found (quite common) the script creates files containing failed song names. The script includes some debugging.

## Thank you!


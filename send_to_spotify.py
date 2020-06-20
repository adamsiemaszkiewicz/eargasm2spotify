# BEGIN LIBRARIES IMPORT

# Import for spotify API handling
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# Import for date stripping
from datetime import datetime
# Import for database creation
import sqlite3

# END LIBRARIES IMPORT



# BEGIN SPOTIFY PREPARATION

# Set client ID and secret codes
client_id 	= '855da9372490409f8c91294cb7bded92'
client_secret = 'bdf605a0de9c4cb5bdf28fcca1c9ef1a'
user_id = 'bb1lourrmw2toc01eq4fqgi9o'

credentials = SpotifyClientCredentials(
    client_id = client_id,
    client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

# END SPOTIFY PREPARATION



# BEGIN DATABASE PREPARATION

# Establish a connection to a database file or create a new file
conn = sqlite3.connect('eargasm.sqlite')
# Create a connection cursor
cur = conn.cursor()

# END DATABASE PREPARATION

# Select all columns from Locations table
cur.execute('SELECT date FROM Songs')
date = cur.fetchone()[0]
print(date)


#playlist_name = input('Enter the name of the playlist: ')
#sp.user_playlist_create(user_id, playlist_name, public=True, description='')

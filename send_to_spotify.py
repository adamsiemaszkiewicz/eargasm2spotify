# BEGIN LIBRARIES IMPORT

# Import for spotify API handling
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
# Import for date stripping
from datetime import datetime
# Import for database creation
import sqlite3

# END LIBRARIES IMPORT



# BEGIN SPOTIFY PREPARATION

# set SPOTIPY_CLIENT_ID=None
# set SPOTIPY_CLIENT_SECRET=None
# set SPOTIPY_REDIRECT_URI=None


# Set client ID and secret codes
client_id 	= '855da9372490409f8c91294cb7bded92'
client_secret = 'bdf605a0de9c4cb5bdf28fcca1c9ef1a'
user_id = 'bb1lourrmw2toc01eq4fqgi9o'
redirect_uri = 'http://eargasmusic.com/'
scopes = 'playlist-read-collaborative playlist-modify-private playlist-modify-public playlist-read-private'



# BEGIN SPOTIFY CONNECTION

token = util.prompt_for_user_token(username=user_id,
                                   scope=scopes,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)

print('Spotify access for authorized.')

# END SPOTIFY CONNECTION



# BEGIN DATABASE PREPARATION

# Establish a connection to a database file or create a new file
conn = sqlite3.connect('eargasm.sqlite')
# Create a connection cursor
cur = conn.cursor()

print('Database connection established.')
# END DATABASE PREPARATION


yearmonth = input('Specify year and month of the playlist (YYYY MM): ')
if len(yearmonth) < 7 :
    print('Wrong date')
    quit()
year = yearmonth[0:4]
month = yearmonth[5:7]
playlist_name = 'eargasm ' + month + '/' + year

playlists = sp.user_playlists(user_id)['items']

for playlist in playlists :
    if playlist['name'] == playlist_name :
        print('Playlist', '"', playlist['name'], '"', 'already exists')
        quit()
    continue

sp.user_playlist_create(user_id, playlist_name, public=True, description='created by eargasm2spotify')
print('Playlist', '"', playlist_name, '"', 'successfully created')


# Select all columns from Locations table
cur.execute('''
SELECT
    artist, title
FROM
    Songs
WHERE
    strftime('%Y', date) = ?
AND
    strftime('%m', date) = ?
''', (year,month))
date = cur.fetchall()

#for song in date :
#    print(song)

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

print('Libraries imported.')
pause = input('Press enter to continue...')

# BEGIN SPOTIFY PREPARATION

# set SPOTIPY_CLIENT_ID=None
# set SPOTIPY_CLIENT_SECRET=None
# set SPOTIPY_REDIRECT_URI=None



# Set client ID and secret codes

client_id 	= input('Enter your Spotify client_id ')
client_secret = input('Enter your Spotify client_secret ')
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


# END SPOTIFY CONNECTION

print('Spotify access for authorized.')
pause = input('Press enter to continue...')

# BEGIN DATABASE PREPARATION

# Establish a connection to a database file or create a new file
conn = sqlite3.connect('eargasm.sqlite')
# Create a connection cursor
cur = conn.cursor()



# END DATABASE PREPARATION

print('Database connection established.')
pause = input('Press enter to continue..')

# BEGIN PLAYLIST CREATION

while True :

    # Prompt for a year and a month of a playlist
    yearmonth = input('Specify year and month of the playlist (YYYY MM): ')
    # If output longer than expected quit
    if len(yearmonth) < 7 :
        print('Wrong date')
        quit()
    # Split output into hear and month variables
    year = yearmonth[0:4]
    month = yearmonth[5:7]


    # Create a playlist name syntax
    playlist_name = 'eargasm ' + month + '/' + year

    # Fetch all playlists by user
    playlists = sp.user_playlists(user_id)['items']

    print('Working on playlist', playlist_name, '.')
    pause = input('Press enter to continue...')

    exists = None
    # Run a loop through playlists to check if playlist already exists
    for playlist in playlists :
        # If playlist_name already exists in the library
        if playlist['name'] == playlist_name :
            # Display monit
            print('Playlist', '"', playlist['name'], '"', 'already exists.')
            # Set exists variable to true and escape loop
            exists = True
            break

    # If playlists doesn't exist create a new one
    if exists == None :
        # Create a public playlist for specified user
        sp.user_playlist_create(user_id, playlist_name, public=True, description='created by eargasm2spotify')
        # Display confirmation
        print('Playlist', '"', playlist_name, '"', 'successfully created')

    # Fetch all playlists again
    playlists = sp.user_playlists(user_id)['items']

    for playlist in playlists :
        if playlist['name'] == playlist_name :
            playlist_uri = playlist['uri'].split(':')
            playlist_id = playlist_uri[2]


    # Select all columns from Locations table
    cur.execute('''
    SELECT
        artist, title, date, uri
    FROM
        Songs
    WHERE
        strftime('%Y', date) = ?
    AND
        strftime('%m', date) = ?
    ''', (year,month))

    songs = cur.fetchall()


    failed_log = 'failed_' + year + '-' + month + '.txt'
    # Create a file handle with read-write permission
    file = open(failed_log,"w+", encoding='UTF-8')

    for song in songs :
        track = song[3]

        if track == '0' :
            try:
                print('Failed to add', song[0], '-', song[1], 'from', song[2], 'to', playlist_name)
                failed_name = (song[0], song[1])
                failed_name = ' - '.join(failed_name) + '\n'
                file.write(failed_name)
            except : pass
            continue
        else :
            sp.user_playlist_add_tracks(user_id, playlist_id, tracks=[track], position=None)
            print('Successfully added', song[0], '-', song[1], 'from', song[2], 'to', playlist_name)
            #track_id = track.split(':')[2]
            #print(track)

    print('Playlist', playlist_name, 'completed.')
    print('See ', failed_log, 'for list of failed tracks.')


# Commit changes and close connection to the database
conn.close()
file.close()

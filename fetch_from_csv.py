# BEGIN LIBRARIES IMPORT

# Import for spotify API handling
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# Import for CSV file importing
import csv
# Import for date stripping
from datetime import datetime
# Import for database creation
import sqlite3

# END LIBRARIES IMPORT



# BEGIN SPOTIFY PREPARATION

# Set client ID and secret codes
client_id 	= '855da9372490409f8c91294cb7bded92'
client_secret = 'bdf605a0de9c4cb5bdf28fcca1c9ef1a'

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

# Drop the database tables if exist and create new ones
cur.executescript('''
DROP TABLE IF EXISTS Songs;

CREATE TABLE Songs (
    id     INTEGER UNIQUE,
    artist   TEXT,
    title   TEXT,
    uri   TEXT,
    date   TEXT
)
''')

# END DATABASE PREPARATION



# BEGIN CSV import

# Open CSV file in UTF-8 encoding
with open('Posts-Export-2019-April-27-1417.csv', encoding='utf-8') as csv_file:
    # Create a reader object from csv_file with , as a delimiter
    csv_reader = csv.reader(csv_file, delimiter=',')
    # Initiate a line counter
    line_count = 0


    # Run a loop through the reader
    for row in csv_reader:
        # Run during first iteration
        if line_count == 0:
            # Display the first row with tuple joint into a string
            #print(f'Column names are {", ".join(row)}')
            # Add 1 to counter
            line_count += 1
        # For all other iterations
        else:
            # Assign second row entry to date (string)
            date_str = row[1]
            # Convert date string into date object
            date = datetime.strptime(date_str, '%Y%m%d').date()
            # Assign third row entry to name
            name = row[2]
            # Split the name with || delimiter
            name = name.split('||')

            # If no delimited set artist only
            if len(name) < 2 :
                artist = name[0]
                title = None
            # Else set artist and title
            else :
                artist = name[0]
                title = name[1]

            # Add 1 to counter
            line_count += 1

            # Create a track_id variable
            id = line_count - 1
            # Create a song name string by joining artist-title 'name' tuple
            single_song = "".join(name)
            # Search for a song and store in results using Spotify API
            results = sp.search(single_song, type='track')
            # If nothing found set song_uri to 0
            if len(results['tracks']['items']) < 1 : song_uri = 0
            # Else fetch the uri from API
            else : song_uri = results['tracks']['items'][0]['uri']
            # Insert or ignore song meta data into the database
            cur.execute('''INSERT OR IGNORE INTO Songs
                (id, artist, title, uri, date) VALUES ( ?, ?, ?, ?, ? )''',
                ( id, artist, title, song_uri, date ) )

            # Print track info
            print('Track #', id, artist, title, date, song_uri)


# Commit changes and close connection to the database
conn.commit()
conn.close()

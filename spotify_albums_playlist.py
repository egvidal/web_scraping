# Web scraping

import requests
from bs4 import BeautifulSoup
import ftfy, re

URL = "https://www.angrymetalguy.com/tag/50/" #page/2/
playlist_name = "Iconic Metal Albums (from angrymetalguy.com)"

response = requests.get(URL)
content = response.text

soup = BeautifulSoup(content, "html.parser")
entries = soup.find_all(name="h2", class_="entry-title")
entries = soup.select(selector=".entry-title a")
print("Entries:", entries)

#Create albums list based on the embeded text

#angrymetalguy.com
#Fix the encoding to allow international chgaracters
#Filter out 'Review' and things like '[Vinyl Review] from the names
albums = [re.sub("\\sReview|\\s\[.*$", "", ftfy.fix_encoding(entry.getText())) for entry in entries]
print("Albums:", albums)


#Spotify

from os import environ
import spotipy
from spotipy.oauth2 import SpotifyOAuth

Client_ID = environ.get("SPOTIFY_CLIENT_ID")
Client_Secret = environ.get("SPOTIFY_CLIENT_SECRET")
Redirect_URI = "http://example.com"
scope = "playlist-modify-private"

album_uris = []
missing = []
# sp = spotipy.oauth2.SpotifyOAuth(client_id=Client_ID, client_secret=Client_Secret, redirect_uri=Redirect_URI, scope=scope)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_ID, client_secret=Client_Secret, redirect_uri=Redirect_URI, scope=scope))
user_id = sp.current_user()["id"]
# results = [sp.search(q="artist:" + album.split(' – ')[0] + " album:" + album.split(' – ')[1], type="album") for album in albums]
# print(results)
for  album in albums:
  result = sp.search(q="artist:" + album.split(' – ')[0] + " album:" + album.split(' – ')[1], type="album")
  print(result)
  try:
    album_uris.append(result["albums"]["items"][0]["uri"])
  except IndexError:
    print(f"{album} doesn't exist in Spotify. Skipped.")
    missing.append(album)

print("Album URIs:", album_uris)
print("Missing in Spotify:", missing)

# Get the album tracks
album_tracks = [sp.album_tracks(album_uri) for album_uri in album_uris]
print(album_tracks)

# Extract the track URIs from the album tracks
track_uris = [[track['uri'] for track in album['items']] for album in album_tracks]
print("Track URIs:", track_uris)

flatten_track_uris = [item for sublist in track_uris for item in sublist]
# print("Track URIs (flatten):", flatten_track_uris)

print("Albums count:", len(track_uris))
print("Tracks count:", len(flatten_track_uris))

playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
print(playlist)
playlist_id = playlist["id"]
try:
  status = sp.playlist_add_items(playlist_id=playlist_id, items=flatten_track_uris)
except Exception as e:
  print(e)
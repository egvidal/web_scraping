# Web scraping

import requests
from bs4 import BeautifulSoup

URL = "https://audioinkradio.com/2022/11/best-metal-songs-of-the-year/"
playlist_name = "BEST METAL SONGS OF 2022 (from audioinkradio.com)"

response = requests.get(URL)
content = response.text

soup = BeautifulSoup(content, "html.parser")
entries = soup.find_all(name="strong")
print("Entries:", entries)

#Create tracks list based on the embeded text

#audioinkradio.com
songs = [entry.getText() for entry in entries]
print("Songs:", songs)


#Spotify

from os import environ
import spotipy
from spotipy.oauth2 import SpotifyOAuth

Client_ID = environ.get("SPOTIFY_CLIENT_ID")
Client_Secret = environ.get("SPOTIFY_CLIENT_SECRET")
Redirect_URI = "http://example.com"
scope = "playlist-modify-private"

uris = []
missing = []
# sp = spotipy.oauth2.SpotifyOAuth(client_id=Client_ID, client_secret=Client_Secret, redirect_uri=Redirect_URI, scope=scope)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_ID, client_secret=Client_Secret, redirect_uri=Redirect_URI, scope=scope))
user_id = sp.current_user()["id"]
for  song in songs:
  result = sp.search(q="artist:" + song.split(', ')[0] + " track:" + song.split(', ')[1], type="track")
  print(result)
  try:
    # uris.append(result["albums"]["items"][0]["uri"])
    uris.append(result["tracks"]["items"][0]["uri"])
  except IndexError:
    # print(f"{album} doesn't exist in Spotify. Skipped.")
    # missing.append(album)
    print(f"{song} doesn't exist in Spotify. Skipped.")
    missing.append(song)

print("URIs:", uris)
print("Missing in Spotify:", missing)
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
print(playlist)
playlist_id = playlist["id"]
print("Playlist ID:", playlist_id)
try:
  status = sp.playlist_add_items(playlist_id=playlist_id, items=uris)
except Exception as e:
  print(e)
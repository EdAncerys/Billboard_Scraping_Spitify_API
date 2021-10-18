from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# env variables fro Spotify API
Client_ID = os.environ['Client_ID']
Client_Secret = os.environ['Client_Secret']
print('Client_ID: ' + str(Client_ID))
print('Client_Secret: ' + str(Client_Secret))

# date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
date = '2003-09-01'

# Scraping Billboard 100
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())
song_names_spans = soup.find_all("span", class_="chart-element__information__song")
song_names = [song.getText() for song in song_names_spans]
print(song_names)

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com/callback?code=AQAgOZS3XICJOYg_MYZCVBJCUCD50Lj8u-g2TD-6foVm2WKzcr5_9vhDsYUzfpFYefigrffBLZkmGZZdpsjuFEqzQeQ2GqkOsi6tn-BUhvVThBwGN7fEHPlhi66Ted2wNjBR6BIzk0Lt_ci6ZCQscgoUVRziOLFYn2Wrv8Yqbj6EYq0JPxAjevcWupGmOQasm1hjrp1kQMA",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
# print(user_id)

# Searching Spotify for songs by title & date
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# print(song_uris)

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
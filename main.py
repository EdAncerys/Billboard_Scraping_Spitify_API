from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
print(os.environ['Client_ID'])
print(os.environ['Client_Secret'])

# date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
date = '2003-09-01'

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())
song_names_spans = soup.find_all("span", class_="chart-element__information__song")
song_names = [song.getText() for song in song_names_spans]
print(song_names)


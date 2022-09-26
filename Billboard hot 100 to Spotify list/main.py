import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth


SPOTIPY_CLIENT_ID = "[HIDE]"
SPOTIPY_CLIENT_SECRET = "[HIDE]"
SPOTIPY_REDIRECT_URI = "http://example.com"
ROOT_URL = "https://www.billboard.com/charts/hot-100/"
SCOPE = "playlist-modify-private"

# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(url=f"{ROOT_URL}{date}")
soup = BeautifulSoup(response.text, "html.parser")
song_name_tags = soup.select(".o-chart-results-list__item h3.c-title")
song_names = [title.getText().strip() for title in song_name_tags]

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        show_dialog=True,
        cache_path="token.txt"
    ))

user_id = sp.current_user().get("id")
user_name = sp.current_user().get("display_name")

# Searching Spotify for songs by title
year = date.split("-")[0]
songs_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
        pass

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uris)

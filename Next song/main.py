"""
    The import section contains all necessary libaries for the complete functioning of this package
"""
import base64
import random
from urllib.parse import urlencode

import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials


class Songs:
    # https://developer.spotify.com/dashboard/applications/00faa139c54143a99a504fb7ab36a1dd
    """
    A class used to represent 3 different functions for fetching song data

    ...
    Attributes
    -----------
    get_random_song : str
        a formatted dictionary to return/print out a random song
    API: Spotify API
        Data that to format is retrieved using the spotify API

    -----------
    highest_rated_song : str
        Parsed HTML data to return/print the highest rated song
    WEB SCRAPPER:
        Data is retrieved using a web scrapper

    -----------
    search_song : str
        a formatted dictionary to return/print out a random song depending on a keyword search
    API: Spotify API
        Data that to format is retrieved using the spotify API
    """

    def __init__(self):
        # initilaize the spotify credentials
        self.spoti_cid = "5d7c819c734a42849b1b5b5a00380a25"
        self.spoti_client_secret = "4f13b1d932f84c4eb5c5f7c31ee8b22b"

    # method 1 returns a new random song
    def get_random_Song(self):
        """
        Retrives json data from the SPOTIFY API

        :return: A formatted dicitonary that portraying:
                "Artist name": artist_name,
                "Song title": song_title,
                "Album cover": album_cover
        """
        print("========================================================================\n")
        print("SPOTIFY API USED TO FETCH SONG\n")
        client_credentials_manager = SpotifyClientCredentials(client_id=self.spoti_cid,
                                                              client_secret=self.spoti_client_secret)
        sp_spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        country_uri = 'spotify:playlist:37i9dQZF1DWTkxQvqMy4WW'

        country_playlist = sp_spotify.playlist(country_uri)

        country_playlist = country_playlist["tracks"]["items"]
        song_details = []
        for song in country_playlist:
            # access all items in the tracks, where each item represents a track
            song = song["track"]["album"]
            artist_name = song["artists"][0]["name"]
            song_title = song["name"]
            album_cover = song["images"][0]["url"]

            spoti_song_info = {
                "Artist name": artist_name,
                "Song title": song_title,
                "Album cover": album_cover
            }
            song_details.append(spoti_song_info)

        randNum = random.randint(0, len(song_details))

        artist_name = song_details[randNum]["Artist name"]  # title
        print("Artist: ", artist_name)

        song_title = song_details[randNum]["Song title"]  # title
        print("Song title: ", song_title)

        album_cover = song_details[randNum]["Album cover"]  # title
        print("Cover: ", album_cover, end="\n\n================="
                                          "================="
                                          "================"
                                          "======================\n")

    def highest_rated_song(self):
        """
           Retrives data from the web using a web scrapper

           :return: A formatted dicitonary that portraying:
                   "Artist name": artist_name,
                   "Song title": song_title,
                   "Ranking": ranking_one
                   "Album cover": album_cover
           """
        print("HIGHEST RATED COUNTRY SONG ACCORDING TO BILLBOARD\n")
        # To get to the page that has the highest rated book, we need to navigate to that page
        req = requests.get("https://www.billboard.com/charts/country-songs/")
        soup = BeautifulSoup(req.content, 'html.parser')

        # Artist name
        artist_name = soup.find('p', {'class': 'lrv-u-margin-tb-00'})
        print("Artist: ", artist_name.text)
        # Song title
        song_title = soup.find('a', {'class': 'c-title__link lrv-a-unstyle-link'})
        print("Song title: ", song_title.text.strip())
        # Rating One
        ranking = soup.find('p', {'class': 'a-font-primary-medium-xxs'})
        print("Ranking: ", ranking.text.strip())
        # song_cover
        song_cover = soup.find('img', {'class': 'lrv-u-width-100p'})
        song_cover = song_cover['src']
        print("Song cover: ", song_cover, end="\n\n================="
                                              "================="
                                              "================"
                                              "======================\n")

    def search_song(self, keyword):
        """
           Retrives json data from the SPOTIFY API

           :return: A formatted dicitonary that portraying:
                   "Artist name": artist_name,
                    "Ranking": ranking_one
                   "Song title": song_title,
                   "Album cover": album_cover
           """
        print("SPOTIFY API USED TO RETRIEVE SONG USING A SEARCH KEYWORD\n")

        # https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
        # Request authorization
        """
            To request authorization, The first step is to send a POST request to the /api/token endpoint of the Spotify 
            OAuth 2.0 Service with the following parameters encoded in application/x-www-form-urlencoded:
                | REQUEST BODY PARAMETER  :    VALUE
                    grant_type                 Required => Set it to client_credentials 
                    
            The headers of the request must contain the following parameters:
                | HEADER PARAMETER        :    VALUE
                    Authorization              Required => Base 64 encoded string that contains the client ID and client
                                               secret key.    
            
        """

        client_creds = f"{self.spoti_cid}:{self.spoti_client_secret}"
        client_cred_b64 = base64.b64encode(client_creds.encode()).decode()
        token_url = "https://accounts.spotify.com/api/token"
        token_data = {
            "grant_type": "client_credentials"
        }
        token_headers = {
            "Authorization": f"Basic {client_cred_b64}"
        }

        # send the authorization request using POST method
        req = requests.post(token_url, data=token_data, headers=token_headers)
        token_response_data = req.json()

        access_token = token_response_data['access_token']
        expires_in = token_response_data['expires_in']  # seconds
        token_type = token_response_data['token_type']

        # https://developer.spotify.com/documentation/general/guides/authorization/
        # Authorization
        """
            Authorization refers to the process of granting a user or application access 
            permissions to Spotify data and features. Spotify implements the OAuth 2.0 
            authorization framework:
                - End User corresponds to the Spotify user. The End User grants access to 
                the protected resources (e.g. playlists, personal information, etc.)

                - My App is the client that requests access to the protected resources 
                (e.g. a mobile or web app).

                - Server which hosts the protected resources and provides authentication 
                and authorization via OAuth 2.0.
                
        """
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        endpoint = "https://api.spotify.com/v1/search"

        data = urlencode({
            "q": f"{keyword}",
            "type": "track"
        })

        lookup_url = f"{endpoint}?{data}"

        # Retrieve/ Get/ Fetch data
        searched_song_data = requests.get(lookup_url, headers=headers)
        searched_song_json = searched_song_data.json()

        searched_song_json = searched_song_json["tracks"]["items"]
        song_details = []

        # Extract particular values
        for song in searched_song_json:
            # access all items in the tracks, where each item represents a track
            artist_name = song["artists"][0]["name"]
            song_title = song["name"]
            ranking_one = song["popularity"]
            album_cover = song["album"]["images"][0]["url"]

            spoti_song_info = {
                "Artist name": artist_name,
                "Song title": song_title,
                "Ranking": ranking_one,
                "Album cover": album_cover
            }
            song_details.append(spoti_song_info)

        randNum = random.randint(0, len(song_details))

        artist_name = song_details[randNum]["Artist name"]  # title
        print("Artist: ", artist_name)

        song_title = song_details[randNum]["Song title"]  # title
        print("Song title: ", song_title)

        ranking = song_details[randNum]["Ranking"]  # title
        print("Ranking: ", ranking)

        album_cover = song_details[randNum]["Album cover"]  # title
        print("Cover: ", album_cover, end="\n\n================="
                                          "================="
                                          "================"
                                          "======================\n")


songs = Songs()
songs.get_random_Song()
songs.highest_rated_song()
keyword = input("Search: ")
songs.search_song(keyword)

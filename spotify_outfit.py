import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib
import numpy as np
import cv2
import json
import requests
from sklearn.cluster import KMeans
from datetime import datetime

# Load Spotify Credentials
with open("spotify_keys.json", "r") as keys_file:
    spotify_keys = json.load(keys_file)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=spotify_keys["client_id"],
    client_secret=spotify_keys["client_secret"],
    redirect_uri=spotify_keys["redirect"],
    scope="user-top-read"
))

with open("etsy_api.json", "r") as etsy_file:
    etsy_keys = json.load(etsy_file)

access_token = None
with open("refresh_token.txt") as refresh_code:
    refresh_token = refresh_code.read()

etsy_client_id = etsy_keys["client_id"]
etsy_client_secret = etsy_keys["client_secret"]
etsy_redirect_uri = etsy_keys["redirect"]


def exchange_code_for_token(authorization_code):
    token_url = "https://api.etsy.com/v3/public/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": etsy_redirect_uri,
        "client_id": etsy_client_id,
        "client_secret": etsy_client_secret
    }

    response = requests.post(token_url, data=data)
    print("Token Exchange Response:", response.status_code, response.text)
    if response.status_code == 200:
        token_info = response.json()
        return token_info["access_token"], token_info["refresh_token"]
    else:
        return None, None


def refresh_access_token():
    token_url = "https://api.etsy.com/v3/public/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": etsy_client_id,
        "client_secret": etsy_client_secret,
    }

    response = requests.post(token_url, data=data)
    print("Token Refresh Response:", response.status_code, response.text)
    if response.status_code == 200:
        token_info = response.json()
        return token_info["access_token"]
    else:
        return None



def get_top_songs_colors():
    results = sp.current_user_top_tracks(limit=5)
    songs = []
    for track in results['items']:
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        album_image_url = track['album']['images'][0]['url']
        colors = get_album_colors(album_image_url)
        color_names = [rgb_to_color_name(color) for color in colors]

        # Debugging: Print color names
        print(f"Colors for '{track_name}': {color_names}")

        songs.append({
            "track_name": track_name,
            "artist_name": artist_name,
            "album_image_url": album_image_url,
            "colors": colors,
            "color_names": color_names,
        })
    return songs

def get_album_colors(image_url):
    image = url_to_image(image_url)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    clt = KMeans(n_clusters=3)
    clt.fit(image)
    return [tuple(map(int, color)) for color in clt.cluster_centers_]

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def rgb_to_color_name(rgb):
    if rgb is None:
        return "Unknown"  # Handle missing values
    import colorsys

    r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    if v < 0.14:
        return "Black"
    elif v > 0.9 and s < 0.1:
        return "White"
    elif s < 0.1:
        return "Grey"

    # Convert hue from 0-1 to 0-360 for easier mapping
    hue_360 = h * 360

    if 0 <= hue_360 < 15 or 345 <= hue_360 <= 360:
        return "Red"
    elif 15 <= hue_360 < 45:
        return "Orange"
    elif 45 <= hue_360 < 75:
        return "Yellow"
    elif 75 <= hue_360 < 165:
        return "Green"
    elif 165 <= hue_360 < 195:
        return "Cyan"
    elif 195 <= hue_360 < 255:
        return "Blue"
    elif 255 <= hue_360 < 285:
        return "Purple"
    elif 285 <= hue_360 < 345:
        return "Pink"
    else:
        return "Unknown"


def get_current_season():
    """Determine the current season based on the current month."""
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "fall"


def get_outfit_suggestions(color_names, gender, season, sort_by="score", limit=5):
    """Fetch outfit suggestions from the Etsy API and their associated images."""
    global access_token
    if not access_token:
        access_token = refresh_access_token()  # Refresh the token if not set

    url = "https://openapi.etsy.com/v3/application/listings/active"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-api-key": etsy_client_id,
    }
    # Adjust keywords to prioritize season
    refined_keywords = f"{gender} {season} clothing {' '.join(color_names)}"
    params = {
        "keywords": refined_keywords,
        "limit": limit,
        "sort_on": sort_by,
        "currency": "GBP",  # Request prices in GBP
    }

    print("Request Params:", params)  # Debugging: Check the request parameters

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 401:
        print("Access token expired. Attempting to refresh...")
        access_token = refresh_access_token()
        if not access_token:
            print("Failed to refresh access token.")
            return []

        # Retry the request with the new token
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        results = response.json().get("results", [])
        outfits = []
        for item in results:
            listing_id = item.get("listing_id")
            if listing_id:
                image_url = fetch_image_url(listing_id)  # Fetch the image for the listing
            else:
                image_url = None

            # Correct price format
            raw_price = item.get("price", {}).get("amount", 0)
            converted_price = raw_price / 100  # Assuming Etsy returns price in cents

            outfits.append({
                "title": item.get("title"),
                "price": f"£{converted_price:.2f}",  # Display price in GBP format
                "currency": "GBP",
                "url": item.get("url"),
                "image_url": image_url,
            })
        return outfits
    else:
        print("Error fetching outfits:", response.status_code, response.text)
        return []





def fetch_image_url(listing_id):
    """Fetch the primary image URL for a given listing."""
    url = f"https://openapi.etsy.com/v3/application/listings/{listing_id}/images"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-api-key": etsy_client_id,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        images = response.json().get("results", [])
        if images:
            return images[0].get("url_570xN")  # Fetch the first image's 570px-wide URL
        else:
            print(f"No images found for listing ID: {listing_id}")
            return None
    else:
        print(f"Error fetching images for listing ID {listing_id}: {response.status_code}, {response.text}")
        return None

    

def prepare_outfits_data(outfits, color_names):
    """
    Prepare the details of outfits for rendering in a web template.
    """
    prepared_outfits = []
    if not outfits:
        print(f"No outfits found for color scheme: {', '.join(color_names).capitalize()}.")
        return prepared_outfits

    # Only add unique outfits to avoid duplicates
    seen = set()
    for item in outfits:
        if item.get("url") not in seen:  # Check if outfit URL is already added
            print(f"Adding outfit: {item.get('title')}") 
            seen.add(item.get("url"))
            prepared_outfits.append({
                "title": item.get("title", "No Title"),
                "price": item.get("price", "N/A"),
                "currency": item.get("currency", "USD"),
                "link": item.get("url", "No URL"),
                "image_url": item.get("image_url", None)
            })
    return prepared_outfits










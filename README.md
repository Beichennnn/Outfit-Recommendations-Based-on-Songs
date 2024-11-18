# 🎵 Music-Inspired Fashion Website 🎨

A dynamic and interactive website that combines your favorite Spotify songs with outfit recommendations from Etsy based on album colors, gender, season, and user-selected sorting options. This project integrates the **Spotify API** and **Etsy API**, along with modern web design for a sleek and user-friendly experience.

------

## 🌟 Features

- Fetch **Spotify top songs** and their album colors.
- **Generate outfit recommendations** based on the album’s dominant colors.
- Customize by **gender**, **season**, and **sort criteria** (e.g., newest, price, etc.).
- Real-time fetching of outfits when clicking on individual songs.
- Modern and responsive design using **CSS** with harmonious color schemes.

------

## 🛠️ Tech Stack

### Backend:

- **Flask**: Python web framework.
- **Spotify API**: For fetching user’s top tracks and album covers.
- **Etsy API**: For retrieving outfits matching the album colors.

### Frontend:

- **HTML**: Web structure.
- **CSS**: Styling with a curated color palette.
- **JavaScript**: Dynamic fetching of outfits.
- **Jinja2**: Template rendering.

------

## 🚀 Setup Guide

### Prerequisites

- Python 3.x installed.
- Spotify Developer account and an **App Key**.
- Etsy Developer account and an **API Key**.
- Virtual Environment (optional but recommended).

###  Configure API Keys

1. **Spotify API**:

   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).

   - Create an app and copy the `client_id`, `client_secret`, and `redirect_uri`.

   - Save them in a file named 

     ```
     spotify_keys.json
     ```

      in the root directory:

     ```
     {
         "client_id": "your_client_id",
         "client_secret": "your_client_secret",
         "redirect": "your_redirect_uri"
     }
     ```

2. **Etsy API**:

   - Go to [Etsy Developer Dashboard](https://developer.etsy.com/).

   - Create an app and get the `client_id` and `client_secret`.

   - Save them in 

     ```
     etsy_api.json
     ```

     :

     ```
     {
         "client_id": "your_client_id",
         "client_secret": "your_client_secret",
         "redirect": "your_redirect_uri"
     }
     ```

   - Follow [Etsy OAuth steps]([Listings Tutorial | Etsy Open API v3](https://developer.etsy.com/documentation/tutorials/listings/)) to obtain your **Refresh Token**.



------

## 🧱 Step-by-Step Walkthrough

### 1️⃣ **Homepage (`index.html`)**

- **H1 Header**: “🎵 Outfit Recommendations 🎨” aligned at the center.
- Dropdown options for **Gender**, **Season**, and **Sort By** criteria.
- A button to “Fetch My Top Songs”.

### 2️⃣ **Fetching Spotify Data**

- Use `spotipy` to fetch **top tracks** from the user’s Spotify account.
- Extract album artwork and dominant colors using the `KMeans` clustering algorithm.
- Display the top 5 songs along with their album colors.

### 3️⃣ **Dynamic Outfit Recommendations**

- On the results page 

  ```
  results.html
  ```

  :

  - Display the album cover, song details, and a “View Outfits” button for each song.
  - When clicked, send a request to fetch outfits based on the album’s colors.
  - Outfits are displayed in a grid, showing images, titles, and prices.

### 4️⃣ **Real-Time Interactions**

- Use JavaScript to fetch and display outfits without reloading the page.
- Enable sorting by **price**, **created**, **updated**, or **score**.

### 5️⃣ **Styling with CSS**

- Applied a curated color scheme:
  - Background: Dark tones (#585248).
  - Text: Soft light shades (#FFFBC7).
  - Buttons and accents: Subtle contrast for interactivity.
- Responsive layout using `flexbox`.

------

## 📂 File Structure

```
phpCopy code├── static/
│   ├── css/
│   │   └── styles.css        # Styling for the website
├── templates/
│   ├── index.html            # Homepage with form
│   ├── results.html          # Results page
├── spotify_outfit.py         # Backend logic for API integrations
├── app.py                    # Flask app routing
├── spotify_keys.json         # Spotify API credentials
├── etsy_api.json             # Etsy API credentials
├── requirements.txt          # Python dependencies
```

------

## 🧩 Future Improvements

1. Style and SongsMatching:

   -  Future improvements could analyze audio features from Spotify (like energy, tempo, and mood) and combine them with colors for more contextually relevant fashion recommendations.

2. Enhanced Filters:

   - Add more filters like material, category, or color combinations. 

3. User Authentication:

   - Allow users to save their favorite outfits.

4. Improved Design:

   - Add animations and transitions for a smoother user experience.

------

Feel free to contribute or suggest improvements! 🌟
# 🎵 Music-Inspired Fashion Website 🎨

A dynamic and interactive website that combines your favorite Spotify songs with outfit recommendations from Etsy based on album colors, gender, season, and user-selected sorting options. This project integrates the **Spotify API** and **Etsy API**, along with modern web design for a sleek and user-friendly experience.

------

## 🌟 Features

- Fetch **Spotify top songs** and their album colors.

- **Generate outfit recommendations** based on the album’s dominant colors.

- Customize by **gender**, **season**, and **sort criteria** (e.g., newest, price, etc.).

- Real-time fetching of outfits when clicking on individual songs.

- Modern and responsive design using **CSS** with harmonious color schemes.

  index.html:

  ![index.html](https://media.discordapp.net/attachments/1138186732093833329/1308386956794920960/image.png?ex=673dc1cf&is=673c704f&hm=4cdbf7bec34c3cc95fdc70b4d1fb5dfe98f089fc28a1bdd1608efef4910f2f62&=&format=webp&quality=lossless&width=1395&height=771)

  results.html:

  ![results.html](https://media.discordapp.net/attachments/1138186732093833329/1308387627795218493/image.png?ex=673dc26f&is=673c70ef&hm=992985badfe87cf15d13d2ff24fd0ab837bb002cb9e942813ef53530ddadd0aa&=&format=webp&quality=lossless&width=1342&height=771)

  ![results.html](https://media.discordapp.net/attachments/1138186732093833329/1308388139210899526/image.png?ex=673dc2e9&is=673c7169&hm=ea81c5c4a2ba63499c1aca42de636cbc1f72bdf99640f320ea957f93708bdbde&=&format=webp&quality=lossless&width=1342&height=771)

  

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

   - Put your Website URL (In my case is http://localhost)
   
   - Put your Callback URLs (In my case is http://localhost:8000/callback)
   
   - **Build the Authorization URL:** Use your client ID and other required parameters to build an authorization URL. This URL directs users to log in to their Etsy account and authorize your app. You would have specified scopes that determine the level of access your application requires, and a `redirect_uri` that Etsy will send users back to after authorization.
   
   - **User Authorization:** You open this URL in a web browser. The user logs in if necessary, and approves the requested permissions. Etsy then redirects the user back to your `redirect_uri` with an authorization code included in the query string.
   
   - **Exchange Authorization Code for Tokens:** You then take this authorization code and make a server-to-server request to Etsy's token endpoint to exchange the authorization code for an access token and a refresh token. The request includes your client ID, client secret, and the authorization code.
   
   - **Store the Refresh Token:** Once you receive the access token and the refresh token, you should securely store the refresh token. In my case I saved in:
   
   - ```
     refresh_token.txt
     ```
   
     It can be used to obtain new access tokens without user interaction once the current access token expires.
   
   - Follow [Etsy OAuth steps]([Listings Tutorial | Etsy Open API v3](https://developer.etsy.com/documentation/essentials/authentication#redirect-uris)) as reference.



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
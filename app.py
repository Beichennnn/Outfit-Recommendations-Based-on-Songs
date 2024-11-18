from flask import Flask, render_template, request, jsonify
from spotify_outfit import get_top_songs_colors, get_outfit_suggestions, prepare_outfits_data

app = Flask(__name__)

songs = []

@app.route("/", methods=["GET", "POST"])
def home():
    global songs
    if request.method == "POST":
        gender = request.form.get("gender", "women")
        season = request.form.get("season", "fall")
        sort_by = request.form.get("sort_by", "score")
        songs = get_top_songs_colors()  
        # Pass gender, season, and sort_by to the template
        return render_template("results.html", songs=songs, gender=gender, season=season, sort_by=sort_by)
    return render_template("index.html")


@app.route("/fetch_outfits", methods=["POST"])
def fetch_outfits():
    data = request.get_json()
    song_index = data.get("song_index")
    gender = data.get("gender", "women")
    season = data.get("season", "fall")
    sort_by = data.get("sort_by", "score")

    try:
        song = songs[song_index]  
        color_names = song["color_names"]

        outfits = get_outfit_suggestions(color_names, gender, season, sort_by=sort_by)

        response_data = {
            "success": True,
            "outfits": prepare_outfits_data(outfits, color_names),
        }
    except Exception as e:
        print(f"Error in /fetch_outfits: {e}")
        response_data = {"success": False, "error": str(e)}

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)

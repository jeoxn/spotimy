from flask import Blueprint, render_template, redirect, request, url_for, flash
from . import db
from .models import Playlist, Song
from .mp3download import download_youtube_audio

urls = Blueprint("urls", __name__)


@urls.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("playlist-name")
        if len(name) < 1:
            flash("Playlist name is too short!", category="error")
        else:
            new_playlist = Playlist(name=name)
            db.session.add(new_playlist)
            db.session.commit()
            flash(f"Playlist {name} has been created!", category="success")
            return render_template("home.html", playlists=Playlist.query.all())
    return render_template("home.html", playlists=Playlist.query.all())

@urls.route("/library/<int:id>", methods=["GET", "POST"])
def library(id):
    if request.method == "POST":
        url = request.form.get("url")
        if len(url) < 1:
            flash("URL is too short!", category="error")
        else:
            title = download_youtube_audio(url)
            print(title)
            new_song = Song(title=title, url=url, playlist_id=id)
            db.session.add(new_song)
            db.session.commit()
            flash(f"Song {title} has been added to the playlist!", category="success")
        
    playlist_songs = Playlist.query.get(id).songs
    list = []
    name = []

    for song in playlist_songs:
        name.append(song.title)
        title = song.title
        # replace spaces with underscores
        title = title.replace(" ", "%20")
        title = "/static/audio/" + title + ".mp4"
        list.append(title)

    return render_template("library.html", playlist=Playlist.query.get(id), list=list, name=name)


@urls.route("/delete/<int:playlist>/<int:song>", methods=["POST"])
def delete(playlist, song):
    # DELETE FROM SONG WHERE id = song AND playlist_id = playlist
    Song.query.filter_by(id=song, playlist_id=playlist).delete()
    db.session.commit()
    flash("Song has been deleted!", category="success")
    return redirect(url_for("urls.library", id=playlist))

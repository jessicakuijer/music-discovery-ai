from typing import Dict, List, Optional

import spotipy
import streamlit as st

from ui.i18n import t


def initialize_spotify(
    client_id: str, client_secret: str, *, silent: bool = False
) -> Optional[spotipy.Spotify]:
    """Initialise le client Spotify. Si silent=True, pas de message d'erreur (init automatique)."""
    try:
        from spotipy.oauth2 import SpotifyClientCredentials

        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        spotify.search(q="test", type="artist", limit=1)
        return spotify
    except Exception as e:
        if not silent:
            st.error(t("errors.spotify_connection", error=str(e)))
        return None


def format_followers(count: int) -> str:
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M".replace(".0M", "M")
    if count >= 1_000:
        return f"{count / 1_000:.0f}K"
    return str(count)


def search_artist_suggestions(
    spotify: spotipy.Spotify, query: str, limit: int = 5
) -> List[Dict]:
    """Recherche des suggestions d'artistes pour l'autocomplete."""
    if not query or len(query.strip()) < 2:
        return []

    try:
        results = spotify.search(q=query.strip(), type="artist", limit=limit)
        suggestions = []
        for artist in results.get("artists", {}).get("items", []):
            genres = artist.get("genres", [])
            genre_label = genres[0] if genres else t("spotify.genre_fallback")
            followers = format_followers(artist["followers"]["total"])
            suggestions.append(
                {
                    "name": artist["name"],
                    "initial": artist["name"][0].upper() if artist["name"] else "?",
                    "meta": t("spotify.meta", followers=followers, genre=genre_label),
                    "popularity": artist.get("popularity", 0),
                    "hot": artist.get("popularity", 0) >= 70,
                }
            )
        return suggestions
    except Exception:
        return []


def get_artist_data(spotify: spotipy.Spotify, artist_name: str) -> Optional[Dict]:
    """Récupère les données d'un artiste depuis Spotify."""
    try:
        results = spotify.search(q=artist_name, type="artist", limit=1)
        if not results["artists"]["items"]:
            return None

        artist = results["artists"]["items"][0]
        artist_id = artist["id"]

        artist_info = spotify.artist(artist_id)
        top_tracks = spotify.artist_top_tracks(artist_id, country="FR")
        albums = spotify.artist_albums(artist_id, album_type="album", limit=5)

        try:
            related_artists = spotify.artist_related_artists(artist_id)
            related = related_artists["artists"][:10]
        except Exception:
            related = []
            st.info(t("errors.spotify_related_info"))

        return {
            "info": artist_info,
            "top_tracks": top_tracks["tracks"],
            "albums": albums["items"],
            "related_artists": related,
            "genres": artist_info["genres"],
            "popularity": artist_info["popularity"],
            "followers": artist_info["followers"]["total"],
        }
    except Exception as e:
        st.error(t("errors.spotify_fetch", error=str(e)))
        return None

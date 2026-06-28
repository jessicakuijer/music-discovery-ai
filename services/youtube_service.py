from typing import Optional

import requests
import streamlit as st

from ui.i18n import t


def search_youtube_videos(
    artist_name: str, track_name: str, youtube_api_key: str
) -> Optional[str]:
    """Recherche une vidéo YouTube pour un artiste et une chanson."""
    try:
        if not youtube_api_key:
            return None

        search_queries = [
            f'"{artist_name}" "{track_name}" official',
            f"{artist_name} {track_name} official",
            f"{artist_name} {track_name}",
            f'"{artist_name}" official',
            artist_name,
        ]

        youtube_search_url = "https://www.googleapis.com/youtube/v3/search"

        for query in search_queries:
            try:
                params = {
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "maxResults": 3,
                    "key": youtube_api_key,
                    "order": "relevance",
                    "videoDuration": "any",
                    "videoEmbeddable": "true",
                }

                response = requests.get(youtube_search_url, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    if data.get("items"):
                        video_id = data["items"][0]["id"]["videoId"]
                        return f"https://www.youtube.com/watch?v={video_id}"
                elif response.status_code == 403:
                    st.warning(t("errors.youtube_quota"))
                    return None

            except Exception:
                continue

        return None
    except Exception:
        return None


def get_youtube_embed_url(youtube_url: str) -> str:
    """Convertit une URL YouTube en URL d'embed."""
    if not youtube_url:
        return ""

    video_id = None
    if "watch?v=" in youtube_url:
        video_id = youtube_url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_url:
        video_id = youtube_url.split("youtu.be/")[1].split("?")[0]

    if video_id:
        return f"https://www.youtube.com/embed/{video_id}"
    return ""

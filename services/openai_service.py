import json
from typing import Dict, List, Optional

import openai
import spotipy
import streamlit as st

from services.youtube_service import search_youtube_videos
from ui.i18n import get_locale, normalize_similarity_type, t

SIMILARITY_TYPE_ENUM = "same_genre|historical_influence|creative_approach|surprise_discovery"


def create_analysis_prompt(artist_data: Dict, locale: Optional[str] = None) -> str:
    """Crée le prompt pour l'analyse IA dans la langue active."""
    active_locale = locale or get_locale()
    artist_info = artist_data["info"]
    unspecified = t("results.unspecified")
    genres = ", ".join(artist_data["genres"]) if artist_data["genres"] else unspecified
    top_tracks = [track["name"] for track in artist_data["top_tracks"][:5]]
    related_artists = [artist["name"] for artist in artist_data["related_artists"][:5]]

    if active_locale == "en":
        return f"""You are a music discovery expert. Analyze this artist and recommend 8 similar but lesser-known artists.

ARTIST TO ANALYZE:
- Name: {artist_info['name']}
- Genres: {genres}
- Popularity: {artist_data['popularity']}/100
- Followers: {artist_data['followers']:,}
- Top tracks: {', '.join(top_tracks)}
- Spotify related artists: {', '.join(related_artists)}

MISSION:
Recommend 8 similar artists using this logic:
- 3 artists in the same genre but less mainstream
- 2 artists from a different era with similar influences
- 2 artists with a similar creative approach
- 1 surprising but coherent discovery

RESPONSE FORMAT (JSON):
{{
  "analysis": "Style analysis in 2-3 sentences in English",
  "recommendations": [
    {{
      "name": "Artist name",
      "reason": "Why this recommendation (1 sentence in English)",
      "similarity_type": "{SIMILARITY_TYPE_ENUM}",
      "confidence": 85
    }}
  ]
}}

IMPORTANT:
- Choose artists that truly exist on Spotify and avoid the most famous ones.
- Write analysis and reason in English.
- Use only the exact similarity_type values listed above."""

    return f"""Tu es un expert en découverte musicale. Analyse cet artiste et recommande 8 artistes similaires mais moins connus.

ARTISTE À ANALYSER:
- Nom: {artist_info['name']}
- Genres: {genres}
- Popularité: {artist_data['popularity']}/100
- Followers: {artist_data['followers']:,}
- Top tracks: {', '.join(top_tracks)}
- Artistes reliés Spotify: {', '.join(related_artists)}

MISSION:
Recommande 8 artistes similaires avec cette logique:
- 3 artistes dans le même genre mais moins mainstream
- 2 artistes d'une époque différente avec des influences similaires
- 2 artistes avec une approche créative proche
- 1 artiste surprenant mais cohérent

FORMAT DE RÉPONSE (JSON):
{{
  "analysis": "Analyse du style de l'artiste en 2-3 phrases en français",
  "recommendations": [
    {{
      "name": "Nom de l'artiste",
      "reason": "Pourquoi cette recommandation (1 phrase en français)",
      "similarity_type": "{SIMILARITY_TYPE_ENUM}",
      "confidence": 85
    }}
  ]
}}

IMPORTANT:
- Choisis des artistes qui existent vraiment sur Spotify et évite les plus connus.
- Rédige analysis et reason en français.
- Utilise uniquement les valeurs similarity_type listées ci-dessus."""


def call_openai_for_recommendations(prompt: str, api_key: str) -> Optional[Dict]:
    """Appelle OpenAI pour les recommandations."""
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7,
        )

        response_text = response.choices[0].message.content
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        return json.loads(response_text.strip())
    except Exception as e:
        st.error(t("errors.ai", error=str(e)))
        return None


def verify_and_enrich_recommendations(
    spotify: spotipy.Spotify,
    recommendations: List[Dict],
    youtube_api_key: str = "",
) -> List[Dict]:
    """Vérifie que les artistes existent sur Spotify et enrichit les données."""
    enriched_recs = []

    for rec in recommendations:
        try:
            results = spotify.search(q=rec["name"], type="artist", limit=1)
            if results["artists"]["items"]:
                artist = results["artists"]["items"][0]
                top_tracks = spotify.artist_top_tracks(artist["id"], country="FR")

                youtube_url = None
                if youtube_api_key and top_tracks["tracks"]:
                    top_track = top_tracks["tracks"][0]
                    youtube_url = search_youtube_videos(
                        artist["name"],
                        top_track["name"],
                        youtube_api_key,
                    )

                enriched_rec = {
                    "name": artist["name"],
                    "reason": rec["reason"],
                    "similarity_type": normalize_similarity_type(rec.get("similarity_type")),
                    "confidence": rec["confidence"],
                    "spotify_data": {
                        "id": artist["id"],
                        "image": artist["images"][0]["url"] if artist["images"] else None,
                        "genres": artist["genres"],
                        "popularity": artist["popularity"],
                        "followers": artist["followers"]["total"],
                        "top_tracks": top_tracks["tracks"][:3],
                        "external_urls": artist["external_urls"],
                        "youtube_url": youtube_url,
                    },
                }
                enriched_recs.append(enriched_rec)

        except Exception:
            st.warning(t("errors.artist_not_found", name=rec.get("name", "")))
            continue

    return enriched_recs

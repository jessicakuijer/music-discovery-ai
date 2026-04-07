import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import openai
import requests
import json
from typing import List, Dict, Optional
import time
import base64
import re

# Configuration de la page
st.set_page_config(
    page_title="🎵 Music Discovery AI",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1db954 0%, #191414 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .artist-card {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #1db954;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .recommendation-card {
        background: linear-gradient(135deg, #1db954 0%, #1ed760 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3);
    }
    
    .track-card {
        background: #f0f0f0;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #1db954;
    }
    
    .analysis-card {
        background: #e8f5e8;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1db954 0%, #1ed760 100%);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .spotify-embed {
        border-radius: 12px;
        overflow: hidden;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("""
<div class="main-header">
    <h1>🎵 Music Discovery AI</h1>
    <h3>Découvrez de nouveaux artistes grâce à l'intelligence artificielle</h3>
    <p>Entrez un artiste que vous aimez, et l'IA vous suggère des découvertes musicales personnalisées !</p>
</div>
""", unsafe_allow_html=True)

# Initialisation du session state
if 'recommendations_ready' not in st.session_state:
    st.session_state.recommendations_ready = False
if 'current_artist_data' not in st.session_state:
    st.session_state.current_artist_data = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
if 'spotify_client' not in st.session_state:
    st.session_state.spotify_client = None

def initialize_spotify(client_id: str, client_secret: str) -> Optional[spotipy.Spotify]:
    """Initialise le client Spotify"""
    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        # Test de connexion
        spotify.search(q="test", type="artist", limit=1)
        return spotify
    except Exception as e:
        st.error(f"Erreur de connexion Spotify : {str(e)}")
        return None

def search_youtube_videos(artist_name: str, track_name: str, youtube_api_key: str) -> Optional[str]:
    """Recherche une vidéo YouTube pour un artiste et une chanson"""
    try:
        if not youtube_api_key:
            return None
            
        # Stratégie de recherche multiple - commence par la plus spécifique
        search_queries = [
            f'"{artist_name}" "{track_name}" official',  # Plus spécifique
            f"{artist_name} {track_name} official",      # Moins de guillemets
            f"{artist_name} {track_name}",               # Sans "official"
            f'"{artist_name}" official',                 # Juste l'artiste
            artist_name                                  # Nom d'artiste seul
        ]
        
        youtube_search_url = "https://www.googleapis.com/youtube/v3/search"
        
        for query in search_queries:
            try:
                params = {
                    'part': 'snippet',
                    'q': query,
                    'type': 'video',
                    'maxResults': 3,  # Plus de résultats pour choisir
                    'key': youtube_api_key,
                    'order': 'relevance',
                    'videoDuration': 'any',
                    'videoEmbeddable': 'true'  # Assure que la vidéo est embeddable
                }
                
                response = requests.get(youtube_search_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('items'):
                        # Prend la première vidéo trouvée
                        video_id = data['items'][0]['id']['videoId']
                        return f"https://www.youtube.com/watch?v={video_id}"
                elif response.status_code == 403:
                    # Quota dépassé ou clé invalide
                    st.warning("⚠️ Quota YouTube API dépassé ou clé invalide")
                    return None
                    
            except Exception as e:
                # Continue avec la prochaine requête
                continue
        
        return None
    except Exception as e:
        # Échec silencieux pour ne pas casser l'app
        return None

def get_youtube_embed_url(youtube_url: str) -> str:
    """Convertit une URL YouTube en URL d'embed"""
    if not youtube_url:
        return ""
    
    # Extrait l'ID de la vidéo
    video_id = None
    if "watch?v=" in youtube_url:
        video_id = youtube_url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_url:
        video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
    
    if video_id:
        return f"https://www.youtube.com/embed/{video_id}"
    return ""

def display_youtube_video(youtube_url: str, title: str = ""):
    """Affiche une vidéo YouTube intégrée dans Streamlit"""
    if youtube_url:
        embed_url = get_youtube_embed_url(youtube_url)
        if embed_url:
            st.markdown(f"""
            <div class="spotify-embed">
                <iframe width="100%" height="200" src="{embed_url}" 
                frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen></iframe>
            </div>
            """, unsafe_allow_html=True)

def get_artist_data(spotify: spotipy.Spotify, artist_name: str) -> Optional[Dict]:
    """Récupère les données d'un artiste depuis Spotify"""
    try:
        # Recherche de l'artiste
        results = spotify.search(q=artist_name, type='artist', limit=1)
        if not results['artists']['items']:
            return None
        
        artist = results['artists']['items'][0]
        artist_id = artist['id']
        
        # Récupération des données détaillées
        artist_info = spotify.artist(artist_id)
        top_tracks = spotify.artist_top_tracks(artist_id, country='FR')
        albums = spotify.artist_albums(artist_id, album_type='album', limit=5)
        
        # Related artists avec fallback (parfois indisponible selon l'artiste)
        try:
            related_artists = spotify.artist_related_artists(artist_id)
            related = related_artists['artists'][:10]
        except Exception:
            # Certains artistes n'ont pas de related_artists disponibles
            related = []
            st.info("ℹ️ Artistes similaires indisponibles pour cet artiste, mais l'IA va quand même faire ses recommandations !")
        
        return {
            'info': artist_info,
            'top_tracks': top_tracks['tracks'],
            'albums': albums['items'],
            'related_artists': related,
            'genres': artist_info['genres'],
            'popularity': artist_info['popularity'],
            'followers': artist_info['followers']['total']
        }
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {str(e)}")
        return None

def create_analysis_prompt(artist_data: Dict) -> str:
    """Crée le prompt pour l'analyse IA"""
    artist_info = artist_data['info']
    genres = ", ".join(artist_data['genres']) if artist_data['genres'] else "Non spécifié"
    top_tracks = [track['name'] for track in artist_data['top_tracks'][:5]]
    related_artists = [artist['name'] for artist in artist_data['related_artists'][:5]]
    
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
  "analysis": "Analyse du style de l'artiste en 2-3 phrases",
  "recommendations": [
    {{
      "name": "Nom de l'artiste",
      "reason": "Pourquoi cette recommandation (1 phrase)",
      "similarity_type": "même genre|influence historique|approche créative|découverte surprenante",
      "confidence": 85
    }}
  ]
}}

IMPORTANT: Choisis des artistes qui existent vraiment sur Spotify et évite les plus connus."""

def call_openai_for_recommendations(prompt: str, api_key: str) -> Optional[Dict]:
    """Appelle OpenAI pour les recommandations"""
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )
        
        # Parse la réponse JSON
        response_text = response.choices[0].message.content
        # Nettoie la réponse si elle contient des backticks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        return json.loads(response_text.strip())
    except Exception as e:
        st.error(f"Erreur IA : {str(e)}")
        return None

def verify_and_enrich_recommendations(spotify: spotipy.Spotify, recommendations: List[Dict], youtube_api_key: str = "") -> List[Dict]:
    """Vérifie que les artistes existent sur Spotify et enrichit les données"""
    enriched_recs = []
    
    for rec in recommendations:
        try:
            # Recherche l'artiste sur Spotify
            results = spotify.search(q=rec['name'], type='artist', limit=1)
            if results['artists']['items']:
                artist = results['artists']['items'][0]
                
                # Récupère les top tracks
                top_tracks = spotify.artist_top_tracks(artist['id'], country='FR')
                
                # Recherche YouTube pour le top track (si API disponible)
                youtube_url = None
                if youtube_api_key and top_tracks['tracks']:
                    top_track = top_tracks['tracks'][0]
                    youtube_url = search_youtube_videos(
                        artist['name'], 
                        top_track['name'], 
                        youtube_api_key
                    )
                
                enriched_rec = {
                    'name': artist['name'],
                    'reason': rec['reason'],
                    'similarity_type': rec['similarity_type'],
                    'confidence': rec['confidence'],
                    'spotify_data': {
                        'id': artist['id'],
                        'image': artist['images'][0]['url'] if artist['images'] else None,
                        'genres': artist['genres'],
                        'popularity': artist['popularity'],
                        'followers': artist['followers']['total'],
                        'top_tracks': top_tracks['tracks'][:3],
                        'external_urls': artist['external_urls'],
                        'youtube_url': youtube_url  # Ajout de l'URL YouTube
                    }
                }
                enriched_recs.append(enriched_rec)
                
        except Exception as e:
            st.warning(f"Artiste '{rec['name']}' non trouvé sur Spotify")
            continue
    
    return enriched_recs

# Sidebar pour la configuration
with st.sidebar:
    st.header("🔧 Configuration")
    
    # Tentative de chargement des secrets Streamlit
    default_openai = ""
    default_spotify_id = ""
    default_spotify_secret = ""
    default_youtube_key = ""
    secrets_loaded = False
    
    try:
        _sec = st.secrets
        default_openai = str(_sec.get("OPENAI_API_KEY", "") or "").strip()
        default_spotify_id = str(_sec.get("SPOTIFY_CLIENT_ID", "") or "").strip()
        default_spotify_secret = str(_sec.get("SPOTIFY_CLIENT_SECRET", "") or "").strip()
        default_youtube_key = str(_sec.get("YOUTUBE_API_KEY", "") or "").strip()
        secrets_loaded = bool(
            default_openai or default_spotify_id or default_spotify_secret or default_youtube_key
        )
        if secrets_loaded:
            st.success("🔒 Clés par défaut chargées depuis secrets.toml")
            st.info("💡 Vous pouvez remplacer ces valeurs par vos propres clés ci-dessous")
        else:
            st.warning(
                "⚠️ secrets.toml présent mais aucune clé renseignée — "
                "complétez le fichier ou saisissez vos clés ci-dessous"
            )
    except Exception:
        st.warning(
            "⚠️ Aucun secrets.toml — copiez .streamlit/secrets.toml.example "
            "vers .streamlit/secrets.toml ou entrez vos clés ci-dessous"
        )
    
    # Clés API avec valeurs par défaut
    st.subheader("🔑 Clés API")
    
    openai_api_key = st.text_input(
        "Clé API OpenAI",
        value=default_openai,
        type="password",
        placeholder="sk-... (optionnel si clés par défaut)",
        help="Laissez vide pour utiliser les clés par défaut" if secrets_loaded else "Pour l'analyse IA des artistes"
    )
    
    spotify_client_id = st.text_input(
        "Spotify Client ID",
        value=default_spotify_id,
        placeholder="Optionnel si clés par défaut" if secrets_loaded else "Votre Client ID Spotify",
        help="Depuis votre compte Spotify Developer"
    )
    
    spotify_client_secret = st.text_input(
        "Spotify Client Secret",
        value=default_spotify_secret,
        type="password",
        placeholder="Optionnel si clés par défaut" if secrets_loaded else "Votre Client Secret",
        help="Depuis votre compte Spotify Developer"
    )
    
    youtube_api_key = st.text_input(
        "YouTube API Key (optionnel)",
        value=default_youtube_key,
        type="password",
        placeholder="Pour intégrer les vidéos YouTube",
        help="API YouTube Data v3 - Optionnel mais recommandé pour une expérience complète"
    )
    
    # Test de connexion Spotify
    if spotify_client_id and spotify_client_secret:
        if st.button("🔗 Tester la connexion Spotify"):
            with st.spinner("Test de connexion..."):
                spotify_client = initialize_spotify(spotify_client_id, spotify_client_secret)
                if spotify_client:
                    st.session_state.spotify_client = spotify_client
                    st.success("✅ Connexion Spotify OK !")
                else:
                    st.error("❌ Erreur de connexion Spotify")
    
    # Instructions
    st.markdown("---")
    st.subheader("📋 Instructions")
    st.markdown("""
    1. **Ajoutez vos clés API** ci-dessus
    2. **Testez la connexion** Spotify
    3. **Entrez un artiste** que vous aimez
    4. **Découvrez** de nouveaux artistes !
    
    💡 **Astuce :** Plus l'artiste est connu, meilleures seront les recommandations !
    
    🎥 **YouTube :** Ajoutez votre clé YouTube API pour voir les vidéos des artistes recommandés !
    """)

# Zone pour les comptes nécessaires
    st.markdown("""
    <div class="analysis-card">
        <h3>🔑 Comptes requis</h3>
        <p><strong>OpenAI API :</strong> <a href="https://platform.openai.com" target="_blank">platform.openai.com</a></p>
        <p><strong>Spotify Developer :</strong> <a href="https://developer.spotify.com/dashboard" target="_blank">developer.spotify.com/dashboard</a></p>
        <p><strong>YouTube Data API :</strong> <a href="https://console.cloud.google.com" target="_blank">console.cloud.google.com</a> (optionnel)</p>
        <p><em>Vos clés restent privées et ne sont utilisées que pour les APIs officielles</em></p>
    </div>
    """, unsafe_allow_html=True)

# Zone principale
if not st.session_state.spotify_client or not openai_api_key:
    # Instructions d'accueil
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="artist-card">
            <h3>🎯 Comment ça marche ?</h3>
            <ol>
                <li><strong>Configurez vos API</strong> dans la barre latérale</li>
                <li><strong>Entrez un artiste</strong> que vous adorez</li>
                <li><strong>L'IA analyse</strong> son style musical</li>
                <li><strong>Découvrez 8 nouveaux artistes</strong> similaires</li>
                <li><strong>Écoutez directement</strong> sur Spotify</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="artist-card">
            <h3>🎵 Fonctionnalités</h3>
            <ul>
                <li>🤖 <strong>IA personnalisée</strong> pour chaque style</li>
                <li>🎧 <strong>Découvertes intelligentes</strong> pas juste "populaire"</li>
                <li>📊 <strong>Analyse des genres</strong> et influences</li>
                <li>🎼 <strong>Top tracks</strong> de chaque recommandation</li>
                <li>🔗 <strong>Liens Spotify</strong> directs</li>
                <li>🎥 <strong>Vidéos YouTube</strong> intégrées (optionnel)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    # Zone pour les comptes nécessaires
    st.markdown("""
    <div class="analysis-card">
        <h3>🔑 Comptes requis</h3>
        <p><strong>OpenAI API :</strong> <a href="https://platform.openai.com" target="_blank">platform.openai.com</a></p>
        <p><strong>Spotify Developer :</strong> <a href="https://developer.spotify.com/dashboard" target="_blank">developer.spotify.com/dashboard</a></p>
        <p><strong>YouTube Data API :</strong> <a href="https://console.cloud.google.com" target="_blank">console.cloud.google.com</a> (optionnel)</p>
        <p><em>Vos clés restent privées et ne sont utilisées que pour les APIs officielles</em></p>
    </div>
    """, unsafe_allow_html=True)

else:
    # Interface de découverte
    st.markdown("## 🔍 Découverte Musicale")
    
    # Input artiste
    col1, col2 = st.columns([3, 1])
    with col1:
        artist_input = st.text_input(
            "Quel artiste aimez-vous ?",
            placeholder="Ex: Radiohead, Billie Eilish, Miles Davis...",
            key="artist_search"
        )
    
    with col2:
        search_button = st.button("🚀 Découvrir !", key="discover_btn")
    
    # Traitement de la recherche
    if search_button and artist_input:
        if not openai_api_key:
            st.error("Clé API OpenAI manquante")
        else:
            with st.spinner(f"🔍 Analyse de {artist_input} en cours..."):
                # Récupération des données Spotify
                artist_data = get_artist_data(st.session_state.spotify_client, artist_input)
                
                if not artist_data:
                    st.error(f"Artiste '{artist_input}' non trouvé sur Spotify")
                else:
                    st.session_state.current_artist_data = artist_data
                    
                    # Analyse IA
                    with st.spinner("🤖 L'IA analyse le style musical..."):
                        analysis_prompt = create_analysis_prompt(artist_data)
                        ia_response = call_openai_for_recommendations(analysis_prompt, openai_api_key)
                        
                        if ia_response:
                            # Vérification et enrichissement des recommandations
                            with st.spinner("🎵 Vérification des artistes sur Spotify..."):
                                enriched_recs = verify_and_enrich_recommendations(
                                    st.session_state.spotify_client, 
                                    ia_response['recommendations'],
                                    youtube_api_key  # Ajout de la clé YouTube
                                )
                                
                                st.session_state.recommendations = {
                                    'analysis': ia_response['analysis'],
                                    'artists': enriched_recs
                                }
                                st.session_state.recommendations_ready = True
                                st.success(f"✅ {len(enriched_recs)} recommandations trouvées !")
    
    # Affichage des résultats
    if st.session_state.recommendations_ready and st.session_state.current_artist_data:
        artist_info = st.session_state.current_artist_data['info']
        recommendations = st.session_state.recommendations
        
        # Affichage de l'artiste analysé
        st.markdown("### 🎤 Artiste Analysé")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if artist_info['images']:
                st.image(artist_info['images'][0]['url'], width=200)
        
        with col2:
            st.markdown(f"""
            <div class="artist-card">
                <h3>{artist_info['name']}</h3>
                <p><strong>Genres :</strong> {', '.join(st.session_state.current_artist_data['genres']) or 'Non spécifié'}</p>
                <p><strong>Popularité :</strong> {st.session_state.current_artist_data['popularity']}/100</p>
                <p><strong>Followers :</strong> {st.session_state.current_artist_data['followers']:,}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Analyse IA
        st.markdown(f"""
        <div class="analysis-card">
            <h4>🤖 Analyse IA du Style</h4>
            <p>{recommendations['analysis']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Recommandations
        st.markdown("### 🎯 Vos Découvertes Personnalisées")
        
        for i, rec in enumerate(recommendations['artists']):
            with st.expander(f"🎵 {rec['name']} - {rec['similarity_type'].title()}", expanded=i < 2):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if rec['spotify_data']['image']:
                        st.image(rec['spotify_data']['image'], width=150)
                    
                    # Affichage de la vidéo YouTube si disponible
                    if rec['spotify_data'].get('youtube_url'):
                        st.markdown("**🎥 Vidéo YouTube :**")
                        display_youtube_video(
                            rec['spotify_data']['youtube_url'], 
                            f"{rec['name']} - {rec['spotify_data']['top_tracks'][0]['name'] if rec['spotify_data']['top_tracks'] else 'Top Track'}"
                        )
                    elif youtube_api_key:
                        st.info("🎥 Vidéo YouTube non trouvée pour cet artiste")
                
                with col2:
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <h4>{rec['name']}</h4>
                        <p><strong>Pourquoi cette recommandation :</strong> {rec['reason']}</p>
                        <p><strong>Genres :</strong> {', '.join(rec['spotify_data']['genres'][:3]) or 'Varié'}</p>
                        <p><strong>Popularité :</strong> {rec['spotify_data']['popularity']}/100</p>
                        <p><strong>Confiance IA :</strong> {rec['confidence']}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Top tracks
                st.markdown("**🎼 À écouter absolument :**")
                for track in rec['spotify_data']['top_tracks']:
                    col_track1, col_track2 = st.columns([3, 1])
                    with col_track1:
                        st.markdown(f"""
                        <div class="track-card">
                            <strong>{track['name']}</strong>
                            <br><small>Album: {track['album']['name']}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_track2:
                        if track['external_urls']['spotify']:
                            st.markdown(f"[🎧 Écouter]({track['external_urls']['spotify']})")
                
                # Lien artiste
                if rec['spotify_data']['external_urls']['spotify']:
                    st.markdown(f"[🎤 Voir l'artiste complet sur Spotify]({rec['spotify_data']['external_urls']['spotify']})")
        
        # Bouton pour nouvelle recherche
        if st.button("🔄 Découvrir un autre artiste"):
            st.session_state.recommendations_ready = False
            st.session_state.current_artist_data = None
            st.session_state.recommendations = []
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🎵 <strong>Music Discovery AI</strong> - Propulsé par Spotify API & OpenAI</p>
    <p>🚀 Déployez gratuitement sur <strong>Streamlit Cloud</strong></p>
    <p>💡 Vos données restent privées - APIs officielles uniquement</p>
</div>
""", unsafe_allow_html=True)
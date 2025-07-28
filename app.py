import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import openai
import requests
import json
from typing import List, Dict, Optional
import time
import base64

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
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, .main-header, .artist-card, .recommendation-card, .analysis-card, .track-card {
        font-family: 'Montserrat', sans-serif !important;
    }
    .main-header {
        background: linear-gradient(135deg, #1db954 0%, #191414 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 24px rgba(29,185,84,0.10);
    }
    .artist-card {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #1db954;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        transition: box-shadow 0.3s, transform 0.3s;
    }
    .artist-card:hover {
        box-shadow: 0 8px 24px rgba(29,185,84,0.15);
        transform: translateY(-4px) scale(1.02);
    }
    .recommendation-card {
        background: linear-gradient(135deg, #1db954 0%, #1ed760 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.18);
        transition: box-shadow 0.3s, transform 0.3s;
    }
    .recommendation-card:hover {
        box-shadow: 0 8px 24px rgba(29,185,84,0.22);
        transform: translateY(-4px) scale(1.02);
    }
    .track-card {
        background: #f0f0f0;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #1db954;
        transition: box-shadow 0.3s, transform 0.3s;
    }
    .track-card:hover {
        box-shadow: 0 4px 12px rgba(29,185,84,0.10);
        transform: scale(1.01);
    }
    .analysis-card {
        background: #e8f5e8;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        transition: box-shadow 0.3s, transform 0.3s;
    }
    .analysis-card:hover {
        box-shadow: 0 8px 24px rgba(40,167,69,0.13);
        transform: translateY(-2px) scale(1.01);
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
        transition: background 0.3s, box-shadow 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1ed760 0%, #1db954 100%);
        box-shadow: 0 2px 8px rgba(29,185,84,0.18);
    }
    .spotify-embed {
        border-radius: 12px;
        overflow: hidden;
        margin: 1rem 0;
    }
    /* Responsive */
    @media (max-width: 600px) {
        .main-header, .artist-card, .recommendation-card, .analysis-card {
            padding: 1rem;
            font-size: 0.95rem;
        }
        .stButton > button {
            font-size: 0.95rem;
        }
    }
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25em 0.7em;
        font-size: 0.85em;
        font-weight: 600;
        border-radius: 8px;
        margin-right: 0.5em;
        background: #1db954;
        color: #fff;
        vertical-align: middle;
    }
    .badge-genre { background: #191414; color: #fff; }
    .badge-similar { background: #1db954; color: #fff; }
    .badge-influence { background: #ffb300; color: #191414; }
    .badge-creative { background: #00bcd4; color: #fff; }
    .badge-surprise { background: #e91e63; color: #fff; }
    /* Dark mode toggle */
    .dark-mode {
        background: #191414 !important;
        color: #e8f5e8 !important;
    }
    .dark-mode .main-header {
        background: linear-gradient(135deg, #232526 0%, #191414 100%);
        color: #fff;
    }
    .dark-mode .artist-card, .dark-mode .recommendation-card, .dark-mode .analysis-card, .dark-mode .track-card {
        background: #232526 !important;
        color: #e8f5e8 !important;
        border-left-color: #1db954 !important;
    }
    .dark-mode .recommendation-card {
        background: linear-gradient(135deg, #232526 0%, #1db954 100%) !important;
    }
    .dark-mode .badge-genre { background: #fff; color: #191414; }
    .dark-mode .badge-similar { background: #1db954; color: #fff; }
    .dark-mode .badge-influence { background: #ffb300; color: #191414; }
    .dark-mode .badge-creative { background: #00bcd4; color: #fff; }
    .dark-mode .badge-surprise { background: #e91e63; color: #fff; }
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

def verify_and_enrich_recommendations(spotify: spotipy.Spotify, recommendations: List[Dict]) -> List[Dict]:
    """Vérifie que les artistes existent sur Spotify, enrichit les données et trie par date de sortie la plus récente."""
    enriched_recs = []
    for rec in recommendations:
        try:
            # Recherche l'artiste sur Spotify
            results = spotify.search(q=rec['name'], type='artist', limit=1)
            if results['artists']['items']:
                artist = results['artists']['items'][0]
                # Récupère les top tracks
                top_tracks = spotify.artist_top_tracks(artist['id'], country='FR')
                # Récupère les albums/singles pour trouver la date la plus récente
                albums = spotify.artist_albums(artist['id'], album_type='album,single', limit=10)
                latest_date = None
                for album in albums['items']:
                    date = album['release_date']
                    if not latest_date or date > latest_date:
                        latest_date = date
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
                        'latest_release_date': latest_date
                    }
                }
                enriched_recs.append(enriched_rec)
        except Exception as e:
            st.warning(f"Artiste '{rec['name']}' non trouvé sur Spotify")
            continue
    # Trie par date de sortie la plus récente (ordre décroissant)
    enriched_recs.sort(key=lambda x: x['spotify_data']['latest_release_date'] or '', reverse=True)
    return enriched_recs

# Ajout du toggle dark mode
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.experimental_rerun()

with st.sidebar:
    st.markdown("---")
    dark_label = "🌙 Mode sombre activé" if st.session_state.dark_mode else "☀️ Mode clair activé"
    if st.button(dark_label):
        toggle_dark_mode()

# Applique la classe dark-mode si activé
if st.session_state.dark_mode:
    st.markdown("""
    <script>
    document.body.classList.add('dark-mode');
    </script>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <script>
    document.body.classList.remove('dark-mode');
    </script>
    """, unsafe_allow_html=True)

# Sidebar pour la configuration
with st.sidebar:
    st.header("🔧 Configuration")
    
    # Tentative de chargement des secrets Streamlit
    default_openai = ""
    default_spotify_id = ""
    default_spotify_secret = ""
    secrets_loaded = False
    
    try:
        default_openai = st.secrets["OPENAI_API_KEY"]
        default_spotify_id = st.secrets["SPOTIFY_CLIENT_ID"]
        default_spotify_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]
        secrets_loaded = True
        
        st.success("🔒 Clés par défaut chargées")
        st.info("💡 Vous pouvez utiliser vos propres clés ci-dessous")
    except:
        st.warning("⚠️ Pas de clés par défaut - Entrez les vôtres")
    
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
    """)

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
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Zone pour les comptes nécessaires
    st.markdown("""
    <div class="analysis-card">
        <h3>🔑 Comptes requis (gratuits)</h3>
        <p><strong>OpenAI API :</strong> <a href="https://platform.openai.com" target="_blank">platform.openai.com</a></p>
        <p><strong>Spotify Developer :</strong> <a href="https://developer.spotify.com/dashboard" target="_blank">developer.spotify.com/dashboard</a></p>
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
                                    ia_response['recommendations']
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
                
                with col2:
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <h4>{rec['name']}</h4>
                        <p><strong>Pourquoi cette recommandation :</strong> {rec['reason']}</p>
                        <div style="margin-bottom:0.5em;">
                          {''.join([f'<span class=\'badge badge-genre\'>{genre}</span>' for genre in rec['spotify_data']['genres'][:3]]) or '<span class=\'badge badge-genre\'>Varié</span>'}
                          <span class='badge badge-similar'>{rec['similarity_type'].replace('même genre','Similaire').replace('influence historique','Influence').replace('approche créative','Créatif').replace('découverte surprenante','Surprise')}</span>
                          <span class='badge' style='background:#fff;color:#191414;'>Popularité: {rec['spotify_data']['popularity']}/100</span>
                          <span class='badge' style='background:#191414;color:#fff;'>Confiance IA: {rec['confidence']}%</span>
                          <span class='badge' style='background:#00bcd4;color:#fff;'>Dernière sortie: {rec['spotify_data']['latest_release_date'] or 'N/A'}</span>
                        </div>
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

# Footer enrichi
st.markdown("""
---
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🎵 <strong>Music Discovery AI</strong> - Propulsé par Spotify API & OpenAI</p>
    <p>🚀 Déployez gratuitement sur <strong>Streamlit Cloud</strong></p>
    <p>💡 Vos données restent privées - APIs officielles uniquement</p>
    <p style='margin-top:1em;'>
        <a href='https://github.com/jessicakuijer/music-discovery-ai' target='_blank' style='margin:0 0.5em;'><img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg' width='28' style='vertical-align:middle;'/></a>
        <a href='https://www.linkedin.com/in/jessicakuijer/' target='_blank' style='margin:0 0.5em;'><img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg' width='28' style='vertical-align:middle;'/></a>
    </p>
    <p style='font-size:0.9em;color:#aaa;'>Design IA & UI par <strong>Music Discovery AI</strong></p>
</div>
""", unsafe_allow_html=True)
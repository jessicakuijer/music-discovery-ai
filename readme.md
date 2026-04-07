# 🎵 Music Discovery AI

**Music Discovery AI** est une application qui utilise l'intelligence artificielle et les données Spotify pour vous faire découvrir de nouveaux artistes selon vos goûts musicaux. Elle enrichit chaque recommandation avec des données Spotify et, si vous fournissez une clé API YouTube, intègre automatiquement une vidéo musicale pour chaque artiste suggéré.

## ✨ Fonctionnalités principales

- 🤖 Analyse IA du style musical d'un artiste de votre choix
- 🎯 8 recommandations personnalisées, classées par type de similarité (genre, époque, créativité, surprise)
- 📊 Données enrichies : genres, popularité, followers, top tracks Spotify
- 🎧 Liens directs pour écouter sur Spotify
- 🎥 Vidéo YouTube intégrée pour chaque artiste recommandé (si clé API fournie)
- 💡 Justification IA pour chaque recommandation

## 🔍 Comment ça marche ?

1. **Vous saisissez le nom d'un artiste que vous aimez**
2. L'application récupère ses données Spotify (genres, popularité, top morceaux, artistes similaires)
3. L'IA (OpenAI) analyse le style de l'artiste et génère 8 recommandations selon une logique précise :
   - 3 artistes du même genre mais moins mainstream
   - 2 artistes d'une époque différente avec des influences similaires
   - 2 artistes à l'approche créative proche
   - 1 découverte surprenante mais cohérente
4. Pour chaque artiste recommandé :
   - Vérification de l'existence sur Spotify
   - Récupération des données principales (image, genres, top tracks, popularité)
   - Recherche d'une vidéo YouTube (si clé API fournie)
5. **Vous découvrez les artistes, écoutez leurs morceaux, et visionnez une vidéo directement dans l'interface**

## 🖥️ Exemple d'utilisation

- **Input** : "Radiohead"
- **Analyse IA** : "Style post-rock expérimental avec influences électroniques."
- **Recommandations** :
  - Portishead (trip-hop atmosphérique)
  - Sigur Rós (post-rock épique)
  - Massive Attack (textures sonores)
  - ...
- **Pour chaque artiste** :
  - Top 3 morceaux à écouter
  - Genres, popularité, followers
  - Lien Spotify
  - Vidéo YouTube intégrée
  - Justification IA de la recommandation

## ⚙️ Prérequis & configuration

- **Clé API OpenAI** (obligatoire) : pour l'analyse et la génération des recommandations
- **Clés Spotify Developer** (obligatoire) : pour accéder aux données musicales
- **Clé API YouTube Data v3** (optionnelle) : pour intégrer automatiquement une vidéo musicale par artiste recommandé

**Où renseigner les clés**

1. **Fichier local (recommandé)** : copiez `.streamlit/secrets.toml.example` vers `.streamlit/secrets.toml`, ouvrez ce dernier et collez vos clés. Ce fichier est ignoré par Git : il ne part pas avec le dépôt.
2. **Barre latérale** : vous pouvez aussi tout saisir à la main dans l’application (session locale, rien n’est enregistré sur un serveur).

Le dépôt ne contient que l’exemple avec des champs vides ; chaque utilisateur remplit `secrets.toml` ou la barre latérale avec ses propres clés.

## 🔒 Confidentialité

- Les clés API restent sur votre machine (`secrets.toml` non versionné ou saisie dans la barre latérale)
- Aucune donnée utilisateur n'est collectée ou stockée
- L'application communique uniquement avec les APIs officielles (Spotify, OpenAI, YouTube)

## 🛠️ Dépendances principales

- [spotipy](https://spotipy.readthedocs.io/) (API Spotify)
- [openai](https://platform.openai.com/docs/api-reference)
- [requests](https://docs.python-requests.org/)
- [streamlit](https://streamlit.io/)

## 🙏 Crédits

Ce projet est inspiré par la passion de la découverte musicale et l'envie de proposer des recommandations vraiment personnalisées grâce à l'IA.

---

*Explorez, écoutez, découvrez... et laissez l'IA élargir vos horizons musicaux !*
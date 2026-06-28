# 🎵 Music Discovery AI

Vous connaissez déjà un artiste que vous adorez, mais vous tournez en boucle sur les mêmes titres ? **Music Discovery AI** part de cet artiste, croise les données Spotify et une analyse OpenAI, et vous propose **8 découvertes moins mainstream** — chacune expliquée, enrichie et prête à écouter.

---

## Ce que vous obtenez

- **Analyse de style** — l’IA résume le univers musical de l’artiste que vous choisissez
- **8 recommandations ciblées** — pas une simple liste « similaire sur Spotify », mais une sélection variée (genre, époque, approche créative, surprise)
- **Données Spotify** — image, genres, popularité, followers, top morceaux, lien direct
- **Vidéos YouTube** — intégrées pour chaque recommandation si une clé YouTube est configurée
- **Filtres et tri** — par type de similarité ou par niveau de confiance de l’IA
- **Vue détail** — fiche complète par artiste recommandé (justification, morceaux, lecteur vidéo)
- **Interface bilingue** — français et anglais (langue détectée ou choisie dans la barre latérale)

---

## Comment ça marche

1. Vous entrez le nom d’un artiste (avec suggestions Spotify pendant la saisie).
2. L’app récupère son profil Spotify : genres, popularité, top tracks, artistes reliés.
3. OpenAI analyse le style et propose **8 artistes** selon cette répartition :
   - **3** dans le même genre, moins mainstream
   - **2** d’une autre époque, influences proches
   - **2** à l’approche créative similaire
   - **1** découverte surprenante mais cohérente
4. Chaque nom est **vérifié sur Spotify**, enrichi (top 3 morceaux, métadonnées), puis associé à une **vidéo YouTube** si possible.
5. Vous parcourez les résultats, filtrez, ouvrez le détail d’un artiste, et relancez une nouvelle recherche quand vous voulez.

---

## Exemple

| Étape | Résultat |
|--------|----------|
| **Vous cherchez** | Radiohead |
| **Analyse IA** | Post-rock expérimental, textures sombres, influences électroniques |
| **Découvertes possibles** | Portishead, Sigur Rós, Massive Attack… |
| **Par carte** | Pourquoi l’IA recommande cet artiste, genres, confiance, top morceaux, Spotify, vidéo |

---

## Démarrage rapide

**Prérequis** : Python 3.10+, comptes développeur [OpenAI](https://platform.openai.com) et [Spotify](https://developer.spotify.com/dashboard). YouTube est optionnel ([Google Cloud](https://console.cloud.google.com/apis/library/youtube.googleapis.com)).

```bash
git clone <url-du-repo>
cd generative-music-py
python -m venv .venv
source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Éditez secrets.toml avec vos clés
streamlit run app.py
```

L’application s’ouvre dans le navigateur. Configurez vos clés si besoin, puis lancez une découverte depuis l’accueil.

---

## Clés API

| Clé | Obligatoire | Rôle |
|-----|-------------|------|
| `OPENAI_API_KEY` | Oui | Analyse et recommandations |
| `SPOTIFY_CLIENT_ID` | Oui | Données artistes et morceaux |
| `SPOTIFY_CLIENT_SECRET` | Oui | Authentification Spotify |
| `YOUTUBE_API_KEY` | Non | Vidéos intégrées par recommandation |

**Où les mettre**

- **`.streamlit/secrets.toml`** (recommandé) — copiez l’exemple, remplissez vos valeurs. Ce fichier n’est **pas versionné** : le dépôt ne contient que des champs vides.
- **Barre latérale** — si la configuration est incomplète, vous pouvez saisir les clés manuellement (session locale uniquement).

**Usage perso** : dès que OpenAI + Spotify sont dans `secrets.toml`, l’app les charge **automatiquement** (connexion Spotify incluse, champs masqués). YouTube est pris en charge de la même façon si la clé est présente.

**Déploiement public** : ne mettez jamais vos clés dans l’interface visible par d’autres utilisateurs. Utilisez les secrets de la plateforme d’hébergement (ex. Streamlit Cloud) et laissez les champs vides côté UI.

---

## Confidentialité

- Les clés restent sur votre machine ou sur votre environnement de déploiement.
- Aucune base de données utilisateur : pas de compte, pas d’historique stocké côté serveur.
- Seules les APIs officielles Spotify, OpenAI et YouTube sont contactées.

---

## Dépendances

- [Streamlit](https://streamlit.io/) — interface web
- [spotipy](https://spotipy.readthedocs.io/) — API Spotify
- [openai](https://platform.openai.com/docs) — modèle de recommandation
- [requests](https://docs.python-requests.org/) — appels HTTP (YouTube)

---

*Un artiste que vous aimez → huit pistes pour sortir de votre playlist habituelle.*

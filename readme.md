# 🎵 Music Discovery AI

Application Streamlit qui utilise l'IA pour découvrir de nouveaux artistes basés sur vos goûts musicaux.

## 🎯 Fonctionnalités

- 🤖 **Analyse IA** du style musical d'un artiste
- 🎵 **8 recommandations personnalisées** par recherche
- 📊 **Données Spotify** complètes (genres, popularité, top tracks)
- 🎧 **Liens directs** vers Spotify pour écouter
- 🎨 **Interface moderne** et intuitive

## 🚀 Déploiement Express

### 1. Configuration Spotify Developer

1. **Créer une app Spotify** :
   - Allez sur [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
   - Cliquez "Create app"
   - Nom : `Music Discovery AI`
   - Description : `AI-powered music discovery app`
   - Website : https://votre-app.streamlit.app
   - Redirect URIs : AJOUTEZ CES 2 LIGNES :
     - https://votre-app.streamlit.app/callback
   - API utilisée : `Web API`

2. **Récupérer les clés** :
   - `Client ID` : Visible sur le dashboard
   - `Client Secret` : Cliquez "Show client secret"
   - **⚠️ Gardez ces clés privées !**

### 2. Configuration OpenAI

1. **Créer une clé API** :
   - Allez sur [platform.openai.com](https://platform.openai.com)
   - Section "API Keys" → "Create new secret key"
   - **⚠️ Copiez immédiatement la clé !**

### 3. Structure du Projet

```
music-discovery-ai/
├── app.py                 # Application Streamlit principale
├── requirements.txt       # Dépendances Python
└── README.md             # Ce fichier
```

### 4. Déploiement sur Streamlit Cloud

1. **GitHub** :
   - Créez un repository public
   - Uploadez les 3 fichiers

2. **Streamlit Cloud** :
   - [share.streamlit.io](https://share.streamlit.io)
   - "New app" → Sélectionnez votre repo
   - Fichier principal : `app.py`
   - Deploy !

3. **Configuration des utilisateurs** :
   - Les utilisateurs entreront leurs propres clés API
   - Aucune configuration serveur nécessaire

## 💡 Utilisation

### Pour les utilisateurs finaux

1. **APIs requises** (gratuites) :
   - Clé OpenAI : [platform.openai.com](https://platform.openai.com)
   - Spotify Developer : [developer.spotify.com](https://developer.spotify.com)

2. **Workflow** :
   - Entrer les clés API dans la sidebar
   - Tester la connexion Spotify
   - Rechercher un artiste aimé
   - Découvrir 8 nouveaux artistes !

## 🎨 Exemple d'Usage

**Input :** "Radiohead"

**Sortie IA :**
- **Analyse** : "Style post-rock expérimental avec influences électroniques"
- **8 Recommandations** :
  - Thom Yorke (même univers)
  - Portishead (trip-hop atmosphérique)  
  - Sigur Rós (post-rock épique)
  - Massive Attack (textures sonores)
  - etc...

**Pour chaque artiste :**
- 🎧 Top 3 tracks à écouter
- 📊 Données Spotify (genres, popularité)
- 🔗 Liens directs vers Spotify
- 💡 Justification IA de la recommandation

## 🔧 Développement Local

```bash
# Installation
pip install -r requirements.txt

# Variables d'environnement (optionnel)
export SPOTIPY_CLIENT_ID="votre_client_id"
export SPOTIPY_CLIENT_SECRET="votre_client_secret"

# Lancement
streamlit run app.py
```

## 🎯 Algorithme de Recommandation

L'IA utilise cette logique pour 8 recommandations :

- **3 artistes** : Même genre, moins mainstream
- **2 artistes** : Époque différente, influences similaires
- **2 artistes** : Approche créative proche
- **1 artiste** : Découverte surprenante mais cohérente

## 🔒 Sécurité

- **Clés API** : Restent côté client uniquement
- **Données** : Aucun stockage serveur
- **APIs** : Communication directe Spotify/OpenAI
- **Privacy** : Aucune donnée utilisateur collectée

## 📈 Évolutions Possibles

- 🎵 **Génération de playlists** Spotify automatique
- 📱 **Mode découverte par humeur** 
- 🎤 **Analyse de lyrics** avec l'IA
- 📊 **Historique personnel** des découvertes
- 🌍 **Découvertes géographiques** (artistes par pays)

## 🎵 APIs Utilisées

- **Spotify Web API** : Données musicales
- **OpenAI GPT-4o-mini** : Analyse et recommandations
- **Streamlit** : Interface utilisateur

## 🎤 Crédit

Inspiré par l'amour de la découverte musicale et la puissance de l'IA pour personnaliser l'expérience d'écoute !

---

🚀 **Ready to discover new music in 5 minutes!**
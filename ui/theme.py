import html
from typing import Dict

import streamlit as st
import streamlit.components.v1 as components

from ui.i18n import normalize_similarity_type

COLORS = {
    "ink": "#0B0B10",
    "surface": "#14141B",
    "elevated": "#1C1C26",
    "text": "#F4F4F6",
    "muted": "#9A9AA8",
    "subtle": "#6B6B78",
    "accent_green": "#34E0A1",
}

SIMILARITY_ACCENTS = {
    "same_genre": "#34E0A1",
    "historical_influence": "#F5B544",
    "creative_approach": "#8B7CFF",
    "surprise_discovery": "#FF6B8B",
}

SIMILARITY_TILES = {
    "same_genre": "linear-gradient(140deg,#3DEFAE,#0C6B4C)",
    "historical_influence": "linear-gradient(140deg,#FFC95E,#8A4E0E)",
    "creative_approach": "linear-gradient(140deg,#9D8CFF,#352a7d)",
    "surprise_discovery": "linear-gradient(140deg,#FF7E9B,#7d2238)",
}

SIMILARITY_GLOW = {
    "same_genre": "radial-gradient(circle,#34E0A1,transparent 64%)",
    "historical_influence": "radial-gradient(circle,#F5B544,transparent 64%)",
    "creative_approach": "radial-gradient(circle,#8B7CFF,transparent 64%)",
    "surprise_discovery": "radial-gradient(circle,#FF6B8B,transparent 64%)",
}

EXAMPLE_ARTISTS = ["Radiohead", "Billie Eilish", "Miles Davis", "Aphex Twin"]


def similarity_style(similarity_type: str) -> Dict[str, str]:
    key = normalize_similarity_type(similarity_type)
    accent = SIMILARITY_ACCENTS.get(key, COLORS["accent_green"])
    return {
        "accent": accent,
        "tile": SIMILARITY_TILES.get(key, SIMILARITY_TILES["same_genre"]),
        "glow": SIMILARITY_GLOW.get(key, SIMILARITY_GLOW["same_genre"]),
        "soft": f"{accent}1F",
        "ring": f"{accent}55",
    }


def esc(text: str) -> str:
    return html.escape(str(text or ""))


def render_html(content: str) -> None:
    """Affiche du HTML sans interprétation Markdown (évite les blocs de code indentés)."""
    html_content = content.strip()
    if hasattr(st, "html"):
        st.html(html_content)
    else:
        st.markdown(html_content, unsafe_allow_html=True)


def inject_reco_card_bindings() -> None:
    """Superpose le bouton Streamlit sur la carte (clic natif, sans lien HTML)."""
    components.html(
        """
<script>
(function () {
  const doc = window.parent.document;

  function bindCards() {
    doc.querySelectorAll("[data-reco-shell]").forEach(function (shell) {
      if (shell.dataset.recoBound === "1") return;

      const block = shell.closest('[data-testid="stVerticalBlock"]');
      if (!block) return;

      const card = shell.querySelector(".md-reco-card");
      const btnHost = block.querySelector('[data-testid="stButton"]');
      if (!card || !btnHost) return;

      const btn = btnHost.querySelector("button");
      if (!btn) return;

      const wrap = btnHost.closest('[data-testid="stElementContainer"]') || btnHost.parentElement;
      if (!wrap) return;

      shell.dataset.recoBound = "1";
      block.classList.add("md-reco-card-block");
      block.style.position = "relative";
      block.style.marginBottom = "12px";

      wrap.style.position = "absolute";
      wrap.style.inset = "0";
      wrap.style.zIndex = "2";
      wrap.style.margin = "0";
      wrap.style.padding = "0";

      btnHost.style.height = "100%";
      btnHost.style.width = "100%";

      btn.style.opacity = "0";
      btn.style.width = "100%";
      btn.style.height = card.offsetHeight + "px";
      btn.style.minHeight = card.offsetHeight + "px";
      btn.style.border = "none";
      btn.style.background = "transparent";
      btn.style.boxShadow = "none";
      btn.style.outline = "none";
      btn.style.padding = "0";
      btn.style.margin = "0";
      btn.style.cursor = "pointer";

      card.style.pointerEvents = "none";
      card.style.marginBottom = "0";

      const setHover = function (on) {
        card.classList.toggle("md-reco-card--hover", on);
      };
      btn.addEventListener("mouseenter", function () { setHover(true); });
      btn.addEventListener("mouseleave", function () { setHover(false); });
      btn.addEventListener("focus", function () { setHover(true); });
      btn.addEventListener("blur", function () { setHover(false); });
    });
  }

  bindCards();
  new MutationObserver(bindCards).observe(doc.body, { childList: true, subtree: true });
})();
</script>
        """,
        height=0,
        width=0,
    )


def inject_global_css() -> None:
    st.markdown(
        """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Hanken+Grotesk:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
    :root {
        --md-ink: #0B0B10;
        --md-surface: #14141B;
        --md-elevated: #1C1C26;
        --md-text: #F4F4F6;
        --md-muted: #9A9AA8;
        --md-subtle: #6B6B78;
        --md-green: #34E0A1;
    }

    html, body, [class*="css"] {
        font-family: 'Hanken Grotesk', sans-serif;
        color: var(--md-text);
    }

    .stApp {
        background: radial-gradient(140% 100% at 50% 0%, #16161c 0%, #0a0a0e 60%);
    }

    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer, .stDeployButton { visibility: hidden; }

    section[data-testid="stSidebar"] {
        background: var(--md-surface);
        border-right: 1px solid rgba(255,255,255,.08);
    }
    section[data-testid="stSidebar"] * {
        color: var(--md-text) !important;
    }
    section[data-testid="stSidebar"] .stTextInput input {
        background: var(--md-elevated) !important;
        border: 1px solid rgba(255,255,255,.12) !important;
        color: var(--md-text) !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #34E0A1, #1FB37D) !important;
        color: var(--md-ink) !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] .md-sidebar-card {
        background: var(--md-elevated);
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 14px;
        padding: 16px;
        margin-top: 12px;
        font-size: 14px;
        line-height: 1.5;
    }
    section[data-testid="stSidebar"] .md-sidebar-card a {
        color: var(--md-green) !important;
    }

    .block-container {
        padding-top: 1.5rem;
        max-width: 920px;
    }

    .md-app-shell {
        position: relative;
        overflow: hidden;
        font-family: 'Hanken Grotesk', sans-serif;
        color: var(--md-text);
    }

    .md-blob {
        position: absolute;
        border-radius: 50%;
        filter: blur(46px);
        pointer-events: none;
        z-index: 0;
    }
    .md-blob-purple { width: 420px; height: 420px; background: radial-gradient(circle,#8B7CFF,transparent 62%); opacity: .34; top: -140px; left: -80px; }
    .md-blob-pink { width: 380px; height: 380px; background: radial-gradient(circle,#FF6B8B,transparent 62%); opacity: .28; bottom: -120px; right: -60px; }
    .md-blob-green { width: 300px; height: 300px; background: radial-gradient(circle,#34E0A1,transparent 62%); opacity: .22; top: 40px; right: -40px; }

    .md-nav {
        position: relative;
        z-index: 2;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 28px;
    }
    .md-logo {
        display: flex;
        align-items: center;
        gap: 11px;
    }
    .md-logo-icon {
        width: 30px;
        height: 30px;
        border-radius: 9px;
        background: linear-gradient(135deg,#34E0A1,#8B7CFF 50%,#FF6B8B 85%,#F5B544);
    }
    .md-logo-text {
        font: 800 16px/1 'Bricolage Grotesque', sans-serif;
        letter-spacing: -0.01em;
    }
    .md-spotify-badge {
        font: 700 10px/1 'Space Mono', monospace;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--md-green);
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .md-spotify-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--md-green);
        box-shadow: 0 0 8px var(--md-green);
    }

    .md-hero { position: relative; z-index: 1; }
    .md-kicker {
        font: 700 12px/1 'Space Mono', monospace;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--md-green);
    }
    .md-title {
        font: 800 58px/1.03 'Bricolage Grotesque', sans-serif;
        letter-spacing: -0.03em;
        margin: 16px 0 0;
    }
    .md-title-gradient {
        background: linear-gradient(100deg,#34E0A1,#8B7CFF 48%,#FF6B8B 78%,#F5B544);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    .md-subtitle {
        font: 400 17px/1.5 'Hanken Grotesk', sans-serif;
        color: var(--md-muted);
        margin-top: 18px;
        max-width: 520px;
    }

    .md-card {
        background: var(--md-surface);
        border: 1px solid rgba(255,255,255,.06);
        border-radius: 16px;
    }
    .md-analysis {
        background: linear-gradient(135deg,#16131f,#120f18);
        border: 1px solid #8B7CFF33;
        border-radius: 16px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        margin-top: 22px;
    }
    .md-analysis-label {
        font: 700 11px/1 'Space Mono', monospace;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #B9AEFF;
    }
    .md-analysis-text {
        font: 500 16px/1.55 'Hanken Grotesk', sans-serif;
        color: #E6E6EC;
        margin-top: 11px;
    }

    .md-reco-card {
        display: flex;
        gap: 18px;
        align-items: center;
        padding: 16px 18px;
        background: var(--md-surface);
        border: 1px solid rgba(255,255,255,.06);
        border-radius: 16px;
        position: relative;
        overflow: hidden;
        margin-bottom: 0;
        transition: border-color .15s ease, background .15s ease;
    }
    .md-reco-card.md-reco-card--hover {
        border-color: rgba(255,255,255,.14);
        background: rgba(255,255,255,.03);
    }
    .md-reco-card-block:focus-within .md-reco-card {
        box-shadow: 0 0 0 2px rgba(52,224,161,.35);
    }
    .md-track-list {
        overflow: hidden;
        margin-top: 0;
    }
    a.md-track-row-link {
        display: block;
        text-decoration: none;
        color: inherit;
        cursor: pointer;
    }
    .md-track-row {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 13px 16px;
        border-bottom: 1px solid rgba(255,255,255,.05);
        transition: background .15s ease;
    }
    a.md-track-row-link:hover .md-track-row,
    a.md-track-row-link:focus-visible .md-track-row {
        background: rgba(255,255,255,.03);
    }
    a.md-track-row-link:focus-visible {
        outline: none;
    }
    a.md-track-row-link:focus-visible .md-track-row {
        box-shadow: inset 0 0 0 2px rgba(52,224,161,.35);
    }
    .md-track-index {
        font: 700 12px/1 'Space Mono', monospace;
        color: #6B6B78;
        width: 16px;
        flex: none;
    }
    .md-track-play {
        width: 34px;
        height: 34px;
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex: none;
        font: 700 12px/1 'Hanken Grotesk', sans-serif;
        color: #fff;
    }
    .md-track-meta {
        flex: 1;
        min-width: 0;
    }
    .md-track-name {
        font: 600 15px/1.2 'Hanken Grotesk', sans-serif;
        color: #F4F4F6;
    }
    .md-track-album {
        font: 400 11px/1 'Space Mono', monospace;
        color: #6B6B78;
        margin-top: 3px;
    }
    .md-track-arrow {
        font: 400 15px/1 'Hanken Grotesk', sans-serif;
        color: #6B6B78;
        flex: none;
    }
    .md-reco-accent {
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        border-radius: 16px 0 0 16px;
    }
    .md-reco-avatar {
        width: 78px;
        height: 78px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font: 800 34px/1 'Bricolage Grotesque', sans-serif;
        color: #fff;
        flex: none;
        position: relative;
    }
    .md-reco-rank {
        position: absolute;
        top: 5px;
        left: 5px;
        font: 700 9px/1 'Space Mono', monospace;
        color: rgba(255,255,255,.85);
        background: rgba(0,0,0,.35);
        border-radius: 6px;
        padding: 3px 5px;
    }
    .md-badge {
        font: 700 9px/1 'Space Mono', monospace;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        border-radius: 999px;
        padding: 5px 9px;
        display: inline-block;
    }
    .md-conf-bar {
        flex: 1;
        height: 5px;
        border-radius: 999px;
        background: var(--md-ink);
        overflow: hidden;
    }
    .md-conf-fill { height: 100%; border-radius: 999px; }

    .md-empty-icon {
        width: 64px;
        height: 64px;
        border-radius: 18px;
        background: var(--md-surface);
        border: 1px solid rgba(255,255,255,.08);
        display: flex;
        align-items: center;
        justify-content: center;
        font: 400 30px/1 'Hanken Grotesk', sans-serif;
        color: var(--md-subtle);
        margin: 0 auto;
    }
    .md-empty-title {
        font: 800 26px/1.2 'Bricolage Grotesque', sans-serif;
        text-align: center;
        margin-top: 22px;
    }
    .md-empty-text {
        font: 400 15px/1.5 'Hanken Grotesk', sans-serif;
        color: var(--md-muted);
        text-align: center;
        margin-top: 10px;
        max-width: 380px;
        margin-left: auto;
        margin-right: auto;
    }

    .md-loading-wrap {
        position: relative;
        min-height: 420px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 40px 20px;
    }
    .md-spinner {
        position: relative;
        width: 74px;
        height: 74px;
    }
    .md-spinner-ring {
        position: absolute;
        inset: 0;
        border-radius: 50%;
        border: 3px solid rgba(255,255,255,.08);
    }
    .md-spinner-active {
        position: absolute;
        inset: 0;
        border-radius: 50%;
        border: 3px solid transparent;
        border-top-color: #34E0A1;
        border-right-color: #8B7CFF;
        animation: mdspin .9s linear infinite;
    }
    @keyframes mdspin { to { transform: rotate(360deg); } }
    @keyframes mdpulse { 0%,100% { opacity: .35; } 50% { opacity: 1; } }

    .md-step {
        display: flex;
        align-items: center;
        gap: 12px;
        font: 500 15px/1 'Hanken Grotesk', sans-serif;
        margin-bottom: 12px;
    }
    .md-step-dot {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font: 700 11px/1 'Space Mono', monospace;
        flex: none;
    }

    .md-youtube-embed {
        border-radius: 16px;
        overflow: hidden;
        aspect-ratio: 16/9;
        margin: 16px 0;
        border: 1px solid rgba(255,255,255,.07);
    }
    .md-youtube-embed iframe { width: 100%; height: 100%; border: none; }

    [data-testid="stIFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,.07);
        margin: 4px 0 0;
    }
    [data-testid="stIFrame"] iframe {
        display: block;
        width: 100%;
        border: none;
    }

    .md-footer {
        text-align: center;
        color: var(--md-subtle);
        padding: 2rem 0 1rem;
        font-size: 14px;
    }
    .md-footer strong { color: var(--md-muted); }

    .md-sticky-bar {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 18px 0;
        border-bottom: 1px solid rgba(255,255,255,.06);
        margin-bottom: 24px;
    }

    div[data-testid="stForm"] {
        border: none;
        padding: 0;
    }
    .md-search-form div[data-testid="stForm"] div[data-testid="stTextInput"] > div {
        background: transparent !important;
        border: none !important;
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        min-height: 44px !important;
        padding-left: 30px !important;
    }
    .md-search-form div[data-testid="stForm"] div[data-testid="stTextInput"] > div::before {
        content: "";
        position: absolute;
        left: 2px;
        top: 50%;
        transform: translateY(-50%);
        width: 15px;
        height: 15px;
        border: 2px solid #6B6B78;
        border-radius: 50%;
        box-sizing: border-box;
        pointer-events: none;
    }
    .md-search-form div[data-testid="stForm"] div[data-testid="stTextInput"] > div::after {
        content: "";
        position: absolute;
        left: 14px;
        top: calc(50% + 6px);
        width: 7px;
        height: 2px;
        background: #6B6B78;
        transform: translateY(-50%) rotate(45deg);
        border-radius: 2px;
        pointer-events: none;
    }
    .md-search-form div[data-testid="stForm"] div[data-testid="stTextInput"] input {
        background: transparent !important;
        border: none !important;
        color: var(--md-text) !important;
        font: 500 16px/1 'Hanken Grotesk', sans-serif !important;
        padding: 0 !important;
        box-shadow: none !important;
        line-height: 1.2 !important;
        min-height: 24px !important;
    }
    .md-search-form div[data-testid="stForm"] div[data-testid="stTextInput"] label {
        display: none;
    }
    .md-search-form div[data-testid="stForm"] .stButton > button,
    .md-search-form div[data-testid="stForm"] [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #34E0A1, #1FB37D) !important;
        color: var(--md-ink) !important;
        border: none !important;
        border-radius: 11px !important;
        font: 700 14px/1 'Hanken Grotesk', sans-serif !important;
        padding: 13px 22px !important;
        white-space: nowrap !important;
        width: 100% !important;
        min-height: 44px !important;
    }
    .md-search-form div[data-testid="stForm"] input::placeholder {
        color: #6B6B78 !important;
        opacity: 1 !important;
    }

    .md-chip-row .stButton > button {
        background: transparent !important;
        color: #C9C9D2 !important;
        border: 1px solid rgba(255,255,255,.14) !important;
        border-radius: 999px !important;
        font: 500 13px/1 'Hanken Grotesk', sans-serif !important;
        padding: 8px 14px !important;
        width: auto !important;
        min-height: 0 !important;
    }
    .md-filter-row .stButton > button,
    .md-sort-row .stButton > button {
        border-radius: 999px !important;
        font: 600 12px/1 'Hanken Grotesk', sans-serif !important;
        padding: 7px 13px !important;
        width: auto !important;
        min-height: 0 !important;
        border: 1px solid rgba(255,255,255,.12) !important;
    }
    .md-back-row .stButton > button {
        background: transparent !important;
        color: var(--md-muted) !important;
        border: 1px solid rgba(255,255,255,.12) !important;
        border-radius: 13px !important;
        font: 600 14px/1 'Hanken Grotesk', sans-serif !important;
        padding: 14px !important;
        width: 100% !important;
    }

    @media (max-width: 768px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .md-title { font-size: 38px; }
        .md-subtitle { font-size: 15px; }
        .md-reco-card { flex-direction: column; align-items: flex-start; }
        .md-reco-avatar { width: 56px; height: 56px; font-size: 26px; }
    }
</style>
""",
        unsafe_allow_html=True,
    )
    inject_reco_card_bindings()

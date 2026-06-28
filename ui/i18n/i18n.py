from typing import Dict, List, Optional

import streamlit as st
import streamlit.components.v1 as components

from ui.i18n.locales import en as en_messages
from ui.i18n.locales import fr as fr_messages

SUPPORTED_LOCALES = {"fr", "en"}
DEFAULT_LOCALE = "fr"

SIMILARITY_KEYS = (
    "same_genre",
    "historical_influence",
    "creative_approach",
    "surprise_discovery",
)

LEGACY_SIMILARITY_MAP: Dict[str, str] = {
    "même genre": "same_genre",
    "influence historique": "historical_influence",
    "approche créative": "creative_approach",
    "découverte surprenante": "surprise_discovery",
    "same genre": "same_genre",
    "historical influence": "historical_influence",
    "creative approach": "creative_approach",
    "surprise discovery": "surprise_discovery",
}

_CATALOGS: Dict[str, Dict[str, str]] = {
    "fr": fr_messages.MESSAGES,
    "en": en_messages.MESSAGES,
}


def get_locale() -> str:
    locale = st.session_state.get("locale", DEFAULT_LOCALE)
    return locale if locale in SUPPORTED_LOCALES else DEFAULT_LOCALE


def set_locale(locale: str) -> None:
    if locale not in SUPPORTED_LOCALES:
        return
    previous = st.session_state.get("locale")
    st.session_state.locale = locale
    st.session_state._locale_user_set = True
    st.session_state._locale_detect_pending = False
    if previous and previous != locale:
        st.session_state._locale_switched = True


def init_locale() -> None:
    if "locale" not in st.session_state:
        st.session_state.locale = DEFAULT_LOCALE
    if "_locale_user_set" not in st.session_state:
        st.session_state._locale_user_set = False
    if "_locale_switched" not in st.session_state:
        st.session_state._locale_switched = False


def t(key: str, **kwargs) -> str:
    locale = get_locale()
    message = _CATALOGS.get(locale, {}).get(key) or _CATALOGS[DEFAULT_LOCALE].get(key, key)
    if kwargs:
        return message.format(**kwargs)
    return message


def loading_steps() -> List[str]:
    return [
        t("loading.step.spotify"),
        t("loading.step.fetch"),
        t("loading.step.ai"),
        t("loading.step.verify"),
    ]


def normalize_similarity_type(raw: Optional[str]) -> str:
    if not raw:
        return "same_genre"
    value = str(raw).strip()
    if value in SIMILARITY_KEYS:
        return value
    normalized = LEGACY_SIMILARITY_MAP.get(value.lower(), LEGACY_SIMILARITY_MAP.get(value))
    if normalized:
        return normalized
    lower = value.lower()
    for legacy, stable in LEGACY_SIMILARITY_MAP.items():
        if legacy.lower() == lower:
            return stable
    return "same_genre"


def similarity_label(similarity_type: str) -> str:
    key = normalize_similarity_type(similarity_type)
    return t(f"similarity.{key}")


def similarity_types() -> List[str]:
    return list(SIMILARITY_KEYS)


def render_locale_detector() -> None:
    if st.session_state.get("_locale_user_set"):
        return

    query_lang = st.query_params.get("lang")
    if isinstance(query_lang, list):
        query_lang = query_lang[0] if query_lang else None
    if query_lang in SUPPORTED_LOCALES:
        st.session_state.locale = query_lang
        return

    if st.session_state.get("_locale_detect_ran"):
        return

    st.session_state._locale_detect_ran = True
    components.html(
        """
<script>
(function () {
  const lang = (navigator.language || 'fr').toLowerCase().startsWith('en') ? 'en' : 'fr';
  const url = new URL(window.parent.location.href);
  if (!url.searchParams.get('lang')) {
    url.searchParams.set('lang', lang);
    window.parent.location.replace(url.toString());
  }
})();
</script>
        """,
        height=0,
    )


def clear_locale_switch_flag() -> None:
    st.session_state._locale_switched = False

def show_locale_switch_hint() -> None:
    if st.session_state.get("_locale_switched"):
        st.info(t("locale.new_search_hint"))

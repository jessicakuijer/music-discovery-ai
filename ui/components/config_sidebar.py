from dataclasses import dataclass

import streamlit as st

from services.spotify_service import initialize_spotify
from ui.components.lang_switch import render_lang_switch
from ui.i18n import t


def _key_effective(manual: str, from_file: str) -> str:
    return (manual or "").strip() or (from_file or "").strip()


@dataclass
class AppConfig:
    openai_api_key: str
    spotify_client_id: str
    spotify_client_secret: str
    youtube_api_key: str
    auto_mode: bool
    secrets_loaded: bool
    ready: bool


def render_config_sidebar() -> AppConfig:
    with st.sidebar:
        st.header(t("sidebar.configuration"))
        render_lang_switch(location="sidebar")
        st.markdown("---")

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
                st.success(t("sidebar.secrets_detected"))
            else:
                st.warning(t("sidebar.secrets_empty"))
        except Exception:
            st.warning(t("sidebar.no_secrets"))

        auto_mode = bool(
            secrets_loaded
            and default_openai
            and default_spotify_id
            and default_spotify_secret
        )

        if auto_mode:
            st.info(t("sidebar.auto_mode"))
            openai_api_key_in = ""
            spotify_client_id_in = ""
            spotify_client_secret_in = ""
            youtube_api_key_in = ""
            with st.expander(t("sidebar.override_expander"), expanded=False):
                st.caption(t("sidebar.override_caption"))
                openai_api_key_in = st.text_input(
                    t("sidebar.openai_key"),
                    value="",
                    type="password",
                    key="cfg_openai_override",
                    placeholder=t("sidebar.placeholder_secrets"),
                )
                spotify_client_id_in = st.text_input(
                    t("sidebar.spotify_id"),
                    value="",
                    type="password",
                    key="cfg_spotify_id_override",
                    placeholder=t("sidebar.placeholder_optional"),
                )
                spotify_client_secret_in = st.text_input(
                    t("sidebar.spotify_secret"),
                    value="",
                    type="password",
                    key="cfg_spotify_secret_override",
                    placeholder=t("sidebar.placeholder_optional"),
                )
                youtube_api_key_in = st.text_input(
                    t("sidebar.youtube_key"),
                    value="",
                    type="password",
                    key="cfg_youtube_override",
                    placeholder=t("sidebar.placeholder_optional"),
                )
        else:
            st.subheader(t("sidebar.api_keys"))
            if secrets_loaded:
                st.caption(t("sidebar.caption_secrets_partial"))
            else:
                st.caption(t("sidebar.caption_manual"))
            openai_api_key_in = st.text_input(
                t("sidebar.openai_key"),
                value="",
                type="password",
                key="cfg_openai_v2",
                placeholder=t("sidebar.placeholder_openai"),
            )
            spotify_client_id_in = st.text_input(
                t("sidebar.spotify_id"),
                value="",
                type="password",
                key="cfg_spotify_id_v2",
                placeholder=t("sidebar.placeholder_optional"),
            )
            spotify_client_secret_in = st.text_input(
                t("sidebar.spotify_secret"),
                value="",
                type="password",
                key="cfg_spotify_secret_v2",
                placeholder=t("sidebar.placeholder_optional"),
            )
            youtube_api_key_in = st.text_input(
                t("sidebar.youtube_key"),
                value="",
                type="password",
                key="cfg_youtube_v2",
                placeholder=t("sidebar.placeholder_optional"),
            )

        openai_api_key = _key_effective(openai_api_key_in, default_openai)
        spotify_client_id = _key_effective(spotify_client_id_in, default_spotify_id)
        spotify_client_secret = _key_effective(spotify_client_secret_in, default_spotify_secret)
        youtube_api_key = _key_effective(youtube_api_key_in, default_youtube_key)

        if spotify_client_id and spotify_client_secret and st.session_state.spotify_client is None:
            sc = initialize_spotify(spotify_client_id, spotify_client_secret, silent=True)
            if sc:
                st.session_state.spotify_client = sc

        if not auto_mode and spotify_client_id and spotify_client_secret:
            if st.button(t("sidebar.test_spotify")):
                with st.spinner(t("sidebar.testing_spotify")):
                    spotify_client = initialize_spotify(spotify_client_id, spotify_client_secret)
                    if spotify_client:
                        st.session_state.spotify_client = spotify_client
                        st.success(t("sidebar.spotify_ok"))
                    else:
                        st.error(t("errors.spotify_failed"))
        elif auto_mode and st.session_state.spotify_client:
            st.caption(t("sidebar.spotify_auto_ready"))

        st.markdown("---")
        st.subheader(t("sidebar.instructions"))
        if auto_mode:
            st.markdown(t("sidebar.instructions_auto"))
        else:
            st.markdown(t("sidebar.instructions_manual"))

        st.markdown(
            f"""
            <div class="md-sidebar-card">
                <h3 style="margin-top:0">{t("sidebar.accounts_title")}</h3>
                <p><strong>{t("sidebar.accounts_openai")}</strong> <a href="https://platform.openai.com" target="_blank">platform.openai.com</a></p>
                <p><strong>{t("sidebar.accounts_spotify")}</strong> <a href="https://developer.spotify.com/dashboard" target="_blank">developer.spotify.com/dashboard</a></p>
                <p><strong>{t("sidebar.accounts_youtube")}</strong> <a href="https://console.cloud.google.com" target="_blank">console.cloud.google.com</a> {t("sidebar.accounts_optional")}</p>
                <p><em>{t("sidebar.accounts_privacy")}</em></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    ready = bool(st.session_state.spotify_client and openai_api_key)
    return AppConfig(
        openai_api_key=openai_api_key,
        spotify_client_id=spotify_client_id,
        spotify_client_secret=spotify_client_secret,
        youtube_api_key=youtube_api_key,
        auto_mode=auto_mode,
        secrets_loaded=secrets_loaded,
        ready=ready,
    )

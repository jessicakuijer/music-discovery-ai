import streamlit as st

from services.openai_service import (
    call_openai_for_recommendations,
    create_analysis_prompt,
    verify_and_enrich_recommendations,
)
from services.spotify_service import get_artist_data
from ui.components.artist_profile import render_artist_profile
from ui.components.config_sidebar import AppConfig, render_config_sidebar
from ui.components.filters import filter_and_sort_artists, render_filters_and_sort
from ui.components.layout import (
    render_ambient_blobs,
    render_footer,
    render_hero,
    render_nav,
    render_no_result,
    render_setup_hint,
)
from ui.components.loading import render_loading
from ui.components.recommendation_card import render_recommendation_card
from ui.components.recommendation_detail import render_recommendation_detail
from ui.components.search import render_compact_search_bar, render_search
from ui.i18n import (
    clear_locale_switch_flag,
    get_locale,
    init_locale,
    normalize_similarity_type,
    render_locale_detector,
    show_locale_switch_hint,
    t,
)
from ui.theme import inject_global_css


def init_session_state() -> None:
    defaults = {
        "screen": "home",
        "query": "",
        "filter_type": "all",
        "sort_by": "confidence",
        "selected_rec_index": None,
        "loading_step": 0,
        "discovery_target": None,
        "recommendations_ready": False,
        "current_artist_data": None,
        "recommendations": {},
        "spotify_client": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    filter_type = st.session_state.get("filter_type", "all")
    if filter_type != "all":
        st.session_state.filter_type = normalize_similarity_type(filter_type)


def go_home() -> None:
    st.session_state.screen = "home"
    st.session_state.discovery_target = None
    st.session_state.selected_rec_index = None
    st.session_state.filter_type = "all"
    st.session_state.sort_by = "confidence"
    st.rerun()


def reset_discovery() -> None:
    st.session_state.recommendations_ready = False
    st.session_state.current_artist_data = None
    st.session_state.recommendations = {}
    st.session_state.selected_rec_index = None
    st.session_state.filter_type = "all"
    st.session_state.sort_by = "confidence"
    clear_locale_switch_flag()


def select_rec(idx: int) -> None:
    st.session_state.selected_rec_index = idx
    st.session_state.screen = "detail"
    st.rerun()


def start_discovery(artist_name: str) -> None:
    st.session_state.query = artist_name
    st.session_state.discovery_target = artist_name
    st.session_state.screen = "loading"
    st.session_state.loading_step = 0
    reset_discovery()
    st.rerun()


def run_discovery_pipeline(artist_name: str, config: AppConfig) -> None:
    load_placeholder = st.empty()

    def show_step(step: int) -> None:
        st.session_state.loading_step = step
        with load_placeholder.container():
            render_loading(artist_name=artist_name, step=step)

    show_step(0)

    show_step(1)
    artist_data = get_artist_data(st.session_state.spotify_client, artist_name)
    if not artist_data:
        st.session_state.screen = "no_result"
        st.session_state.discovery_target = None
        st.rerun()

    st.session_state.current_artist_data = artist_data

    show_step(2)
    analysis_prompt = create_analysis_prompt(artist_data, locale=get_locale())
    ia_response = call_openai_for_recommendations(analysis_prompt, config.openai_api_key)
    if not ia_response:
        st.session_state.screen = "no_result"
        st.session_state.discovery_target = None
        st.rerun()

    show_step(3)
    enriched_recs = verify_and_enrich_recommendations(
        st.session_state.spotify_client,
        ia_response["recommendations"],
        config.youtube_api_key,
    )

    st.session_state.recommendations = {
        "analysis": ia_response["analysis"],
        "artists": enriched_recs,
    }
    st.session_state.recommendations_ready = bool(enriched_recs)
    st.session_state.discovery_target = None
    st.session_state.screen = "results" if enriched_recs else "no_result"
    clear_locale_switch_flag()
    st.rerun()


def main() -> None:
    init_locale()

    st.set_page_config(
        page_title=t("meta.page_title"),
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    render_locale_detector()

    init_session_state()
    inject_global_css()
    config = render_config_sidebar()

    st.markdown('<div class="md-app-shell">', unsafe_allow_html=True)
    render_ambient_blobs()

    spotify_connected = st.session_state.spotify_client is not None
    screen = st.session_state.screen

    if screen == "loading" and st.session_state.discovery_target:
        render_nav(spotify_connected=spotify_connected)
        run_discovery_pipeline(st.session_state.discovery_target, config)
        st.markdown("</div>", unsafe_allow_html=True)
        render_footer()
        return

    if screen == "home":
        render_nav(spotify_connected=spotify_connected)
        render_hero(show_full=True)
        if config.ready:
            render_search(
                spotify_client=st.session_state.spotify_client,
                ready=True,
                on_discover=start_discovery,
            )
        else:
            render_setup_hint()

    elif screen == "no_result":
        render_nav(spotify_connected=spotify_connected)
        render_no_result(
            st.session_state.get("query", ""),
            on_example=start_discovery,
            on_home=go_home,
        )

    elif screen == "results" and st.session_state.recommendations_ready:
        artist_info = st.session_state.current_artist_data["info"]
        render_nav(spotify_connected=spotify_connected, compact=False)
        render_compact_search_bar(artist_info["name"], on_home=go_home)
        show_locale_switch_hint()

        recommendations = st.session_state.recommendations
        render_artist_profile(
            st.session_state.current_artist_data,
            recommendations.get("analysis", ""),
        )

        artists = recommendations.get("artists", [])
        filter_type, sort_by = render_filters_and_sort(artists)
        filtered = filter_and_sort_artists(artists, filter_type, sort_by)

        for display_rank, rec in enumerate(filtered, 1):
            original_index = artists.index(rec)
            render_recommendation_card(
                rec,
                rank=display_rank,
                index=original_index,
                on_select=select_rec,
            )

        if st.button(t("results.new_search"), key="new_search"):
            reset_discovery()
            go_home()

    elif screen == "detail" and st.session_state.recommendations_ready:
        artists = st.session_state.recommendations.get("artists", [])
        idx = st.session_state.selected_rec_index
        if idx is None or idx >= len(artists):
            st.session_state.screen = "results"
            st.rerun()

        rec = artists[idx]
        render_nav(spotify_connected=spotify_connected, compact=True)
        show_locale_switch_hint()

        def back_to_results() -> None:
            st.session_state.screen = "results"
            st.session_state.selected_rec_index = None
            st.rerun()

        render_recommendation_detail(
            rec,
            rank=idx + 1,
            total=len(artists),
            on_back=back_to_results,
            youtube_api_configured=bool(config.youtube_api_key),
        )

    else:
        st.session_state.screen = "home"
        render_nav(spotify_connected=spotify_connected)
        render_hero(show_full=True)
        if config.ready:
            render_search(
                spotify_client=st.session_state.spotify_client,
                ready=True,
                on_discover=start_discovery,
            )
        else:
            render_setup_hint()

    st.markdown("</div>", unsafe_allow_html=True)
    render_footer()


if __name__ == "__main__":
    main()

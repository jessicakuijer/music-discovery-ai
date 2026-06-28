from typing import Callable, List

import streamlit as st

from services.spotify_service import search_artist_suggestions
from ui.i18n import t
from ui.theme import EXAMPLE_ARTISTS, esc


def render_search(
    *,
    spotify_client,
    ready: bool,
    on_discover: Callable[[str], None],
) -> None:
    if not ready:
        return

    query_value = st.session_state.get("query", "")
    active = bool(query_value.strip())
    border = "#34E0A1" if active else "rgba(255,255,255,.10)"
    shadow = (
        "0 0 0 4px #34E0A11F, 0 14px 44px rgba(0,0,0,.45)"
        if active
        else "0 14px 44px rgba(0,0,0,.45)"
    )

    st.markdown(
        f"""
        <style>
        .md-search-form div[data-testid="stForm"] {{
            background: #14141B;
            border: 1.5px solid {border};
            border-radius: 16px;
            padding: 8px 8px 8px 16px;
            box-shadow: {shadow};
            margin-top: 32px;
            max-width: 620px;
        }}
        .md-search-form div[data-testid="stForm"] [data-testid="stHorizontalBlock"] {{
            align-items: center;
            gap: 0.4rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="md-search-form">', unsafe_allow_html=True)
    with st.form("md_search_form", clear_on_submit=False, border=False):
        col_input, col_btn = st.columns([4.8, 1.2], vertical_alignment="center")
        with col_input:
            query = st.text_input(
                t("search.label"),
                value=query_value,
                placeholder=t("search.placeholder"),
                label_visibility="collapsed",
                key="md_artist_query",
            )
        with col_btn:
            submitted = st.form_submit_button(t("search.discover"), type="primary")
    st.markdown("</div>", unsafe_allow_html=True)

    if query != st.session_state.get("query"):
        st.session_state.query = query

    suggestions: List[dict] = []
    if spotify_client and st.session_state.get("query", "").strip():
        suggestions = search_artist_suggestions(
            spotify_client, st.session_state.query, limit=5
        )

    if suggestions and st.session_state.get("query", "").strip():
        _render_suggestions(suggestions, on_discover)

    st.markdown(
        f'<p style="font:400 13px/1 \'Hanken Grotesk\';color:#6B6B78;margin:22px 0 10px">{esc(t("search.try"))}</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="md-chip-row">', unsafe_allow_html=True)
    chip_cols = st.columns(len(EXAMPLE_ARTISTS))
    for col, name in zip(chip_cols, EXAMPLE_ARTISTS):
        with col:
            if st.button(name, key=f"example_{name}"):
                st.session_state.query = name
                on_discover(name)
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted and st.session_state.get("query", "").strip():
        on_discover(st.session_state.query.strip())


def _render_suggestions(suggestions: List[dict], on_discover: Callable[[str], None]) -> None:
    st.markdown(
        f"""
        <div style="font:700 10px/1 'Space Mono';letter-spacing:0.14em;text-transform:uppercase;
            color:#6B6B78;margin:12px 0 6px;max-width:620px">{esc(t("search.suggestions"))}</div>
        """,
        unsafe_allow_html=True,
    )
    for i, s in enumerate(suggestions):
        badge = (
            f'<span style="font:700 9px/1 \'Space Mono\';letter-spacing:0.08em;text-transform:uppercase;'
            f'color:#34E0A1;background:#34E0A11F;border-radius:999px;padding:5px 9px">{esc(t("search.popular"))}</span>'
            if s.get("hot")
            else ""
        )
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:13px;padding:12px 16px;max-width:620px;
                background:#14141B;border:1px solid rgba(255,255,255,.10);border-radius:14px;margin-bottom:6px">
                <div style="width:38px;height:38px;border-radius:10px;background:linear-gradient(140deg,#9D8CFF,#352a7d);
                    display:flex;align-items:center;justify-content:center;font:800 16px/1 'Bricolage Grotesque';color:#fff;flex:none">
                    {esc(s['initial'])}
                </div>
                <div style="flex:1;min-width:0">
                    <div style="font:600 15px/1.2 'Hanken Grotesk'">{esc(s['name'])}</div>
                    <div style="font:400 11px/1 'Space Mono';color:#6B6B78;margin-top:4px">{esc(s['meta'])}</div>
                </div>
                {badge}
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(t("search.analyze", name=s["name"]), key=f"suggest_{i}_{s['name']}"):
            st.session_state.query = s["name"]
            on_discover(s["name"])


def render_compact_search_bar(artist_name: str, on_home: Callable[[], None]) -> None:
    col_back, col_search = st.columns([1, 6])
    with col_back:
        if st.button(t("nav.home"), key="nav_home"):
            on_home()
    with col_search:
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:9px;background:#14141B;
                border:1px solid rgba(255,255,255,.10);border-radius:11px;padding:9px 14px">
                <div style="width:14px;height:14px;border:2px solid #6B6B78;border-radius:50%;position:relative;flex:none">
                    <div style="position:absolute;width:5px;height:2px;background:#6B6B78;transform:rotate(45deg);right:-4px;bottom:1px"></div>
                </div>
                <span style="font:500 14px/1 'Hanken Grotesk';white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
                    {esc(artist_name)}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

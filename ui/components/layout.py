from typing import Callable

import streamlit as st

from ui.components.lang_switch import render_lang_switch
from ui.i18n import t
from ui.theme import EXAMPLE_ARTISTS, esc, render_html


def render_nav(*, spotify_connected: bool, compact: bool = False) -> None:
    logo_text = t("nav.logo_compact") if compact else t("nav.logo")
    nav_cols = st.columns([3, 1, 1])
    with nav_cols[0]:
        render_html(
            f"""
<div class="md-nav" style="margin-bottom:0">
    <div class="md-logo">
        <div class="md-logo-icon"></div>
        <div class="md-logo-text">{esc(logo_text)}</div>
    </div>
</div>
"""
        )
    with nav_cols[1]:
        render_lang_switch(location="nav")
    with nav_cols[2]:
        if spotify_connected:
            render_html(
                f"""
<div class="md-spotify-badge" style="justify-content:flex-end;margin-top:6px">
    <span class="md-spotify-dot"></span>{esc(t("nav.spotify_connected"))}
</div>
"""
            )


def render_ambient_blobs() -> None:
    render_html(
        """
<div class="md-blob md-blob-purple"></div>
<div class="md-blob md-blob-pink"></div>
<div class="md-blob md-blob-green"></div>
"""
    )


def render_hero(*, show_full: bool = True) -> None:
    if show_full:
        render_html(
            f"""
<div class="md-hero">
    <div class="md-kicker">{esc(t("home.kicker"))}</div>
    <h1 class="md-title">
        {esc(t("home.title_prefix"))}
        <span class="md-title-gradient">{esc(t("home.title_highlight"))}</span>.
    </h1>
    <p class="md-subtitle">{esc(t("home.subtitle"))}</p>
</div>
"""
        )
    else:
        render_html(
            f"""
<div class="md-hero" style="text-align:center;margin-bottom:8px">
    <div class="md-kicker">{esc(t("home.kicker"))}</div>
    <h2 class="md-title" style="font-size:42px;margin-top:14px">{esc(t("home.title_compact"))}</h2>
</div>
"""
        )


def render_footer() -> None:
    render_html(
        f"""
<div class="md-footer">
    <p><strong>{esc(t("meta.page_title"))}</strong> — {esc(t("footer.powered"))}</p>
    <p>{esc(t("footer.privacy"))}</p>
</div>
"""
    )


def render_setup_hint() -> None:
    render_html(
        f"""
<div class="md-card" style="padding:24px;margin-top:24px">
    <div class="md-kicker" style="margin-bottom:12px">{esc(t("setup.title"))}</div>
    <p class="md-subtitle" style="max-width:none">{esc(t("setup.text"))}</p>
</div>
"""
    )


def render_no_result(query: str, on_example: Callable[[str], None], on_home: Callable[[], None]) -> None:
    render_html(
        f"""
<div style="min-height:360px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 20px">
    <div class="md-empty-icon">∅</div>
    <div class="md-empty-title">{esc(t("no_result.title", query=query))}</div>
    <div class="md-empty-text">{esc(t("no_result.text"))}</div>
</div>
"""
    )
    render_html('<div class="md-chip-row" style="display:flex;justify-content:center;gap:10px">')
    cols = st.columns(min(len(EXAMPLE_ARTISTS), 4))
    for col, name in zip(cols, EXAMPLE_ARTISTS[:4]):
        with col:
            if st.button(name, key=f"noresult_{name}"):
                on_example(name)
    render_html("</div>")
    if st.button(t("no_result.home"), key="noresult_home"):
        on_home()

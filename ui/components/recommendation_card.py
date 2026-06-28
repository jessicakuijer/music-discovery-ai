from typing import Callable

import streamlit as st

from ui.i18n import similarity_label, t
from ui.theme import esc, render_html, similarity_style


def render_recommendation_card(
    rec: dict,
    rank: int,
    index: int,
    on_select: Callable[[int], None],
) -> None:
    style = similarity_style(rec.get("similarity_type", ""))
    name = rec["name"]
    initial = name[0].upper() if name else "?"
    sim_label = similarity_label(rec.get("similarity_type", ""))
    confidence = rec.get("confidence", 0)
    image_url = rec.get("spotify_data", {}).get("image")

    if image_url:
        avatar_inner = f'<img src="{esc(image_url)}" alt="{esc(name)}" style="width:100%;height:100%;object-fit:cover;border-radius:14px">'
    else:
        avatar_inner = esc(initial)

    card_html = f"""
<div data-reco-shell="{index}">
    <div class="md-reco-card">
        <div class="md-reco-accent" style="background:{style['accent']}"></div>
        <div class="md-reco-avatar" style="background:{style['tile']}">
            <span class="md-reco-rank">{rank:02d}</span>
            {avatar_inner}
        </div>
        <div style="flex:1;min-width:0">
            <span class="md-badge" style="color:{style['accent']};background:{style['soft']};border:1px solid {style['ring']}">
                {esc(sim_label)}
            </span>
            <div style="font:800 22px/1.05 'Bricolage Grotesque';margin-top:9px">{esc(name)}</div>
            <div style="font:400 14px/1.45 'Hanken Grotesk';color:#B7B7C2;margin-top:6px">{esc(rec.get('reason', ''))}</div>
            <div style="display:flex;align-items:center;gap:11px;margin-top:12px;max-width:300px">
                <div style="font:700 9px/1 'Space Mono';text-transform:uppercase;letter-spacing:0.09em;color:#6B6B78">{esc(t("results.conf_short"))}</div>
                <div class="md-conf-bar"><div class="md-conf-fill" style="width:{confidence}%;background:{style['accent']}"></div></div>
                <div style="font:700 11px/1 'Space Mono';color:{style['accent']}">{confidence}%</div>
            </div>
        </div>
        <div style="font:400 20px/1 'Hanken Grotesk';color:#6B6B78;flex:none">→</div>
    </div>
</div>
"""

    with st.container():
        render_html(card_html)
        st.button(
            " ",
            key=f"reco_open_{index}",
            on_click=on_select,
            kwargs={"idx": index},
            help=t("results.view_artist", name=name),
            use_container_width=True,
            type="secondary",
        )

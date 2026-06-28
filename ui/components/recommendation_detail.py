import streamlit as st

from services.spotify_service import format_followers
from ui.components.embeds import render_youtube_embed
from ui.i18n import similarity_label, t
from ui.theme import esc, render_html, similarity_style


def render_recommendation_detail(
    rec: dict,
    *,
    rank: int,
    total: int,
    on_back,
    youtube_api_configured: bool = False,
) -> None:
    style = similarity_style(rec.get("similarity_type", ""))
    name = rec["name"]
    initial = name[0].upper() if name else "?"
    spotify_data = rec.get("spotify_data", {})
    genres = " · ".join(spotify_data.get("genres", [])[:4]) or t("results.varied")
    confidence = rec.get("confidence", 0)
    popularity = spotify_data.get("popularity", 0)
    spotify_url = spotify_data.get("external_urls", {}).get("spotify", "")
    top_tracks = spotify_data.get("top_tracks", [])
    youtube_url = spotify_data.get("youtube_url")
    image_url = spotify_data.get("image")
    sim_label = similarity_label(rec.get("similarity_type", ""))

    if image_url:
        hero_avatar = (
            f'<img src="{esc(image_url)}" alt="{esc(name)}" '
            'style="width:124px;height:124px;border-radius:22px;object-fit:cover;flex:none;'
            'box-shadow:0 18px 44px rgba(0,0,0,.4)">'
        )
    else:
        hero_avatar = (
            f'<div style="width:124px;height:124px;border-radius:22px;background:{style["tile"]};'
            "display:flex;align-items:center;justify-content:center;"
            f"font:800 56px/1 'Bricolage Grotesque';color:#fff;flex:none;"
            f'box-shadow:0 18px 44px rgba(0,0,0,.4)">{esc(initial)}</div>'
        )

    render_html(
        f"""
<div style="position:relative;overflow:hidden;padding-bottom:14px;margin-bottom:8px">
    <div style="position:absolute;inset:0;background:{style['tile']};opacity:.16"></div>
    <div style="position:absolute;width:340px;height:340px;border-radius:50%;background:{style['glow']};
        filter:blur(50px);opacity:.3;top:-120px;right:-40px"></div>
    <div style="position:relative;display:flex;align-items:center;justify-content:space-between;
        font:600 13px/1 'Hanken Grotesk';color:#C9C9D2;margin-bottom:16px">
        <span>{rank:02d} / {total:02d}</span>
    </div>
    <div style="position:relative;display:flex;gap:22px;align-items:flex-end;flex-wrap:wrap">
        {hero_avatar}
        <div style="flex:1;min-width:220px">
            <span class="md-badge" style="color:{style['accent']};background:{style['soft']};border:1px solid {style['ring']}">
                {esc(sim_label)}
            </span>
            <div style="font:800 44px/1 'Bricolage Grotesque';letter-spacing:-0.03em;margin-top:13px">{esc(name)}</div>
            <div style="font:400 12px/1 'Space Mono';color:#9A9AA8;margin-top:11px">{esc(genres)}</div>
        </div>
    </div>
</div>
"""
    )

    if spotify_url:
        st.link_button(t("detail.listen_spotify"), spotify_url, use_container_width=False)

    render_html(
        f"""
<div class="md-card" style="padding:18px 20px;margin-top:16px;border-color:{style['ring']}">
    <div style="font:700 10px/1 'Space Mono';letter-spacing:0.14em;text-transform:uppercase;color:#9A9AA8">
        {esc(t("detail.why_reco"))}
    </div>
    <div style="font:500 16px/1.55 'Hanken Grotesk';color:#E6E6EC;margin-top:10px">{esc(rec.get('reason', ''))}</div>
</div>
"""
    )

    if youtube_url:
        top_name = top_tracks[0]["name"] if top_tracks else t("detail.top_track_fallback")
        render_html(
            f'<div style="font:700 10px/1 \'Space Mono\';letter-spacing:0.14em;text-transform:uppercase;'
            f'color:#6B6B78;margin:24px 0 11px">{esc(t("detail.video_youtube"))}</div>'
        )
        render_youtube_embed(youtube_url, f"{name} — {top_name}")
    elif youtube_api_configured:
        render_html(
            f'<div style="font:400 13px/1 \'Hanken Grotesk\';color:#6B6B78;margin:20px 0 0">'
            f"{esc(t('detail.video_not_found'))}</div>"
        )

    render_html(
        f"""
<div style="display:flex;gap:12px;margin-top:18px">
    <div style="flex:1;background:#14141B;border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:15px">
        <div style="font:800 26px/1 'Bricolage Grotesque';color:{style['accent']}">{confidence}%</div>
        <div style="font:400 10px/1 'Space Mono';color:#6B6B78;margin-top:6px;text-transform:uppercase;letter-spacing:0.08em">{esc(t("detail.confidence"))}</div>
    </div>
    <div style="flex:1;background:#14141B;border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:15px">
        <div style="font:800 26px/1 'Bricolage Grotesque'">{popularity}<span style="font:400 12px/1 'Space Mono';color:#6B6B78">/100</span></div>
        <div style="font:400 10px/1 'Space Mono';color:#6B6B78;margin-top:6px;text-transform:uppercase;letter-spacing:0.08em">{esc(t("results.popularity"))}</div>
    </div>
    <div style="flex:1;background:#14141B;border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:15px">
        <div style="font:800 26px/1 'Bricolage Grotesque'">{esc(format_followers(spotify_data.get('followers', 0)))}</div>
        <div style="font:400 10px/1 'Space Mono';color:#6B6B78;margin-top:6px;text-transform:uppercase;letter-spacing:0.08em">{esc(t("results.followers"))}</div>
    </div>
</div>
"""
    )

    if top_tracks:
        render_html(
            f'<div style="font:700 10px/1 \'Space Mono\';letter-spacing:0.14em;text-transform:uppercase;'
            f'color:#6B6B78;margin:24px 0 10px">{esc(t("detail.top_tracks"))}</div>'
        )
        tracks_html = ""
        for i, track in enumerate(top_tracks, 1):
            track_url = track.get("external_urls", {}).get("spotify", "")
            row_inner = f"""
<div class="md-track-row">
    <div class="md-track-index">{i}</div>
    <div class="md-track-play" style="background:{style['tile']}">▶</div>
    <div class="md-track-meta">
        <div class="md-track-name">{esc(track['name'])}</div>
        <div class="md-track-album">{esc(track['album']['name'])}</div>
    </div>
    <div class="md-track-arrow">↗</div>
</div>
"""
            if track_url:
                tracks_html += (
                    f'<a href="{esc(track_url)}" target="_blank" rel="noopener noreferrer" '
                    f'class="md-track-row-link" aria-label="{esc(track["name"])}">'
                    f"{row_inner}</a>"
                )
            else:
                tracks_html += row_inner
        render_html(f'<div class="md-card md-track-list">{tracks_html}</div>')

    render_html('<div class="md-back-row">')
    if st.button(t("detail.back"), key="detail_back"):
        on_back()
    render_html("</div>")

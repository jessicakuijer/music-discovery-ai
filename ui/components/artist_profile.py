from services.spotify_service import format_followers
from ui.i18n import t
from ui.theme import esc, render_html


def render_artist_profile(artist_data: dict, analysis: str) -> None:
    artist_info = artist_data["info"]
    name = artist_info["name"]
    initial = name[0].upper() if name else "?"
    genres = " · ".join(artist_data["genres"][:4]) or t("results.unspecified")
    followers = format_followers(artist_data["followers"])
    popularity = artist_data["popularity"]
    image_url = artist_info["images"][0]["url"] if artist_info.get("images") else None

    if image_url:
        avatar_html = (
            f'<img src="{esc(image_url)}" alt="{esc(name)}" '
            'style="width:108px;height:108px;border-radius:20px;object-fit:cover;flex:none;'
            'box-shadow:0 16px 40px rgba(139,124,255,.3)">'
        )
    else:
        avatar_html = (
            f'<div style="width:108px;height:108px;border-radius:20px;'
            "background:linear-gradient(140deg,#34E0A1,#8B7CFF 52%,#FF6B8B 90%);"
            "display:flex;align-items:center;justify-content:center;"
            f"font:800 48px/1 'Bricolage Grotesque';color:#fff;flex:none;"
            f'box-shadow:0 16px 40px rgba(139,124,255,.3)">{esc(initial)}</div>'
        )

    render_html(
        f"""
<div style="display:flex;gap:22px;align-items:center;flex-wrap:wrap;margin-bottom:8px">
    {avatar_html}
    <div style="flex:1;min-width:200px">
        <div style="font:700 11px/1 'Space Mono';letter-spacing:0.16em;text-transform:uppercase;color:#6B6B78">
            {esc(t("results.analyzed_artist"))}
        </div>
        <div style="font:800 34px/1 'Bricolage Grotesque';letter-spacing:-0.02em;margin-top:7px">{esc(name)}</div>
        <div style="font:400 12px/1 'Space Mono';color:#9A9AA8;margin-top:10px">{esc(genres)}</div>
        <div style="display:flex;gap:26px;margin-top:16px;flex-wrap:wrap">
            <div>
                <span style="font:800 22px/1 'Bricolage Grotesque'">{esc(followers)}</span>
                <div style="font:400 10px/1 'Space Mono';color:#6B6B78;margin-top:5px;text-transform:uppercase;letter-spacing:0.1em">{esc(t("results.followers"))}</div>
            </div>
            <div>
                <span style="font:800 22px/1 'Bricolage Grotesque'">{popularity}<span style="font:400 12px/1 'Space Mono';color:#6B6B78">/100</span></span>
                <div style="font:400 10px/1 'Space Mono';color:#6B6B78;margin-top:5px;text-transform:uppercase;letter-spacing:0.1em">{esc(t("results.popularity"))}</div>
            </div>
        </div>
    </div>
</div>
<div class="md-analysis">
    <div class="md-analysis-label">{esc(t("results.analysis_label"))}</div>
    <div class="md-analysis-text">{esc(analysis)}</div>
</div>
"""
    )

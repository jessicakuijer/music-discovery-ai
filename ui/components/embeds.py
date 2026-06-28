import streamlit.components.v1 as components

from services.youtube_service import get_youtube_embed_url
from ui.i18n import t
from ui.theme import esc, render_html


def render_youtube_embed(youtube_url: str, title: str = "") -> None:
    embed_url = get_youtube_embed_url(youtube_url)
    if not embed_url:
        return

    components.iframe(
        embed_url,
        height=360,
        scrolling=False,
    )

    render_html(
        f'<p style="margin-top:8px;font:400 12px/1 \'Space Mono\';color:#6B6B78">'
        f'<a href="{esc(youtube_url)}" target="_blank" rel="noopener noreferrer" '
        f'style="color:#9A9AA8;text-decoration:none">{esc(t("detail.open_youtube"))}</a></p>'
    )

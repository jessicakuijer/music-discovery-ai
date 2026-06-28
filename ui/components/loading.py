from ui.i18n import loading_steps, t
from ui.theme import esc, render_html


def render_loading(*, artist_name: str, step: int) -> None:
    steps = loading_steps()
    steps_html = ""
    for i, label in enumerate(steps):
        done = step > i
        active = step == i
        color = "#F4F4F6" if done or active else "#5a5a66"
        mark = "✓" if done else str(i + 1)
        if done:
            dot_bg = "#34E0A1"
            dot_color = "#0B0B10"
            anim = ""
        elif active:
            dot_bg = "#8B7CFF"
            dot_color = "#0B0B10"
            anim = "animation:mdpulse 1s ease infinite;"
        else:
            dot_bg = "#1C1C26"
            dot_color = "#6B6B78"
            anim = ""
        steps_html += f"""
        <div class="md-step" style="color:{color}">
            <span class="md-step-dot" style="background:{dot_bg};color:{dot_color};{anim}">{mark}</span>
            {esc(label)}
        </div>
        """

    render_html(
        f"""
<div class="md-loading-wrap">
    <div class="md-blob md-blob-purple" style="opacity:.28;width:380px;height:380px;top:50%;left:50%;transform:translate(-50%,-50%)"></div>
    <div class="md-spinner">
        <div class="md-spinner-ring"></div>
        <div class="md-spinner-active"></div>
    </div>
    <div style="font:800 24px/1.2 'Bricolage Grotesque';margin-top:26px">
        {esc(t("loading.exploring"))}<br>
        <span class="md-title-gradient">{esc(artist_name)}</span>
    </div>
    <div style="margin-top:28px;text-align:left">{steps_html}</div>
</div>
"""
    )

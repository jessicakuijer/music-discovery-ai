import streamlit as st

from ui.i18n import normalize_similarity_type, similarity_label, similarity_types, t
from ui.theme import SIMILARITY_ACCENTS, esc


def _normalize_filter_type(filter_type: str) -> str:
    if filter_type == "all":
        return "all"
    return normalize_similarity_type(filter_type)


def render_filters_and_sort(artists: list) -> tuple[str, str]:
    filter_type = _normalize_filter_type(st.session_state.get("filter_type", "all"))
    st.session_state.filter_type = filter_type
    sort_by = st.session_state.get("sort_by", "confidence")

    type_meta = [("all", t("filters.all"), "#F4F4F6")]
    for key in similarity_types():
        type_meta.append((key, similarity_label(key), SIMILARITY_ACCENTS[key]))

    st.markdown(
        f"""
        <div style="display:flex;align-items:center;justify-content:space-between;margin-top:30px;flex-wrap:wrap;gap:14px">
            <div style="font:800 22px/1 'Bricolage Grotesque'">{esc(t("results.discoveries_count", n=len(artists)))}</div>
            <div style="display:flex;align-items:center;gap:8px;font:600 12px/1 'Hanken Grotesk';color:#6B6B78">
                {esc(t("results.sort"))}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="md-sort-row">', unsafe_allow_html=True)
    sort_cols = st.columns([1, 1, 4])
    with sort_cols[0]:
        if st.button(
            t("results.sort_confidence"),
            key="sort_confidence",
            type="primary" if sort_by == "confidence" else "secondary",
        ):
            st.session_state.sort_by = "confidence"
            sort_by = "confidence"
    with sort_cols[1]:
        if st.button(
            t("results.sort_popularity"),
            key="sort_popularity",
            type="primary" if sort_by == "popularity" else "secondary",
        ):
            st.session_state.sort_by = "popularity"
            sort_by = "popularity"
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="md-filter-row">', unsafe_allow_html=True)
    chip_cols = st.columns(len(type_meta))
    for col, (key, label, accent) in zip(chip_cols, type_meta):
        if key == "all":
            count = len(artists)
        else:
            count = sum(
                1 for a in artists if normalize_similarity_type(a.get("similarity_type")) == key
            )
        with col:
            if st.button(
                f"{label} · {count}",
                key=f"filter_{key}",
                type="primary" if filter_type == key else "secondary",
            ):
                st.session_state.filter_type = key
                filter_type = key
    st.markdown("</div>", unsafe_allow_html=True)

    return filter_type, sort_by


def filter_and_sort_artists(artists: list, filter_type: str, sort_by: str) -> list:
    filtered = artists
    if filter_type != "all":
        stable_filter = normalize_similarity_type(filter_type)
        filtered = [
            a for a in artists if normalize_similarity_type(a.get("similarity_type")) == stable_filter
        ]

    if sort_by == "popularity":
        return sorted(
            filtered,
            key=lambda a: a.get("spotify_data", {}).get("popularity", 0),
            reverse=True,
        )
    return sorted(filtered, key=lambda a: a.get("confidence", 0), reverse=True)

import streamlit as st

from ui.i18n import get_locale, set_locale, t


def render_lang_switch(*, location: str = "nav") -> None:
    locale = get_locale()
    prefix = f"lang_{location}"
    col_fr, col_en = st.columns(2)

    with col_fr:
        if st.button(
            "FR",
            key=f"{prefix}_fr",
            type="primary" if locale == "fr" else "secondary",
            use_container_width=True,
        ):
            if locale != "fr":
                set_locale("fr")
                st.rerun()

    with col_en:
        if st.button(
            "EN",
            key=f"{prefix}_en",
            type="primary" if locale == "en" else "secondary",
            use_container_width=True,
        ):
            if locale != "en":
                set_locale("en")
                st.rerun()

    if location == "sidebar":
        st.caption(t("lang.label"))

from pathlib import Path

import streamlit as st


def load_theme() -> None:
    style_path = Path(__file__).resolve().parents[1] / "assets" / "style.css"

    if style_path.exists():
        st.markdown(
            f"<style>{style_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def page_header(title: str, subtitle: str, eyebrow: str = "Executive workspace") -> None:
    st.markdown(
        f"""
        <div class="page-hero">
            <div class="eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p class="page-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def theme_plotly(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0f172a", family="Inter, Segoe UI, Arial, sans-serif"),
        title=dict(font=dict(color="#0f172a")),
        colorway=["#2563eb", "#38bdf8", "#0ea5e9", "#60a5fa", "#1d4ed8", "#93c5fd"],
        margin=dict(l=10, r=10, t=70, b=10),
        legend=dict(bgcolor="rgba(255,255,255,0.7)", bordercolor="rgba(148, 163, 184, 0.2)"),
    )
    fig.update_xaxes(gridcolor="rgba(148, 163, 184, 0.22)", zeroline=False, linecolor="rgba(37, 99, 235, 0.35)")
    fig.update_yaxes(gridcolor="rgba(148, 163, 184, 0.22)", zeroline=False, linecolor="rgba(37, 99, 235, 0.35)")
    return fig
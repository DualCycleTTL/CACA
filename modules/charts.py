"""
Modul Visualisasi & Tema Grafik Glassmorphism
Terminal Teluk Lamong - Pelindo

Menyediakan utilitas styling transparansi glassmorphism maritim untuk Plotly Charts,
serta grafik-grafik siap pakai untuk dashboard CACA.
"""

import pandas as pd
import plotly.express as px

URUTAN_HARI_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
URUTAN_SHIFT = ["Shift 1 (00:00-08:00)", "Shift 2 (08:00-16:00)", "Shift 3 (16:00-24:00)"]


def apply_glass_theme(fig, title: str = None, *args, **kwargs):
    """
    Menerapkan layout tema transparent glassmorphism maritim pada objek Plotly Figure
    dengan tipografi Plus Jakarta Sans dan warna kontras tinggi.
    """
    default_margin = dict(t=56, b=30, l=40, r=20)
    if fig.layout.margin:
        for k in ['t', 'b', 'l', 'r']:
            val = getattr(fig.layout.margin, k, None)
            if val is not None:
                default_margin[k] = val
    margin = kwargs.get("margin")
    if margin:
        default_margin.update(margin)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, -apple-system, sans-serif", color="#e2e8f0"),
        title=dict(
            text=title or (fig.layout.title.text if fig.layout.title else ""),
            font=dict(size=14, color="#ffffff", family="Plus Jakarta Sans, sans-serif"),
            y=0.98,
            x=0.01,
            xanchor="left",
            yanchor="top",
        ),
        margin=default_margin,
        legend=dict(
            bgcolor="rgba(13, 22, 38, 0.85)",
            bordercolor="rgba(255, 255, 255, 0.12)",
            borderwidth=1,
            font=dict(size=11, family="Plus Jakarta Sans, sans-serif", color="#e2e8f0"),
        ),
        hoverlabel=dict(
            bgcolor="rgba(11, 19, 32, 0.96)",
            font_size=12,
            font_family="Plus Jakarta Sans, sans-serif",
            font_color="#ffffff",
            bordercolor="rgba(56, 189, 248, 0.5)",
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(255, 255, 255, 0.08)",
        zerolinecolor="rgba(255, 255, 255, 0.12)",
        linecolor="rgba(255, 255, 255, 0.18)",
        tickfont=dict(color="#94a3b8"),
        title_font=dict(color="#cbd5e1"),
    )
    fig.update_yaxes(
        gridcolor="rgba(255, 255, 255, 0.08)",
        zerolinecolor="rgba(255, 255, 255, 0.12)",
        linecolor="rgba(255, 255, 255, 0.18)",
        tickfont=dict(color="#94a3b8"),
        title_font=dict(color="#cbd5e1"),
    )
    return fig


def chart_hari_shift_bar(events: pd.DataFrame, title: str = "Produktivitas per Hari & Shift"):
    """
    Grafik pengganti heatmap untuk visualisasi produktivitas per Hari & Shift:
    grouped bar chart (Hari di sumbu-X, Shift sbg warna terpisah). Lebih mudah
    dibaca dibanding heatmap karena nilai antar shift bisa dibandingkan langsung
    tanpa perlu menerka gradasi warna.

    Membutuhkan `events` yang sudah punya kolom HARI & SHIFT
    (lihat `calculations.tambah_kolom_hari_shift`).
    """
    agg = events.groupby(["HARI", "SHIFT"], observed=True).size().reset_index(name="Jumlah Event")
    agg["HARI"] = pd.Categorical(agg["HARI"], categories=URUTAN_HARI_ID, ordered=True)
    agg["SHIFT"] = pd.Categorical(agg["SHIFT"], categories=URUTAN_SHIFT, ordered=True)
    agg = agg.sort_values(["HARI", "SHIFT"])

    fig = px.bar(
        agg,
        x="HARI",
        y="Jumlah Event",
        color="SHIFT",
        barmode="group",
        title=title,
        color_discrete_sequence=["#38bdf8", "#0284C7", "#075985"],
        text="Jumlah Event",
    )
    fig.update_traces(marker=dict(line=dict(color="#ffffff", width=1)), textposition="outside")
    apply_glass_theme(fig)
    fig.update_layout(xaxis=dict(title=""), yaxis=dict(title="Jumlah Event"))
    return fig


def chart_hari_shift_line(events: pd.DataFrame, title: str = "Tren Produktivitas per Hari & Shift"):
    """
    Alternatif lain (selain grouped bar) untuk visualisasi Hari & Shift:
    line chart dgn satu garis per shift, sumbu-X hari. Cocok kalau ingin
    menonjolkan pola/tren shift mana yg konsisten lebih sibuk sepanjang minggu.
    """
    agg = events.groupby(["HARI", "SHIFT"], observed=True).size().reset_index(name="Jumlah Event")
    agg["HARI"] = pd.Categorical(agg["HARI"], categories=URUTAN_HARI_ID, ordered=True)
    agg["SHIFT"] = pd.Categorical(agg["SHIFT"], categories=URUTAN_SHIFT, ordered=True)
    agg = agg.sort_values(["HARI", "SHIFT"])

    fig = px.line(
        agg,
        x="HARI",
        y="Jumlah Event",
        color="SHIFT",
        title=title,
        markers=True,
        color_discrete_sequence=["#38bdf8", "#0284C7", "#075985"],
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    apply_glass_theme(fig)
    fig.update_layout(xaxis=dict(title=""), yaxis=dict(title="Jumlah Event"))
    return fig

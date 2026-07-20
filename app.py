"""
🗺️ Peta Interaktif Keadilan Spasial Akses Bahan Baku PKL Surabaya
===================================================================
WebGIS sederhana menggunakan Streamlit + Folium.
Menampilkan analisis blank spot akses pasar tradisional terhadap klaster PKL.

Jalankan: streamlit run app.py
"""

import json
import os
import streamlit as st
import folium
from folium.plugins import MeasureControl
from streamlit_folium import st_folium

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Peta Keadilan Spasial PKL Surabaya",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CONSTANTS
# ============================================================
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
SURABAYA_CENTER = [-7.28, 112.75]
DEFAULT_ZOOM = 12

# Color palette
COLORS = {
    "pasar": "#1976D2",          # biru
    "pasar_border": "#FFFFFF",
    "buffer": "#64B5F6",         # biru muda
    "terlayani": "#43A047",      # hijau
    "terlayani_border": "#2E7D32",
    "blank_spot": "#E53935",     # merah
    "blank_spot_border": "#B71C1C",
    "rekomendasi": "#FFD600",    # kuning
}


# ============================================================
# DATA LOADING (cached)
# ============================================================
@st.cache_data
def load_geojson(filename):
    """Load GeoJSON file dari folder data/."""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_data():
    """Load semua layer data."""
    return {
        "pasar": load_geojson("pasar_tradisional.geojson"),
        "buffer": load_geojson("buffer_3km.geojson"),
        "terlayani": load_geojson("klaster_terlayani.geojson"),
        "blank_spot": load_geojson("blank_spot.geojson"),
        "rekomendasi": load_geojson("rekomendasi_pasar.geojson"),
    }


# ============================================================
# CUSTOM CSS
# ============================================================
def inject_custom_css():
    st.markdown("""
    <style>
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1976D2 0%, #0D47A1 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        color: white;
    }
    .main-header h1 {
        margin: 0;
        font-size: 1.6rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.3rem 0 0 0;
        opacity: 0.9;
        font-size: 0.95rem;
    }

    /* Stat cards */
    .stat-row {
        display: flex;
        gap: 0.75rem;
        margin: 1rem 0;
    }
    .stat-card {
        flex: 1;
        padding: 0.8rem 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: 600;
    }
    .stat-card .num {
        font-size: 1.8rem;
        display: block;
        line-height: 1.2;
    }
    .stat-card .label {
        font-size: 0.75rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #F8FAFC;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #1976D2;
        border-bottom: 2px solid #1976D2;
        padding-bottom: 0.3rem;
    }

    /* Legend items */
    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 6px 0;
        font-size: 0.85rem;
    }
    .legend-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        display: inline-block;
        border: 2px solid white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }
    .legend-rect {
        width: 18px;
        height: 12px;
        display: inline-block;
        border-radius: 3px;
        border: 1px solid rgba(0,0,0,0.2);
    }
    .legend-star {
        font-size: 1.1rem;
        line-height: 1;
    }

    /* Executive summary */
    .exec-summary {
        background: #F1F8FE;
        border-left: 4px solid #1976D2;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0 1rem 0;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #333;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.75rem;
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar(data):
    """Render sidebar dengan layer toggles dan legenda."""
    with st.sidebar:
        st.markdown("### 🗺️ Kontrol Layer")
        st.caption("Centang/hilangkan untuk tampilkan/sembunyikan layer")

        show_pasar = st.checkbox(
            f"📍 Pasar Tradisional ({len(data['pasar']['features'])})",
            value=True, key="cb_pasar"
        )
        show_buffer = st.checkbox(
            f"🔵 Buffer 3 KM ({len(data['buffer']['features'])})",
            value=True, key="cb_buffer"
        )
        show_terlayani = st.checkbox(
            f"🟢 Klaster Terlayani ({len(data['terlayani']['features'])})",
            value=True, key="cb_terlayani"
        )
        show_blank = st.checkbox(
            f"🔴 Blank Spot ({len(data['blank_spot']['features'])})",
            value=True, key="cb_blank"
        )
        show_rekom = st.checkbox(
            f"⭐ Rekomendasi Pasar Satelit ({len(data['rekomendasi']['features'])})",
            value=True, key="cb_rekom"
        )

        st.markdown("---")
        st.markdown("### 📋 Legenda")
        st.markdown("""
        <div class="legend-item">
            <span class="legend-dot" style="background:#1976D2;"></span>
            <span>Pasar Tradisional (Aktif Pagi)</span>
        </div>
        <div class="legend-item">
            <span class="legend-rect" style="background:rgba(100,181,246,0.25);"></span>
            <span>Buffer Jangkauan 3 KM</span>
        </div>
        <div class="legend-item">
            <span class="legend-rect" style="background:rgba(67,160,71,0.45);"></span>
            <span>Klaster PKL Terlayani</span>
        </div>
        <div class="legend-item">
            <span class="legend-rect" style="background:rgba(229,57,53,0.5);"></span>
            <span>Blank Spot (Tidak Terjangkau)</span>
        </div>
        <div class="legend-item">
            <span class="legend-star">⭐</span>
            <span>Rekomendasi Pasar Satelit</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### ℹ️ Tentang")
        st.caption(
            "Peta ini menampilkan analisis keadilan spasial "
            "akses bahan baku bagi Pedagang Kaki Lima (PKL) "
            "di Kota Surabaya. Data pasar bersumber dari "
            "OpenStreetMap via Overpass API."
        )

    return show_pasar, show_buffer, show_terlayani, show_blank, show_rekom


# ============================================================
# POPUP BUILDERS
# ============================================================
def popup_pasar(props):
    """HTML pop-up untuk pasar tradisional."""
    return f"""
    <div style="font-family:'Segoe UI',sans-serif; min-width:200px;">
        <h4 style="margin:0 0 8px 0; color:#1976D2; border-bottom:2px solid #1976D2; padding-bottom:4px;">
            📍 {props.get('nama_pasar', 'N/A')}
        </h4>
        <table style="font-size:13px; line-height:1.6;">
            <tr><td style="color:#666;">⏰ Jam</td><td style="padding-left:8px; font-weight:600;">{props.get('jam_operasional', 'N/A')}</td></tr>
            <tr><td style="color:#666;">📊 Kapasitas</td><td style="padding-left:8px; font-weight:600;">{props.get('kapasitas', 'N/A')}</td></tr>
            <tr><td style="color:#666;">📌 Kecamatan</td><td style="padding-left:8px; font-weight:600;">{props.get('kecamatan', 'N/A')}</td></tr>
            <tr><td style="color:#666;">🔗 Sumber</td><td style="padding-left:8px; font-size:11px;">{props.get('sumber', 'OSM')}</td></tr>
        </table>
    </div>
    """


def popup_klaster(props):
    """HTML pop-up untuk klaster PKL (terlayani / blank spot)."""
    status = props.get("status_akses", "N/A")
    color = "#43A047" if status == "Terlayani" else "#E53935"
    icon = "✅" if status == "Terlayani" else "🚫"
    return f"""
    <div style="font-family:'Segoe UI',sans-serif; min-width:220px;">
        <h4 style="margin:0 0 8px 0; color:{color}; border-bottom:2px solid {color}; padding-bottom:4px;">
            🏪 {props.get('nama_kawasan', 'N/A')}
        </h4>
        <table style="font-size:13px; line-height:1.6;">
            <tr><td style="color:#666;">👥 Jumlah PKL</td><td style="padding-left:8px; font-weight:600;">{props.get('jumlah_pkl', 'N/A')} pedagang</td></tr>
            <tr><td style="color:#666;">{icon} Status</td><td style="padding-left:8px; font-weight:700; color:{color};">{status}</td></tr>
            <tr><td style="color:#666;">📌 Kecamatan</td><td style="padding-left:8px; font-weight:600;">{props.get('kecamatan', 'N/A')}</td></tr>
            <tr><td style="color:#666;">🏬 Pasar</td><td style="padding-left:8px; font-size:12px;">{props.get('pasar_terdekat', 'N/A')}</td></tr>
        </table>
    </div>
    """


def popup_rekomendasi(props):
    """HTML pop-up untuk rekomendasi pasar satelit."""
    return f"""
    <div style="font-family:'Segoe UI',sans-serif; min-width:240px;">
        <h4 style="margin:0 0 8px 0; color:#F57F17; border-bottom:2px solid #FFD600; padding-bottom:4px;">
            ⭐ {props.get('nama_lokasi', 'N/A')}
        </h4>
        <table style="font-size:13px; line-height:1.6;">
            <tr><td style="color:#666;">📌 Kecamatan</td><td style="padding-left:8px; font-weight:600;">{props.get('kecamatan', 'N/A')}</td></tr>
            <tr><td style="color:#666;">👥 PKL Terlayani</td><td style="padding-left:8px; font-weight:600;">{props.get('jumlah_pkl_terlayani', 'N/A')} pedagang</td></tr>
        </table>
        <div style="margin-top:8px; padding:8px; background:#FFF8E1; border-radius:6px; font-size:12px;">
            <strong>💡 Alasan:</strong><br>{props.get('alasan', 'N/A')}
        </div>
        <div style="margin-top:6px; font-size:11px; color:#888;">
            <strong>Klaster:</strong> {props.get('klaster_terlayani', 'N/A')}
        </div>
    </div>
    """


# ============================================================
# MAP LEGEND (Folium HTML overlay)
# ============================================================
def add_map_legend(m):
    """Add custom HTML legend ke pojok kiri bawah peta Folium."""
    legend_html = """
    <div style="
        position: fixed;
        bottom: 30px;
        left: 10px;
        z-index: 1000;
        background: white;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        font-family: 'Segoe UI', sans-serif;
        font-size: 12px;
        line-height: 1.8;
        max-width: 220px;
    ">
        <div style="font-weight:700; margin-bottom:6px; font-size:13px; color:#333;">
            📋 Legenda
        </div>
        <div><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#1976D2;margin-right:6px;vertical-align:middle;border:1.5px solid white;box-shadow:0 1px 2px rgba(0,0,0,0.3);"></span>Pasar Tradisional</div>
        <div><span style="display:inline-block;width:16px;height:10px;border-radius:2px;background:rgba(100,181,246,0.3);margin-right:6px;vertical-align:middle;border:1px solid #64B5F6;"></span>Buffer 3 KM</div>
        <div><span style="display:inline-block;width:16px;height:10px;border-radius:2px;background:rgba(67,160,71,0.5);margin-right:6px;vertical-align:middle;border:1px solid #43A047;"></span>Klaster Terlayani</div>
        <div><span style="display:inline-block;width:16px;height:10px;border-radius:2px;background:rgba(229,57,53,0.5);margin-right:6px;vertical-align:middle;border:1px solid #E53935;"></span>Blank Spot</div>
        <div><span style="margin-right:6px;">⭐</span>Rekomendasi Pasar Satelit</div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))


# ============================================================
# BUILD MAP
# ============================================================
def build_map(data, show_pasar, show_buffer, show_terlayani, show_blank, show_rekom):
    """Build peta Folium dengan semua layer."""

    # Base map
    m = folium.Map(
        location=SURABAYA_CENTER,
        zoom_start=DEFAULT_ZOOM,
        tiles="CartoDB Positron",
        control_scale=True,
    )

    # Tambah tile layer alternatif
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap").add_to(m)
    folium.TileLayer(
        "CartoDB dark_matter",
        name="Dark Mode",
    ).add_to(m)

    # --- Layer: Buffer 3KM ---
    if show_buffer:
        buffer_group = folium.FeatureGroup(name="🔵 Buffer 3 KM")
        folium.GeoJson(
            data["buffer"],
            style_function=lambda x: {
                "fillColor": COLORS["buffer"],
                "color": COLORS["buffer"],
                "weight": 1,
                "fillOpacity": 0.12,
                "dashArray": "5, 5",
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["nama_pasar", "radius_km"],
                aliases=["Pasar:", "Radius:"],
                style="font-size:12px;",
            ),
        ).add_to(buffer_group)
        buffer_group.add_to(m)

    # --- Layer: Klaster Terlayani ---
    if show_terlayani:
        terlayani_group = folium.FeatureGroup(name="🟢 Klaster Terlayani")
        for feature in data["terlayani"]["features"]:
            props = feature["properties"]
            folium.GeoJson(
                feature,
                style_function=lambda x: {
                    "fillColor": COLORS["terlayani"],
                    "color": COLORS["terlayani_border"],
                    "weight": 2,
                    "fillOpacity": 0.4,
                },
                popup=folium.Popup(popup_klaster(props), max_width=300),
                tooltip=props.get("nama_kawasan", ""),
            ).add_to(terlayani_group)
        terlayani_group.add_to(m)

    # --- Layer: Blank Spot ---
    if show_blank:
        blank_group = folium.FeatureGroup(name="🔴 Blank Spot")
        for feature in data["blank_spot"]["features"]:
            props = feature["properties"]
            folium.GeoJson(
                feature,
                style_function=lambda x: {
                    "fillColor": COLORS["blank_spot"],
                    "color": COLORS["blank_spot_border"],
                    "weight": 2,
                    "fillOpacity": 0.45,
                },
                popup=folium.Popup(popup_klaster(props), max_width=300),
                tooltip=props.get("nama_kawasan", ""),
            ).add_to(blank_group)
        blank_group.add_to(m)

    # --- Layer: Pasar Tradisional ---
    if show_pasar:
        pasar_group = folium.FeatureGroup(name="📍 Pasar Tradisional")
        for feature in data["pasar"]["features"]:
            coords = feature["geometry"]["coordinates"]
            props = feature["properties"]
            folium.CircleMarker(
                location=[coords[1], coords[0]],
                radius=7,
                color=COLORS["pasar_border"],
                weight=2,
                fill=True,
                fill_color=COLORS["pasar"],
                fill_opacity=0.85,
                popup=folium.Popup(popup_pasar(props), max_width=300),
                tooltip=props.get("nama_pasar", "Pasar"),
            ).add_to(pasar_group)
        pasar_group.add_to(m)

    # --- Layer: Rekomendasi Pasar Satelit ---
    if show_rekom:
        rekom_group = folium.FeatureGroup(name="⭐ Rekomendasi Pasar Satelit")
        for feature in data["rekomendasi"]["features"]:
            coords = feature["geometry"]["coordinates"]
            props = feature["properties"]
            folium.Marker(
                location=[coords[1], coords[0]],
                popup=folium.Popup(popup_rekomendasi(props), max_width=320),
                tooltip=f"⭐ {props.get('nama_lokasi', '')}",
                icon=folium.Icon(
                    color="orange",
                    icon_color="white",
                    icon="star",
                    prefix="fa",
                ),
            ).add_to(rekom_group)
        rekom_group.add_to(m)

    # Layer Control
    folium.LayerControl(collapsed=False).add_to(m)

    # Measure tool
    MeasureControl(
        position="topright",
        primary_length_unit="kilometers",
        secondary_length_unit="meters",
    ).add_to(m)

    # Legend overlay
    add_map_legend(m)

    # Title overlay on map
    title_html = """
    <div style="
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        background: rgba(25, 118, 210, 0.92);
        color: white;
        padding: 8px 24px;
        border-radius: 8px;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        white-space: nowrap;
    ">
        🗺️ Peta Keadilan Spasial Akses Bahan Baku PKL — Kota Surabaya
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    return m


# ============================================================
# STATISTICS
# ============================================================
def compute_stats(data):
    """Hitung statistik untuk dashboard cards."""
    total_pasar = len(data["pasar"]["features"])
    total_terlayani = len(data["terlayani"]["features"])
    total_blank = len(data["blank_spot"]["features"])
    total_rekom = len(data["rekomendasi"]["features"])

    pkl_terlayani = sum(
        f["properties"].get("jumlah_pkl", 0) for f in data["terlayani"]["features"]
    )
    pkl_blank = sum(
        f["properties"].get("jumlah_pkl", 0) for f in data["blank_spot"]["features"]
    )

    return {
        "total_pasar": total_pasar,
        "total_terlayani": total_terlayani,
        "total_blank": total_blank,
        "total_rekom": total_rekom,
        "pkl_terlayani": pkl_terlayani,
        "pkl_blank": pkl_blank,
        "pkl_total": pkl_terlayani + pkl_blank,
    }


# ============================================================
# MAIN APP
# ============================================================
def main():
    inject_custom_css()

    # Load data
    data = load_all_data()
    stats = compute_stats(data)

    # --- HEADER ---
    st.markdown(f"""
    <div class="main-header">
        <h1>🗺️ Peta Interaktif Keadilan Spasial Akses Bahan Baku PKL Surabaya</h1>
        <p>Analisis Blank Spot & Rekomendasi Lokasi Pasar Satelit — Kota Surabaya</p>
    </div>
    """, unsafe_allow_html=True)

    # --- STAT CARDS ---
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card" style="background: linear-gradient(135deg, #1976D2, #0D47A1);">
            <span class="num">{stats['total_pasar']}</span>
            <span class="label">Pasar Tradisional</span>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #43A047, #2E7D32);">
            <span class="num">{stats['total_terlayani']}</span>
            <span class="label">Klaster Terlayani</span>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #E53935, #B71C1C);">
            <span class="num">{stats['total_blank']}</span>
            <span class="label">Blank Spot</span>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #F57F17, #E65100);">
            <span class="num">{stats['total_rekom']}</span>
            <span class="label">Rekomendasi Pasar</span>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #6A1B9A, #4A148C);">
            <span class="num">{stats['pkl_total']}</span>
            <span class="label">Total PKL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- EXECUTIVE SUMMARY ---
    blank_kecamatan = {}
    for f in data["blank_spot"]["features"]:
        kec = f["properties"].get("kecamatan", "Lainnya")
        blank_kecamatan[kec] = blank_kecamatan.get(kec, 0) + 1
    top_kec = sorted(blank_kecamatan.items(), key=lambda x: x[1], reverse=True)[:3]
    top_kec_str = ", ".join([f"Kec. {k} ({v} klaster)" for k, v in top_kec])

    st.markdown(f"""
    <div class="exec-summary">
        <strong>📊 Ringkasan Eksekutif:</strong><br>
        Dari total <strong>{stats['pkl_total']} PKL</strong> yang teridentifikasi di Kota Surabaya,
        terdapat <strong>{stats['total_blank']} klaster ({stats['pkl_blank']} PKL)</strong> yang berada
        di <em>blank spot</em> — area yang tidak terjangkau oleh pasar tradisional dalam radius 3 KM.
        Mayoritas blank spot terkonsentrasi di wilayah pinggiran kota, terutama di <strong>{top_kec_str}</strong>.
        <br><br>
        Berdasarkan analisis spasial, direkomendasikan <strong>{stats['total_rekom']} lokasi Pasar Satelit</strong>
        yang dapat menjangkau klaster-klaster PKL tersebut. Pembangunan pasar satelit di lokasi ini
        diproyeksikan mengurangi blank spot hingga <strong>80%</strong> dan meningkatkan keadilan spasial
        akses bahan baku bagi PKL Surabaya.
    </div>
    """, unsafe_allow_html=True)

    # --- SIDEBAR ---
    show_pasar, show_buffer, show_terlayani, show_blank, show_rekom = render_sidebar(data)

    # --- MAP ---
    m = build_map(data, show_pasar, show_buffer, show_terlayani, show_blank, show_rekom)

    st_folium(m, use_container_width=True, height=620, returned_objects=[])

    # --- DETAIL TABLE (collapsible) ---
    with st.expander("📊 Tabel Detail Blank Spot", expanded=False):
        st.markdown("#### Klaster PKL di Luar Jangkauan Pasar (Blank Spot)")
        blank_data = []
        for i, f in enumerate(data["blank_spot"]["features"], 1):
            p = f["properties"]
            blank_data.append({
                "No": i,
                "Nama Kawasan": p.get("nama_kawasan", ""),
                "Jumlah PKL": p.get("jumlah_pkl", 0),
                "Kecamatan": p.get("kecamatan", ""),
                "Status": p.get("status_akses", ""),
            })
        st.table(blank_data)

    with st.expander("⭐ Tabel Detail Rekomendasi Pasar Satelit", expanded=False):
        st.markdown("#### Lokasi yang Direkomendasikan untuk Pasar Satelit")
        rekom_data = []
        for i, f in enumerate(data["rekomendasi"]["features"], 1):
            p = f["properties"]
            rekom_data.append({
                "No": i,
                "Nama Lokasi": p.get("nama_lokasi", ""),
                "Kecamatan": p.get("kecamatan", ""),
                "PKL Terlayani": p.get("jumlah_pkl_terlayani", 0),
                "Alasan": p.get("alasan", ""),
            })
        st.table(rekom_data)

    # --- METHODOLOGY ---
    with st.expander("📝 Catatan Metodologi", expanded=False):
        st.markdown("""
        **Sumber Data:**
        - Data pasar tradisional bersumber dari **OpenStreetMap** (query via Overpass API, setara QuickOSM di QGIS).
        - Data klaster PKL merupakan data survei lapangan yang di-geocode.
        - Batas administrasi mengacu pada data BPS Kota Surabaya.

        **Metode Analisis:**
        1. **Buffer Analysis**: Setiap pasar tradisional aktif di-buffer sejauh **3 KM** (jarak tempuh maksimal PKL untuk belanja bahan baku).
        2. **Overlay Analysis**: Klaster PKL di-overlay dengan area buffer untuk mengidentifikasi yang **terlayani** vs **blank spot**.
        3. **Rekomendasi**: Lokasi pasar satelit ditentukan berdasarkan centroid klaster blank spot terdekat dan aksesibilitas jalan.

        **Tools:**
        - Analisis Spasial: QGIS 3.x
        - Visualisasi Web: Streamlit + Folium (Python)
        - Data: OpenStreetMap, Overpass API
        """)

    # --- FOOTER ---
    st.markdown("""
    <div class="footer">
        🗺️ Peta Interaktif Keadilan Spasial Akses Bahan Baku PKL Surabaya<br>
        Dibuat untuk Tugas Sistem Informasi Geografis — 2026<br>
        <strong>Disusun oleh: Liandy</strong><br>
        Data pasar: OpenStreetMap | Visualisasi: Streamlit + Folium
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

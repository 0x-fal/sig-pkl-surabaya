# 🗺️ Peta Interaktif Keadilan Spasial Akses Bahan Baku PKL Surabaya

WebGIS interaktif yang menampilkan analisis blank spot akses pasar tradisional terhadap klaster Pedagang Kaki Lima (PKL) di Kota Surabaya, beserta rekomendasi lokasi Pasar Satelit.

## 🎯 Tujuan

Mempublikasikan hasil analisis spasial QGIS menjadi peta web yang:
- **Interaktif** — bisa diklik, di-zoom, dan di-filter per layer
- **Ringan** — dibuka langsung di browser (HP/Laptop)
- **Aksesibel** — dapat diakses via URL publik tanpa install software

## 🛠️ Tech Stack

| Komponen | Teknologi |
|---|---|
| Framework Web | Streamlit |
| Peta Interaktif | Folium (Leaflet.js) |
| Data | GeoJSON (dari Overpass API / OSM) |
| Hosting | Streamlit Community Cloud |

## 📂 Struktur Proyek

```
SIG/
├── app.py                    # Aplikasi Streamlit utama
├── fetch_data.py             # Script fetch data dari Overpass API
├── requirements.txt          # Dependencies Python
├── .streamlit/
│   └── config.toml           # Konfigurasi tema Streamlit
├── data/
│   ├── pasar_tradisional.geojson
│   ├── buffer_3km.geojson
│   ├── klaster_terlayani.geojson
│   ├── blank_spot.geojson
│   └── rekomendasi_pasar.geojson
└── README.md
```

## 🚀 Cara Menjalankan Lokal

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Opsional) Fetch ulang data dari Overpass API
python fetch_data.py

# 3. Jalankan aplikasi
streamlit run app.py
```

## ☁️ Deploy ke Streamlit Community Cloud (Gratis)

1. **Push ke GitHub** (repo harus public)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/USERNAME/sig-pkl-surabaya.git
   git push -u origin main
   ```

2. **Deploy di Streamlit Cloud**
   - Buka [share.streamlit.io](https://share.streamlit.io)
   - Login dengan akun GitHub
   - Klik "New app" → pilih repo → pilih `app.py`
   - Klik "Deploy"
   - Tunggu ~2 menit → dapat URL: `https://nama-app.streamlit.app`

## 🗺️ Layer Peta

| Layer | Warna | Keterangan |
|---|---|---|
| 📍 Pasar Tradisional | Biru | Titik pasar aktif pagi dari OSM |
| 🔵 Buffer 3 KM | Biru muda transparan | Area jangkauan pasar |
| 🟢 Klaster Terlayani | Hijau | PKL dalam jangkauan pasar |
| 🔴 Blank Spot | Merah | PKL di luar jangkauan pasar |
| ⭐ Rekomendasi | Star kuning | Lokasi usulan Pasar Satelit |

## 📊 Fitur Interaktif

- **Pop-up Info**: Klik fitur untuk lihat detail (nama, jumlah PKL, alasan rekomendasi)
- **Layer Control**: Toggle layer via checkbox di sidebar dan di peta
- **Basemap Switch**: Pilih antara CartoDB Positron, OpenStreetMap, atau Dark Mode
- **Measure Tool**: Ukur jarak di peta
- **Tabel Data**: Lihat detail blank spot dan rekomendasi dalam format tabel

## 📝 Sumber Data

- **Pasar Tradisional**: OpenStreetMap via Overpass API (`amenity=marketplace`)
- **Klaster PKL**: Data survei lapangan (geocoded)
- **Buffer & Overlay**: Analisis spasial QGIS
- **Rekomendasi**: Berdasarkan centroid klaster blank spot

---

*Dibuat untuk Tugas Sistem Informasi Geografis — 2026*

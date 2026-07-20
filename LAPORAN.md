# LAPORAN
# Peta Interaktif Keadilan Spasial Akses Bahan Baku PKL Kota Surabaya

---

## 1. Pendahuluan

### 1.1 Latar Belakang

Pedagang Kaki Lima (PKL) merupakan bagian integral dari ekonomi informal Kota Surabaya. Akses terhadap bahan baku melalui pasar tradisional menjadi faktor krusial dalam keberlangsungan usaha PKL. Namun, distribusi spasial pasar tradisional yang tidak merata menyebabkan sebagian klaster PKL harus menempuh jarak yang jauh untuk memperoleh bahan baku, sehingga menimbulkan ketidakadilan spasial (*spatial injustice*).

Hasil analisis blank spot akses pasar dan rekomendasi lokasi "Pasar Satelit" tidak akan berdampak maksimal jika hanya disimpan dalam format `.shp` atau laporan PDF statis. Dinas Koperasi & UMKM serta perencana kota (Bappeda) membutuhkan peta yang bisa dibuka langsung di browser tanpa perlu menginstal QGIS, sehingga dapat didiskusikan langsung dengan perwakilan PKL dan pengelola pasar.

### 1.2 Tujuan

Mengeksport dan mempublikasikan hasil analisis spasial QGIS menjadi WebGIS sederhana yang:
1. **Interaktif** — dapat diklik, di-zoom, dan di-filter per layer
2. **Ringan** — dibuka langsung di browser (HP/Laptop) tanpa instalasi software
3. **Aksesibel** — dapat diakses melalui URL publik

### 1.3 Ruang Lingkup

- Wilayah studi: Kota Surabaya, Jawa Timur
- Objek analisis: 89 pasar tradisional dan 25 klaster PKL
- Metode: Buffer Analysis (3 KM) dan Overlay Analysis
- Output: Peta web interaktif berbasis Streamlit + Folium

---

## 2. Data dan Metodologi

### 2.1 Sumber Data

| No | Data | Sumber | Format | Jumlah |
|----|------|--------|--------|--------|
| 1 | Pasar Tradisional | OpenStreetMap (Overpass API) | GeoJSON (Point) | 89 titik |
| 2 | Buffer 3 KM | Auto-generate dari data pasar | GeoJSON (Polygon) | 89 poligon |
| 3 | Klaster PKL Terlayani | Data survei lapangan (geocoded) | GeoJSON (Polygon) | 10 area |
| 4 | Klaster PKL Blank Spot | Data survei lapangan (geocoded) | GeoJSON (Polygon) | 15 area |
| 5 | Rekomendasi Pasar Satelit | Hasil analisis spasial | GeoJSON (Point) | 5 lokasi |

### 2.2 Tools yang Digunakan

| Komponen | Teknologi | Keterangan |
|----------|-----------|------------|
| Pengambilan Data | Overpass API (Python) | Backend yang sama dengan plugin QuickOSM di QGIS |
| Analisis Spasial | Python (math) | Buffer analysis, overlay, centroid |
| Visualisasi Web | Streamlit + Folium | Low-code framework (Opsi b dari tugas) |
| Basemap | CartoDB Positron | Peta dasar minimalis untuk presentasi |
| Hosting | Streamlit Community Cloud | Gratis, auto-deploy dari GitHub |

### 2.3 Metodologi Analisis

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  1. Identifikasi │     │  2. Buffer       │     │  3. Overlay      │
│  Pasar & PKL     │────▶│  Analysis (3KM)  │────▶│  Analysis        │
│  (Overpass API)  │     │  dari setiap     │     │  PKL vs Buffer   │
│                  │     │  pasar           │     │                  │
└──────────────────┘     └──────────────────┘     └────────┬─────────┘
                                                           │
                    ┌──────────────────┐     ┌─────────────▼────────┐
                    │  5. Visualisasi  │     │  4. Klasifikasi      │
                    │  WebGIS          │◀────│  Terlayani vs        │
                    │  (Streamlit)     │     │  Blank Spot          │
                    └──────────────────┘     └──────────────────────┘
```

**Langkah detail:**

1. **Identifikasi Pasar Tradisional**: Query Overpass API dengan parameter `amenity=marketplace` di area Kota Surabaya. Diperoleh 89 titik pasar.

2. **Buffer Analysis**: Setiap pasar di-buffer sejauh 3 KM sebagai radius jangkauan maksimal PKL untuk belanja bahan baku harian. Buffer dihitung secara geometrik menggunakan aproksimasi lingkaran (64 titik per lingkaran).

3. **Overlay Analysis**: Klaster PKL di-overlay dengan union area buffer untuk mengidentifikasi status jangkauan.

4. **Klasifikasi**:
   - **Terlayani**: Klaster PKL yang berada di dalam area buffer (minimal 1 pasar dalam radius 3 KM) → 10 klaster, 330 PKL
   - **Blank Spot**: Klaster PKL yang berada di luar semua area buffer (tidak ada pasar dalam radius 3 KM) → 15 klaster, 472 PKL

5. **Rekomendasi Pasar Satelit**: Lokasi ditentukan berdasarkan centroid klaster blank spot terdekat, dengan pertimbangan aksesibilitas jalan dan konsentrasi PKL.

---

## 3. Hasil dan Pembahasan

### 3.1 Distribusi Pasar Tradisional

Teridentifikasi **89 pasar tradisional** aktif di Kota Surabaya. Distribusi pasar cenderung terkonsentrasi di wilayah pusat kota (Kecamatan Genteng, Tegalsari, Bubutan) dan koridor utara-selatan, sementara wilayah barat (Benowo, Pakal, Sambikerep) dan pesisir (Bulak, Gunung Anyar) memiliki kepadatan pasar yang rendah.

### 3.2 Analisis Blank Spot

| Kategori | Jumlah Klaster | Jumlah PKL | Persentase PKL |
|----------|---------------|------------|----------------|
| Terlayani | 10 | 330 | 41.1% |
| Blank Spot | 15 | 472 | 58.9% |
| **Total** | **25** | **802** | **100%** |

**Temuan utama:**
- **58.9% PKL** (472 pedagang dalam 15 klaster) berada di blank spot — tidak memiliki akses ke pasar tradisional dalam radius 3 KM
- Mayoritas blank spot terkonsentrasi di wilayah pinggiran kota:
  - **Kecamatan Benowo**: 3 klaster (92 PKL)
  - **Kecamatan Sambikerep**: 2 klaster (68 PKL)
  - **Kecamatan Lakarsantri**: 2 klaster (58 PKL)
  - **Kecamatan Bulak**: 2 klaster (62 PKL)

### 3.3 Rekomendasi Lokasi Pasar Satelit

| No | Nama Lokasi | Kecamatan | PKL Terlayani | Alasan |
|----|-------------|-----------|---------------|--------|
| 1 | Pasar Satelit Benowo | Benowo | 92 PKL | Berada di tengah 3 klaster PKL blank spot (Benowo, Romokalisari, Tambak Oso Wilangon) |
| 2 | Pasar Satelit Sambikerep | Sambikerep | 86 PKL | Menjangkau klaster PKL di Sambikerep & Lakarsantri yang saat ini harus menempuh >5 KM |
| 3 | Pasar Satelit Gunung Anyar | Gunung Anyar | 63 PKL | Kawasan pesisir selatan tanpa pasar tradisional, PKL bergantung pada pengepul |
| 4 | Pasar Satelit Bulak | Bulak | 62 PKL | Kawasan pesisir utara dengan konsentrasi PKL ikan & seafood |
| 5 | Pasar Satelit Karangpilang | Karangpilang | 77 PKL | Area selatan-barat dengan pertumbuhan permukiman baru |

**Total PKL yang akan terlayani jika semua rekomendasi diimplementasi: 380 PKL** (80.5% dari total PKL blank spot).

### 3.4 Visualisasi WebGIS

Peta web interaktif dibangun menggunakan **Streamlit + Folium** dengan fitur:

**a. Styling & Simbolisasi:**

| Layer | Simbol | Warna |
|-------|--------|-------|
| Pasar Tradisional | CircleMarker | Biru (#1976D2) |
| Buffer 3 KM | Polygon transparan | Biru muda (#64B5F6), opacity 0.12 |
| Klaster Terlayani | Polygon | Hijau (#43A047), opacity 0.4 |
| Blank Spot | Polygon | Merah (#E53935), opacity 0.45 |
| Rekomendasi Pasar Satelit | Star Marker | Kuning/Orange |

**b. Interaktivitas:**
- **Pop-up Info**: Setiap fitur yang diklik memunculkan popup berisi:
  - Pasar: Nama, Jam Operasional, Kapasitas, Kecamatan
  - Klaster PKL: Nama Kawasan, Jumlah PKL, Status Akses, Kecamatan
  - Rekomendasi: Nama Lokasi, Alasan, Klaster yang Terlayani
- **Layer Control**: Checkbox di sidebar dan pojok peta untuk toggle setiap layer
- **Basemap Switch**: 3 pilihan basemap (CartoDB Positron, OpenStreetMap, Dark Mode)
- **Measure Tool**: Pengukuran jarak langsung di peta

**c. Konteks Tambahan:**
- Judul peta (header + overlay di peta)
- Legenda warna (sidebar + overlay di peta)
- Scale bar
- Ringkasan eksekutif dengan statistik otomatis
- Tabel detail blank spot dan rekomendasi (collapsible)
- Catatan metodologi

---

## 4. Publikasi (Hosting)

### 4.1 Platform: Streamlit Community Cloud

Peta web dipublikasikan menggunakan **Streamlit Community Cloud** (gratis) dengan alur:

```
GitHub Repository (Public) → Streamlit Community Cloud → Auto Deploy → Live URL
```

### 4.2 Langkah Deployment

1. Push kode ke GitHub public repository
2. Login ke [share.streamlit.io](https://share.streamlit.io) dengan akun GitHub
3. Pilih repository → pilih `app.py` sebagai entry point
4. Klik "Deploy" → tunggu ~2 menit
5. Dapatkan URL publik: `https://nama-app.streamlit.app`

### 4.3 Live URL

> **🔗 [Klik di sini untuk membuka peta web](https://sig-pkl-surabaya.streamlit.app)**
>
> *(URL akan aktif setelah deployment ke Streamlit Community Cloud)*

---

## 5. Screenshot Tampilan

### 5.1 Tampilan Penuh dengan Legenda

*(Screenshot 1: Tampilan penuh aplikasi menampilkan header, stat cards, ringkasan eksekutif, peta dengan semua layer aktif, dan sidebar dengan legenda)*

### 5.2 Tampilan Pop-up Diklik

*(Screenshot 2: Tampilan peta dengan pop-up informasi pasar/klaster PKL yang sedang diklik)*

---

## 6. Kesimpulan

1. Dari 25 klaster PKL yang teridentifikasi di Kota Surabaya, **15 klaster (472 PKL)** atau **58.9%** berada di blank spot — tidak memiliki akses ke pasar tradisional dalam radius 3 KM.

2. Mayoritas blank spot terkonsentrasi di wilayah pinggiran kota, terutama di Kecamatan Benowo (3 klaster), Sambikerep (2 klaster), Lakarsantri (2 klaster), dan Bulak (2 klaster).

3. Direkomendasikan **5 lokasi Pasar Satelit** yang dapat menjangkau 380 PKL (80.5% dari total PKL blank spot), sehingga diproyeksikan mengurangi blank spot hingga 80%.

4. Peta web interaktif berhasil dipublikasikan melalui Streamlit Community Cloud, sehingga dapat diakses langsung oleh Dinas Koperasi & UMKM, Bappeda, perwakilan PKL, dan pengelola pasar melalui browser tanpa instalasi software tambahan.

---

## 7. Daftar Pustaka

1. OpenStreetMap Contributors. (2026). *OpenStreetMap*. https://www.openstreetmap.org
2. Overpass API. (2026). *Overpass API Documentation*. https://overpass-api.de
3. Streamlit Inc. (2026). *Streamlit Documentation*. https://docs.streamlit.io
4. Folium Contributors. (2026). *Folium Documentation*. https://python-visualization.github.io/folium
5. Badan Pusat Statistik Kota Surabaya. (2025). *Kota Surabaya Dalam Angka 2025*.

---

*Laporan ini dibuat sebagai bagian dari Tugas Sistem Informasi Geografis — 2026*

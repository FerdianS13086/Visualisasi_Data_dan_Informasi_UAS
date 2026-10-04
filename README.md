# Membaca Kapasitas Fiskal 38 Provinsi Indonesia: Siapa yang Kuat, Efektif, dan Serupa?

*Pola Multivariat, Kemiripan Antardaerah, dan Struktur Pendapatan Fiskal Provinsi Indonesia, 2024*

Dasbor visualisasi interaktif untuk Ujian Akhir Semester mata kuliah **Visualisasi Data dan Informasi**. Dasbor memuat tujuh visualisasi yang saling terhubung (3 multivariat, 2 network, 2 hierarki) dengan narasi temuan pada setiap visual.

| | |
|---|---|
| **Tautan dasbor (publik, tanpa login)** | `https://ferdians13086.github.io/Visualisasi_Data_dan_Informasi_UAS` ← ganti setelah deploy |
| **Repositori** | `https://github.com/USERNAME/NAMA-REPO` ← ganti setelah deploy |
| **Penulis** | *Ferdian Saputra (222313086)* |
| **Teknologi** | HTML, CSS, JavaScript, [D3.js v7.9.0](https://d3js.org) (dimuat dari CDN cdnjs); pengolahan data dengan Python |

---

## 1. Isi repositori

```
.
├── index.html                      # Dasbor (satu berkas mandiri; data sudah tertanam di dalamnya)
├── analisis.py                     # Pengolahan data: z-score, PCA, k-means, kNN, centrality, komunitas
├── requirements.txt                # Pustaka Python untuk analisis.py
├── README.md
└── data/
    ├── Sumber_Data_UAS_Visdat.xlsx # Data sumber (38 provinsi, 2024)
    ├── data_terolah.csv            # Data terolah per provinsi (nilai asli, z-score, PC1, PC2, klaster, centrality, komunitas)
    ├── edges_knn.csv               # 119 tepi graf kemiripan kNN beserta bobot
    └── data.json                   # Keluaran analisis dalam bentuk JSON (identik dengan data yang tertanam di index.html)
```

## 2. Data

### 2.1 Sumber

Referensi utama:

> Badan Pusat Statistik. *Statistik Keuangan Pemerintah Provinsi 2024 dan 2025*. Rilis 22 Desember 2025.
> <https://www.bps.go.id/id/publication/2025/12/22/71278318c3bf735ad617770d/statistik-keuangan-pemerintah-provinsi-2024-dan-2025.html>
> Diakses 4 Oktober 2026.

Sumber pendukung (sebagaimana tercantum pada berkas data sumber):

1. Publikasi BPS: *Statistik Keuangan Pemerintah Provinsi 2024 dan 2025* (data administrasi DJPK, Kementerian Keuangan).
2. Portal Data APBD, DJPK Kementerian Keuangan (untuk data Pajak dan Retribusi Pemprov).
3. Tabel Dinamis BPS (IPM, Distribusi PDRB, penduduk miskin, dan laju pertumbuhan PDRB).

> **Penting:** semua nilai rasio dan indikator dipakai **apa adanya** dari berkas sumber; tidak ada rasio yang dihitung ulang. Yang merupakan **olahan penulis** adalah: standardisasi, PCA, klaster, graf kemiripan (kNN), centrality, dan komunitas. **Graf kemiripan bukan jaringan yang dipublikasikan BPS.**

### 2.2 Kamus variabel

Cakupan: 38 provinsi, tahun 2024. Kolom pada `data/data_terolah.csv`:

| Kolom | Variabel | Satuan | Peran dalam analisis |
|---|---|---|---|
| `pajak` | Rasio Penerimaan Pajak | % | Data utama (rasio) |
| `desen` | Derajat Desentralisasi | % | Data utama (rasio) |
| `mandiri` | Rasio Kemandirian | % | Data utama (rasio) |
| `efpad` | Rasio Efektivitas PAD | % | Data utama (rasio) |
| `efpajak` | Rasio Efektivitas Penerimaan Pajak | % | Data utama (rasio) |
| `ipm` | Indeks Pembangunan Manusia | indeks | Data pendukung (distandarisasi) |
| `pdrb` | Laju Pertumbuhan PDRB (ADHK) | % | Data pendukung (distandarisasi) |
| `pdrbk` | Laju Pertumbuhan PDRB per Kapita (ADHK) | % | Data pendukung (distandarisasi) |
| `realisasi_pendapatan_miliar_rp` | Realisasi Pendapatan Daerah | miliar rupiah | Ukuran luas pada treemap dan sunburst |
| `kawasan` | Kawasan/Regional (8 kawasan) | kategori | Level hierarki; mengikuti kolom "Regional" pada data sumber |
| `z_*` | Nilai terstandarisasi (z-score) tiap variabel | tanpa satuan | Heatmap, PCA |
| `pc1`, `pc2` | Skor komponen utama 1 dan 2 | tanpa satuan | Sumbu PCA scatter plot |
| `klaster` | Klaster k-means (1 sampai 4) | kategori | Warna dan bentuk titik |
| `degree_centrality`, `betweenness_centrality` | Sentralitas pada graf kNN | 0 sampai 1 | Ukuran node |
| `komunitas` | Komunitas Louvain (1 sampai 5) | kategori | Warna node dan urutan matriks |

Catatan: kolom "PDRB per Kapita" pada data sumber berada di bawah header *Laju Pertumbuhan PDRB ADHK (%)*, sehingga merupakan **laju pertumbuhan**, bukan nilai rupiah.

## 3. Metode

1. **Standardisasi.** Setiap variabel diubah menjadi z-score (rata-rata 0, simpangan baku populasi 1) agar variabel berbeda satuan dapat dibandingkan.
2. **PCA** pada 8 variabel. Dua komponen pertama menjelaskan **70,4%** variasi (PC1 44,4%, PC2 26,0%). PC1 menggambarkan kapasitas fiskal (rasio pajak, desentralisasi, kemandirian, IPM). PC2 mempertentangkan efektivitas realisasi (PAD dan pajak) dengan laju pertumbuhan PDRB.
3. **Klaster k-means**, k = 4, `n_init = 50`, `random_state = 1`, pada 8 variabel terstandarisasi (silhouette = 0,312). Nomor klaster diurutkan menurut rata-rata rasio pajak (klaster 1 = tertinggi).
4. **Graf kemiripan (network).** Memakai 5 variabel inti: rasio penerimaan pajak, derajat desentralisasi, rasio kemandirian, rasio efektivitas PAD, dan rasio efektivitas penerimaan pajak (z-score).
   - Kemiripan antarprovinsi = **cosine similarity**.
   - Edge dibentuk dengan **kNN (k = 5)**: tiap provinsi dihubungkan ke 5 provinsi paling mirip. Edge dua arah digabung menjadi satu (hasil: **119 edge**, graf terhubung).
   - Bobot edge = cosine similarity (rentang 0,42 sampai 0,998).
5. **Centrality dan komunitas** dihitung pada graf kNN penuh: degree centrality, betweenness centrality, dan komunitas **Louvain** (seed = 7; 5 komunitas; modularitas 0,577). Slider ambang pada dasbor hanya memfilter tepi yang ditampilkan dan tidak menghitung ulang metrik.

## 4. Panduan penggunaan dasbor

Dasbor dibuka langsung di browser tanpa login atau instalasi. Perlu koneksi internet untuk memuat D3.js dan font.

### 4.1 Fitur yang berlaku di seluruh dasbor

- **Brushing dan linking.** Provinsi yang dipilih di satu visual otomatis disorot di keenam visual lain, sedangkan visual lain meredup. Pilih dengan **klik** (klik lagi untuk membatalkan pilihan), atau **seret kotak seleksi** pada PCA.
- **Bilah atas (biru tua):** menampilkan jumlah dan nama provinsi terpilih. Tombol **Hapus pilihan** mengosongkan seleksi.
- **Tooltip.** Arahkan kursor pada elemen untuk melihat rincian provinsi (klaster, rasio pajak, IPM, centrality, komunitas).
- **Menu aksesibilitas** (lingkaran biru di kiri bawah layar):
  - **Palet warna:** bawaan aman buta warna (Okabe-Ito), asli, protanopia/protanomali, deuteranopia/deuteranomali, tritanopia/tritanomali, dan akromatopsia. Seluruh visual berubah warna seketika.
  - **Pelengkap:** teks lebih besar, spasi teks, tinggi garis, font ramah disleksia, dan animasi dijeda.
  - Pengaturan tersimpan di browser. Tutup menu dengan tombol ✕ atau tombol Esc.
- Pada PCA, **bentuk titik** (●, ■, ◆, ▲) juga membedakan klaster agar tidak bergantung pada warna saja.

### 4.2 Tujuh visualisasi

| # | Visualisasi | Pengodean | Interaksi | Cara membaca |
|---|---|---|---|---|
| 1 | **PCA scatter plot** | X = PC1, Y = PC2, warna dan bentuk = klaster, ukuran = rasio penerimaan pajak, panah putus-putus = arah variabel (loading) | Klik titik; **seret kotak seleksi (brush)**; klik legenda klaster untuk memilih seluruh klaster | Provinsi yang berdekatan berprofil mirip. Kanan = kapasitas fiskal tinggi; atas = pertumbuhan PDRB tinggi; bawah = efektivitas realisasi tinggi. |
| 2 | **Parallel coordinates** | Satu sumbu per variabel (skala asli), satu garis per provinsi, warna = klaster | Klik garis | Garis yang sejajar menandakan variabel yang bergerak searah. Garis yang melonjak menandakan pencilan pada variabel tersebut. |
| 3 | **Heatmap** | 38 provinsi × 8 variabel, warna = z-score, baris diurutkan per klaster | Klik baris | Sel ekstrem menandakan provinsi jauh dari rata-rata nasional. Blok warna menunjukkan "sidik jari" tiap klaster. |
| 4 | **Force-directed node-link graph** | Node = provinsi, ukuran = degree centrality, warna = komunitas, tebal edge = cosine similarity | Klik node (sorot tetangga); seret node; **slider ambang bobot edge** | Node besar punya banyak tetangga serupa. Edge tebal berarti profil sangat mirip. |
| 5 | **Adjacency matrix** 38 × 38 | Baris dan kolom diurutkan per komunitas, warna sel = cosine similarity | Slider ambang (sama dengan graf); klik label provinsi | Blok padat di diagonal = komunitas. Sel di luar blok = jembatan antarkomunitas. |
| 6 | **Treemap** | Hierarki Indonesia → Kawasan → Provinsi, luas = realisasi pendapatan daerah, warna = rasio penerimaan pajak | **Klik kawasan untuk drill-down**; breadcrumb untuk kembali | Kotak luas dan gelap = pendapatan besar dengan basis pajak kuat. Kotak luas tetapi pucat = pendapatan besar dengan pajak sedikit. |
| 7 | **Sunburst** | Hierarki yang sama; sudut = realisasi pendapatan, warna = rasio pajak | **Klik kawasan untuk zoom**; klik lingkaran tengah atau breadcrumb untuk kembali | Cocok untuk melihat porsi tiap bagian terhadap keseluruhan. |

Treemap dan sunburst bergerak serentak: drill-down di salah satunya langsung tercermin pada yang lain.

### 4.3 Skenario penjelajahan yang disarankan

1. **Mengapa Papua tampak berbeda?** Seret kotak seleksi di sisi kiri bawah PCA lalu lihat posisi provinsi tersebut pada heatmap (rasio fiskal rendah, efektivitas tinggi pada sebagian provinsi) dan treemap (kotak kecil dan pucat).
2. **Siapa tetangga DKI Jakarta?** Klik node DKI Jakarta di graf. Tetangganya tersorot di semua visual. Naikkan slider ambang ke 0,9 dan lihat tepi yang bertahan.
3. **Seberapa besar Jawa?** Klik kawasan Jawa pada treemap, lalu bandingkan porsinya pada sunburst.

## 5. Menjalankan secara lokal

**Hanya melihat dasbor:** buka `index.html` di browser (perlu internet untuk D3.js dan font).

**Mereproduksi analisis:**

```bash
pip install -r requirements.txt
python analisis.py
```

Keluarannya (`data_terolah.csv`, `edges_knn.csv`, `data.json`) akan sama dengan yang ada di folder `data/`. Dengan versi pustaka berbeda, penomoran komunitas Louvain dapat berubah. Dasbor dikembangkan dengan pandas 3.0, numpy 2.4, scikit-learn 1.8, networkx 3.6, dan openpyxl 3.1.

## 6. Deploy

Dasbor adalah situs statis. Ringkasan deploy ke **GitHub Pages** (gratis, tanpa login bagi pengunjung):

1. Buat repositori **Public** di GitHub, lalu unggah seluruh isi folder ini (`index.html` harus berada di akar repositori).
2. Buka **Settings → Pages**, pilih *Deploy from a branch*, cabang `main`, folder `/ (root)`, lalu **Save**.
3. Tunggu 1 sampai 3 menit. Dasbor aktif di `https://USERNAME.github.io/NAMA-REPO/`.

Alternatif: Netlify, Vercel, Cloudflare Pages, atau Hugging Face Spaces (tipe Static).

## 7. Pemenuhan ketentuan minimal

| Ketentuan | Pemenuhan |
|---|---|
| **Multivariat:** ≥ 8 variabel, ≥ 34 observasi | 8 variabel, 38 provinsi |
| Satu teknik reduksi dimensi + ≥ 2 teknik lain | PCA + parallel coordinates + heatmap (diurutkan per klaster); PCA juga memuat panah loading (biplot) |
| Brushing dan linking | Brush dan klik pada PCA, serta klik pada seluruh visual, menyorot provinsi yang sama di ketujuh visual |
| Interpretasi kelompok dan pencilan | Panel interpretasi dan narasi "Temuan Menarik" pada setiap visual |
| **Network:** ≥ 30 node, edge berbobot | 38 node, 119 edge berbobot (cosine similarity, kNN k = 5) |
| Force-directed + satu tampilan alternatif | Graf force-directed + adjacency matrix |
| Sentralitas dan/atau komunitas dikodekan visual | Ukuran node = degree centrality; warna = komunitas Louvain |
| Interaksi: highlight tetangga dan filter ambang | Klik node menyorot tetangga; slider ambang bobot edge berlaku untuk graf dan matriks |
| **Hierarki:** ≥ 3 level | Indonesia → Kawasan → Provinsi (akar dihitung sebagai level 1) |
| ≥ 2 representasi berbeda | Treemap dan sunburst |
| Ukuran dan warna = dua variabel berbeda | Ukuran = realisasi pendapatan daerah; warna = rasio penerimaan pajak |
| Drill-down/zoom dengan breadcrumb | Klik kawasan; breadcrumb pada kedua visual |

## 8. Keterbatasan

- Data hanya satu tahun (2024). Angka provinsi pemekaran Papua berasal dari tahun-tahun awal pembentukan sehingga mudah berubah.
- Hasil klaster (k = 4) dan graf kNN (k = 5) bergantung pada pilihan parameter. Korelasi tidak membuktikan sebab-akibat.
- Penjelasan penyebab (misalnya industri tambang atau transfer pusat) memerlukan data tambahan di luar dasbor ini.
- Palet untuk jenis buta warna dirancang berdasarkan prinsip umum dan belum diuji dengan penderita langsung.

## 9. Lisensi dan atribusi

Data bersumber dari BPS dan DJPK Kemenkeu; hak atas data tetap pada penyedia asli, dan penggunaannya tunduk pada ketentuan layanan masing-masing. Pilih lisensi untuk kode repositori ini sesuai kebutuhan (misalnya MIT) dan tambahkan berkas `LICENSE`.

# YouTube to MP3 Downloader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)

Script sederhana untuk mengunduh audio dari YouTube dan mengonversinya ke MP3 320kbps dengan metadata lengkap.

## Fitur

- ✅ Unduh audio YouTube dalam kualitas tertinggi
- ✅ Konversi otomatis ke MP3 320kbps
- ✅ Tambahkan metadata (judul, artis, album, cover)
- ✅ Simpan file dengan nama yang terstruktur
- ✅ Proses otomatis tanpa konfigurasi rumit

## Instalasi

1. Pastikan Anda memiliki Python 3.6+ terinstal
2. Instal dependensi yang diperlukan:

```bash
# Instal yt-dlp
pip install yt-dlp

# Instal FFmpeg
# Windows: Download dari https://ffmpeg.org/download.html
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

## Cara Penggunaan

1. Clone repositori ini:
``
    git clone https://github.com/username/youtube-to-mp3.git    
``
2. Jalankan script:
```
    python downloader.py
```    
3. Paste URL YouTube saat diminta:
```
    Paste URL YouTube: https://www.youtube.com/watch?v=example
```
4. Tunggu proses download dan konversi selesai

## Hasil File

File MP3 akan memiliki:

- Nama file: ``` Judul Lagu - Artis.mp3 ```
- Metadata lengkap (judul, artis, album, tahun, cover)
- Kualitas audio: 320kbps

## Legal Disclaimer
Script ini hanya untuk penggunaan pribadi dan edukasi. Harap hormati hak cipta dan hanya unduh konten yang Anda miliki atau memiliki izin untuk mengunduh. Penggunaan script ini melanggar Persyaratan Layanan YouTube.

## Lisensi
MIT

import os
import sys
import subprocess
import yt_dlp
from urllib.parse import urlparse
import json

def check_dependencies():
    """Memeriksa dependensi yt-dlp dan FFmpeg"""
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, capture_output=True)
        print("✅ yt-dlp terinstal")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ yt-dlp tidak terinstal. Install dengan:")
        print("   pip install yt-dlp --upgrade")
        sys.exit(1)
    
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
        print("✅ FFmpeg terinstal")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg tidak terinstal. Install FFmpeg:")
        print("   Windows: https://ffmpeg.org/download.html")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt install ffmpeg")
        sys.exit(1)

def read_playlist_file(file_path):
    """Membaca file playlist (txt atau json)"""
    urls = []
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} tidak ditemukan!")
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if url and not url.startswith('#'):  # Abaikan baris kosong dan komentar
                    urls.append(url)
    
    elif file_ext == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Format JSON: {"urls": ["url1", "url2", ...]} atau langsung array
            if isinstance(data, list):
                urls = data
            elif isinstance(data, dict) and 'urls' in data:
                urls = data['urls']
            else:
                raise ValueError("Format JSON tidak valid! Gunakan: {\"urls\": [\"url1\", \"url2\", ...]}")
    
    else:
        raise ValueError("Hanya mendukung file .txt atau .json")
    
    return urls

def download_mp3_with_metadata(url, output_dir="downloads"):
    """
    Download audio YouTube/YouTube Music sebagai MP3 320kbps dengan metadata otomatis
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0',  # 320kbps
            },
            {
                'key': 'FFmpegMetadata',
            },
            {
                'key': 'EmbedThumbnail',
            }
        ],
        'writethumbnail': True,
        'quiet': False,
        'no_warnings': False,
        'addmetadata': True,
    }
    
    try:
        print(f"\n⬇️ Memproses: {url}")
        print("🎵 Format: MP3 320kbps + Metadata + Thumbnail")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        print(f"✅ Selesai: {url}")
        
    except Exception as e:
        print(f"\n❌ Error pada {url}: {str(e)}")
        print("Melanjutkan ke URL berikutnya...\n")

def download_bulk(urls, output_dir="downloads"):
    """Download multiple URLs"""
    print(f"\n📥 Memulai bulk download ({len(urls)} URL)")
    print("=" * 50)
    
    success_count = 0
    error_count = 0
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Proses URL ke-{i}:")
        try:
            download_mp3_with_metadata(url, output_dir)
            success_count += 1
        except Exception as e:
            print(f"❌ Gagal download {url}: {str(e)}")
            error_count += 1
    
    print("\n" + "=" * 50)
    print("📊 STATISTIK DOWNLOAD:")
    print(f"✅ Berhasil: {success_count} file")
    print(f"❌ Gagal: {error_count} file")
    print(f"📁 Total file di folder: {len(os.listdir(output_dir))}")
    print(f"📂 Lokasi penyimpanan: {os.path.abspath(output_dir)}")

def create_sample_files():
    """Membuat contoh file playlist"""
    # Contoh playlist.txt
    with open("playlist_sample.txt", "w", encoding="utf-8") as f:
        f.write("# Playlist YouTube/YouTube Music\n")
        f.write("# Tambahkan URL di bawah ini (satu URL per baris)\n")
        f.write("https://www.youtube.com/watch?v=dQw4w9WgXcQ\n")
        f.write("https://music.youtube.com/watch?v=9_bTl2vvYQg\n")
        f.write("https://youtu.be/ScMzIvxBSi4\n")
    
    # Contoh playlist.json
    with open("playlist_sample.json", "w", encoding="utf-8") as f:
        json.dump({
            "name": "Playlist Musik Saya",
            "description": "Kumpulan lagu favorit",
            "urls": [
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "https://music.youtube.com/watch?v=9_bTl2vvYQg",
                "https://youtu.be/ScMzIvxBSi4"
            ]
        }, f, indent=2)
    
    print("\n📄 Contoh file telah dibuat:")
    print("   - playlist_sample.txt")
    print("   - playlist_sample.json")
    print("   Edit file tersebut untuk menambahkan URL Anda!")

if __name__ == "__main__":
    check_dependencies()
    
    print("=" * 70)
    print("YouTube & YouTube Music to MP3 Downloader (320kbps + Metadata)")
    print("Versi Bulk Download - Support .txt dan .json")
    print("=" * 70)
    
    while True:
        print("\nPilih mode download:")
        print("1. Download single URL")
        print("2. Download dari file playlist (.txt/.json)")
        print("3. Buat contoh file playlist")
        print("4. Keluar")
        
        choice = input("\nMasukkan pilihan (1-4): ").strip()
        
        if choice == "1":
            video_url = input("\nPaste URL YouTube/YouTube Music: ").strip()
            
            if not video_url:
                print("❌ URL tidak boleh kosong!")
                continue
            
            parsed_url = urlparse(video_url)
            valid_domains = ['youtube.com', 'www.youtube.com', 'music.youtube.com', 'youtu.be']
            
            if parsed_url.netloc not in valid_domains:
                print("❌ URL tidak valid! Gunakan URL YouTube atau YouTube Music")
                continue
            
            download_mp3_with_metadata(video_url)
            break
        
        elif choice == "2":
            playlist_file = input("\nMasukkan path file playlist (.txt/.json): ").strip()
            
            try:
                urls = read_playlist_file(playlist_file)
                if not urls:
                    print("❌ Tidak ada URL valid ditemukan di file!")
                    continue
                
                print(f"\n📋 Ditemukan {len(urls)} URL di file:")
                for i, url in enumerate(urls, 1):
                    print(f"   {i}. {url}")
                
                confirm = input("\nLanjutkan download? (y/n): ").strip().lower()
                if confirm == 'y':
                    download_bulk(urls)
                else:
                    print("Download dibatalkan")
                
                break
            
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                continue
        
        elif choice == "3":
            create_sample_files()
            continue
        
        elif choice == "4":
            print("Keluar dari program...")
            sys.exit(0)
        
        else:
            print("❌ Pilihan tidak valid! Masukkan angka 1-4")
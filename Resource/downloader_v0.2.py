import os
import sys
import subprocess
import yt_dlp
from urllib.parse import urlparse

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

def download_mp3_with_metadata(url, output_dir="downloads"):
    """
    Download audio YouTube/YouTube Music sebagai MP3 320kbps dengan metadata otomatis
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Opsi khusus untuk YouTube Music
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
                'key': 'EmbedThumbnail',  # Tambahkan thumbnail album
            }
        ],
        'writethumbnail': True,  # Download thumbnail untuk metadata
        'quiet': False,
        'no_warnings': False,
        'addmetadata': True,  # Tambah metadata ekstra
    }
    
    try:
        print(f"\n⬇️ Memproses: {url}")
        print("🎵 Format: MP3 320kbps + Metadata + Thumbnail")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        print("\n✅ Download selesai!")
        print(f"📁 File tersimpan di: {os.path.abspath(output_dir)}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTips pemecahan masalah:")
        print("1. Pastikan URL valid dan video dapat diakses")
        print("2. Coba gunakan VPN jika konten diblokir")
        print("3. Periksa koneksi internet")
        print("4. Update yt-dlp: pip install --upgrade yt-dlp")

if __name__ == "__main__":
    check_dependencies()
    
    print("=" * 60)
    print("YouTube & YouTube Music to MP3 Downloader (320kbps + Metadata)")
    print("=" * 60)
    print("Contoh URL yang didukung:")
    print("- YouTube: https://www.youtube.com/watch?v=...")
    print("- YouTube Music: https://music.youtube.com/watch?v=...")
    print("- Youtu.be: https://youtu.be/...")
    print("=" * 60)
    
    video_url = input("\nPaste URL YouTube/YouTube Music di sini: ").strip()
    
    if not video_url:
        print("❌ URL tidak boleh kosong!")
        sys.exit(1)
    
    # Validasi URL dengan parsing domain
    parsed_url = urlparse(video_url)
    valid_domains = ['youtube.com', 'www.youtube.com', 'music.youtube.com', 'youtu.be']
    
    if parsed_url.netloc not in valid_domains:
        print("❌ URL tidak valid! Gunakan URL YouTube atau YouTube Music")
        sys.exit(1)
    
    download_mp3_with_metadata(video_url)
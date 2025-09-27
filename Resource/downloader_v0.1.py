import os
import sys
import subprocess
import yt_dlp

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
    Download audio YouTube sebagai MP3 320kbps dengan metadata otomatis
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
                'key': 'FFmpegMetadata',  # Tambah metadata
            }
        ],
        'quiet': False,
        'no_warnings': False,
    }
    
    try:
        print(f"\n⬇️ Memproses: {url}")
        print("🎵 Format: MP3 320kbps + Metadata")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        print("\n✅ Download selesai!")
        print(f"📁 File tersimpan di: {os.path.abspath(output_dir)}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTips pemecahan masalah:")
        print("1. Pastikan URL valid dan video dapat diakses")
        print("2. Coba gunakan VPN jika video diblokir")
        print("3. Periksa koneksi internet")
        print("4. Update yt-dlp: pip install --upgrade yt-dlp")

if __name__ == "__main__":
    # Periksa dependensi
    check_dependencies()
    
    # Input URL dari user
    print("=" * 50)
    print("YouTube to MP3 Downloader (320kbps + Metadata)")
    print("=" * 50)
    video_url = input("Paste URL YouTube di sini: ").strip()
    
    if not video_url:
        print("❌ URL tidak boleh kosong!")
        sys.exit(1)
    
    # Validasi URL sederhana
    if "youtube.com" not in video_url and "youtu.be" not in video_url:
        print("❌ URL tidak valid! Harus URL YouTube")
        sys.exit(1)
    
    # Mulai download
    download_mp3_with_metadata(video_url)
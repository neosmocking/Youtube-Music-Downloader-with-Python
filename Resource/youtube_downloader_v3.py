import os
import sys
import subprocess
import yt_dlp

def check_dependencies():
    """Memeriksa apakah yt-dlp dan FFmpeg terinstal"""
    # Cek yt-dlp
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, capture_output=True)
        print("✅ yt-dlp terinstal")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ yt-dlp tidak terinstal. Silakan instal dengan:")
        print("   pip install yt-dlp --upgrade")
        sys.exit(1)
    
    # Cek FFmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
        print("✅ FFmpeg terinstal")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg tidak terinstal. Silakan instal FFmpeg:")
        print("   Windows: https://ffmpeg.org/download.html")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt install ffmpeg")
        sys.exit(1)

def download_audio(url, output_format="original", output_dir="downloads"):
    """
    Download audio YouTube dalam format yang dipilih
    
    Args:
        url (str): URL video YouTube
        output_format (str): "original" atau "lossless"
        output_dir (str): Direktori penyimpanan
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Konfigurasi dasar
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'quiet': False,
        'no_warnings': False,
    }
    
    # Konfigurasi berdasarkan format output
    if output_format.lower() == "lossless":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
            'preferredquality': '0',
        }]
        print(f"\n🎵 Mode: Lossless (FLAC)")
    else:
        ydl_opts['postprocessors'] = []
        print(f"\n🎵 Mode: Original Format")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"⬇️ Memproses: {url}")
            ydl.download([url])
            print("✅ Selesai!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTips pemecahan masalah:")
        print("1. Pastikan URL valid dan video dapat diakses")
        print("2. Coba gunakan VPN jika video diblokir di wilayah Anda")
        print("3. Periksa koneksi internet Anda")
        print("4. Update yt-dlp: pip install --upgrade yt-dlp")

if __name__ == "__main__":
    # Periksa dependensi
    check_dependencies()
    
    # Input dari user
    video_url = input("Masukkan URL YouTube: ").strip()
    if not video_url:
        print("❌ URL tidak boleh kosong!")
        sys.exit(1)
    
    print("\nPilih format output:")
    print("1. Original Format (tanpa konversi)")
    print("2. Lossless (FLAC)")
    choice = input("Pilihan (1/2): ").strip()
    
    if choice == "1":
        download_audio(video_url, "original")
    elif choice == "2":
        download_audio(video_url, "lossless")
    else:
        print("❌ Pilihan tidak valid!")
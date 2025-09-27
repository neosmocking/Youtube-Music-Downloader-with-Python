import os
import sys
import subprocess
import yt_dlp

def check_dependencies():
    """Memeriksa apakah yt-dlp dan FFmpeg terinstal"""
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

def download_audio(url, output_format="mp3", add_metadata=True, output_dir="downloads"):
    """
    Download audio YouTube dengan opsi metadata
    
    Args:
        url (str): URL video YouTube
        output_format (str): "mp3", "original", atau "lossless"
        add_metadata (bool): Tambah metadata ke file?
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
    postprocessors = []
    
    if output_format.lower() == "mp3":
        postprocessors.append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',  # 320kbps
        })
        print(f"\n🎵 Mode: MP3 320kbps")
    elif output_format.lower() == "lossless":
        postprocessors.append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
            'preferredquality': '0',
        })
        print(f"\n🎵 Mode: Lossless (FLAC)")
    else:  # original
        print(f"\n🎵 Mode: Original Format")
    
    # Tambah metadata jika dipilih
    if add_metadata and output_format.lower() != "original":
        postprocessors.append({
            'key': 'FFmpegMetadata',
        })
        print("🏷️  Metadata akan ditambahkan")
    else:
        print("🚫 Tanpa metadata")
    
    ydl_opts['postprocessors'] = postprocessors
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"⬇️ Memproses: {url}")
            ydl.download([url])
            print("✅ Selesai!")
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
    
    # Input dari user
    video_url = input("Masukkan URL YouTube: ").strip()
    if not video_url:
        print("❌ URL tidak boleh kosong!")
        sys.exit(1)
    
    print("\nPilih format output:")
    print("1. MP3 320kbps (rekomendasi)")
    print("2. Original Format (.webm/.m4a)")
    print("3. Lossless (FLAC)")
    format_choice = input("Pilihan (1/2/3): ").strip()
    
    format_map = {
        '1': 'mp3',
        '2': 'original',
        '3': 'lossless'
    }
    
    if format_choice not in format_map:
        print("❌ Pilihan format tidak valid!")
        sys.exit(1)
    
    # Tanya apakah ingin metadata
    if format_choice != '2':  # Kecuali original format
        meta_choice = input("\nTambahkan metadata? (y/n): ").strip().lower()
        add_metadata = meta_choice == 'y'
    else:
        add_metadata = False  # Original format tidak bisa tambah metadata
    
    # Download
    download_audio(
        url=video_url,
        output_format=format_map[format_choice],
        add_metadata=add_metadata
    )
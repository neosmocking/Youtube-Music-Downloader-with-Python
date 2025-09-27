import yt_dlp
import os

def download_original_format(url, output_dir="downloads"):
    """
    Download audio dalam format original (tanpa konversi)
    Format output: .webm, .m4a, atau format audio asli YouTube
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [],  # Tidak ada konversi
        'quiet': False,
        'no_warnings': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"⬇️ Mengunduh audio original dari: {url}")
            ydl.download([url])
            print("✅ Unduhan selesai!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def download_lossless_format(url, output_dir="downloads"):
    """
    Download audio dan konversi ke FLAC (lossless)
    Catatan: Kualitas tergantung sumber. Jika sumber lossy, FLAC hanya akan "membungkus" file lossy.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',  # Konversi ke FLAC
            'preferredquality': '0',   # Kualitas tertinggi (lossless)
        }],
        'quiet': False,
        'no_warnings': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"⬇️ Mengunduh dan konversi ke FLAC dari: {url}")
            ydl.download([url])
            print("✅ Konversi ke FLAC selesai!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

# Contoh penggunaan
if __name__ == "__main__":
    # video_url = "https://www.youtube.com/watch?v=VIDEO_ID"  # Ganti dengan URL YouTube
    video_url = "https://www.youtube.com/watch?v=0_68MvxV3LI"  # Ganti dengan URL YouTube
    
    # Pilih salah satu:
    download_original_format(video_url)  # Format original
    # download_lossless_format(video_url)  # Format lossless (FLAC)
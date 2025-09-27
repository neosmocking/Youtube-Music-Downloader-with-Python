import yt_dlp

def download_high_quality_mp3(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',  # 0 = highest quality (320kbps)
        }],
        'ffmpeg_location': '/usr/local/bin',  # Path to your FFmpeg
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Usage
download_high_quality_mp3("https://www.youtube.com/watch?v=RwRUV2PYWsw", "output_filename")
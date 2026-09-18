import os
import yt_dlp

# যেখানে ভিডিও ডাউনলোড হয়ে সেভ হবে
DOWNLOAD_DIR = 'downloaded_videos'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_video(url):
    print(f"[*] Downloading video from: {url}")
    
    # yt-dlp এর কনফিগারেশন (বেস্ট কোয়ালিটি এবং ওয়াটারমার্ক ছাড়া)
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'format': 'best',
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'Unknown Title')
            video_id = info.get('id', 'unknown_id')
            video_ext = info.get('ext', 'mp4')
            
            filepath = os.path.join(DOWNLOAD_DIR, f"{video_id}.{video_ext}")
            return filepath, video_title, video_id
    except Exception as e:
        print(f"[-] Download error: {e}")
        return None, None, None

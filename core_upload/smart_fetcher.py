import yt_dlp
from core_upload.history_checker import is_uploaded
from utils.downloader import download_video

def fetch_new_video(source_key, source_val):
    print(f"[*] Scanning {source_val['platform']} account: {source_val['account_name']}...")
    
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
        'playlistend': 20 
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(source_val['profile_url'], download=False)
            entries = info.get('entries', [])
            
            if not entries:
                print("[-] No videos found in this account.")
                return None
                
            for entry in entries:
                video_url = entry.get('url') or entry.get('webpage_url')
                video_id = entry.get('id')
                
                if not video_url: continue
                
                if not is_uploaded(source_key, video_id):
                    print(f"[+] Found un-uploaded video: {entry.get('title', video_id)}")
                    
                    filepath, title, v_id = download_video(video_url)
                    if filepath:
                        return {
                            "filepath": filepath,
                            "title": title,
                            "video_id": v_id,
                            "source_key": source_key
                        }
            
            print("[-] All recent videos from this account are already uploaded.")
            return None
    except Exception as e:
        print(f"[-] Error fetching videos: {e}")
        return None

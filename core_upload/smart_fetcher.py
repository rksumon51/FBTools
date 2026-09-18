import yt_dlp
from core_upload.history_checker import is_uploaded
from utils.downloader import download_video

def fetch_new_video(source):
    print(f"[*] Scanning {source['platform']} account: {source['account_name']}...")
    
    # প্রোফাইলের লেটেস্ট ২০টি ভিডিও চেক করবে (সময় বাঁচানোর জন্য)
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
        'playlistend': 20 
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(source['profile_url'], download=False)
            entries = info.get('entries', [])
            
            if not entries:
                print("[-] No videos found in this account.")
                return None
                
            # Smart Fetching Logic
            for entry in entries:
                video_url = entry.get('url') or entry.get('webpage_url')
                video_id = entry.get('id')
                
                if not video_url: continue
                
                # হিস্ট্রি চেক (Priority Logic)
                if not is_uploaded(source['_id'], video_id):
                    print(f"[+] Found un-uploaded video: {entry.get('title', video_id)}")
                    
                    # ভিডিওটি ডাউনলোড করা
                    filepath, title, v_id = download_video(video_url)
                    if filepath:
                        return {
                            "filepath": filepath,
                            "title": title,
                            "video_id": v_id,
                            "source_id": source['_id']
                        }
            
            print("[-] All recent videos from this account are already uploaded.")
            return None
    except Exception as e:
        print(f"[-] Error fetching videos: {e}")
        return None

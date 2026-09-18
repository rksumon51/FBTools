import os
import requests
from database.db_connect import get_db_url
from core_upload.smart_fetcher import fetch_new_video
from core_upload.history_checker import save_history

def upload_to_facebook(page_val, video_data):
    print(f"[*] Uploading to Facebook Page: {page_val['page_name']}...")
    
    url = f"https://graph.facebook.com/v18.0/{page_val['page_id']}/videos"
    
    payload = {
        'title': video_data['title'],
        'description': video_data['title'],
        'access_token': page_val['access_token']
    }
    
    try:
        with open(video_data['filepath'], 'rb') as f:
            files = {'file': f}
            print("[*] Uploading in progress... Please wait.")
            response = requests.post(url, data=payload, files=files)
            result = response.json()
            
            if 'id' in result:
                print(f"[+] Successfully uploaded! FB Video ID: {result['id']}")
                return True
            else:
                print(f"[-] Facebook API Error: {result}")
                return False
    except Exception as e:
        print(f"[-] Error during upload: {e}")
        return False
    finally:
        if os.path.exists(video_data['filepath']):
            os.remove(video_data['filepath'])

def run():
    url = get_db_url()
    if not url: return
    
    try:
        mappings_res = requests.get(f"{url}mappings.json").json() or {}
        pages_res = requests.get(f"{url}pages.json").json() or {}
        sources_res = requests.get(f"{url}sources.json").json() or {}
    except Exception:
        print("[-] Error fetching data from Firebase.")
        return
        
    if not mappings_res:
        print("[-] No mappings found. Please map accounts from Option [6].")
        return
        
    print("\n===============================")
    print("      LIVE UPLOAD STARTED")
    print("===============================")
    
    # ম্যাপিং অনুযায়ী কাজ শুরু
    for page_id_str, mapping in mappings_res.items():
        # পেজের বিস্তারিত ডেটা খুঁজে বের করা
        page_val = None
        for p_key, p_val in pages_res.items():
            if p_val['page_id'] == page_id_str:
                page_val = p_val
                break
                
        if not page_val: continue
        
        print(f"\n=============================================")
        print(f"[*] Processing FB Page: {page_val['page_name']}")
        print(f"=============================================")
        
        for source_key in mapping.get('source_ids', []):
            source_val = sources_res.get(source_key)
            if not source_val: continue
            
            video_data = fetch_new_video(source_key, source_val)
            
            if video_data:
                success = upload_to_facebook(page_val, video_data)
                
                if success:
                    save_history(source_key, video_data['video_id'], video_data['title'])
                    print("[+] Done for this source.\n")
                else:
                    print("[-] Upload failed. Will retry next time.\n")
            else:
                print(f"[*] Skipping source {source_val['account_name']}, no new videos found.\n")
    
    print("[*] All mappings processed successfully!")

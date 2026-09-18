import os
import requests
from database.db_connect import get_db
from core_upload.smart_fetcher import fetch_new_video
from core_upload.history_checker import save_history

def upload_to_facebook(page, video_data):
    print(f"[*] Uploading to Facebook Page: {page['page_name']}...")
    
    # Facebook Graph API (v18.0)
    url = f"https://graph.facebook.com/v18.0/{page['page_id']}/videos"
    
    # সোর্সের অরিজিনাল টাইটেলটাই ক্যাপশন হিসেবে যাবে
    payload = {
        'title': video_data['title'],
        'description': video_data['title'],
        'access_token': page['access_token']
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
        # স্টোরেজ বাঁচাতে আপলোড শেষে ফাইল ডিলিট করে দেওয়া হবে
        if os.path.exists(video_data['filepath']):
            os.remove(video_data['filepath'])

def run():
    db = get_db()
    if db is None: return
    
    mappings = list(db.mappings.find())
    if not mappings:
        print("[-] No mappings found. Please map accounts from Option [6].")
        return
        
    print("\n===============================")
    print("      LIVE UPLOAD STARTED")
    print("===============================")
    
    # ম্যাপিং অনুযায়ী কাজ শুরু
    for mapping in mappings:
        page_id = mapping['page_id']
        page = db.pages.find_one({"page_id": page_id})
        
        if not page: continue
        
        print(f"\n=============================================")
        print(f"[*] Processing FB Page: {page['page_name']}")
        print(f"=============================================")
        
        for source_id in mapping['source_ids']:
            from bson.objectid import ObjectId
            source = db.sources.find_one({"_id": ObjectId(source_id)})
            if not source: continue
            
            # লেটেস্ট আনকোরা ভিডিও খুঁজে ডাউনলোড করা
            video_data = fetch_new_video(source)
            
            if video_data:
                # ভিডিওটি ফেসবুকে আপলোড করা
                success = upload_to_facebook(page, video_data)
                
                if success:
                    # সফল হলে হিস্ট্রিতে সেভ করা
                    save_history(source_id, video_data['video_id'], video_data['title'])
                    print("[+] Done for this source.\n")
                else:
                    print("[-] Upload failed. Will retry next time.\n")
            else:
                print(f"[*] Skipping source {source['account_name']}, no new videos found.\n")
    
    print("[*] All mappings processed successfully!")

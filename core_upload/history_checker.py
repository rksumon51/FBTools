import requests
from database.db_connect import get_db_url

def safe_key(key):
    return str(key).replace('.', '_').replace('#', '_').replace('$', '_').replace('[', '_').replace(']', '_')

def is_uploaded(source_key, video_id):
    url = get_db_url()
    if not url: return False
    
    v_id = safe_key(video_id)
    try:
        res = requests.get(f"{url}history/{source_key}/{v_id}.json").json()
        return True if res else False
    except Exception:
        return False

def save_history(source_key, video_id, title):
    url = get_db_url()
    if not url: return
    
    v_id = safe_key(video_id)
    try:
        requests.put(f"{url}history/{source_key}/{v_id}.json", json={"title": title})
        print(f"[+] Saved to Firebase History: {title}")
    except Exception as e:
        print(f"[-] Failed to save history: {e}")

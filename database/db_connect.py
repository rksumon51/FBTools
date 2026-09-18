import os
import json
import requests

CONFIG_FILE = 'db_config.json'
firebase_url = None

def get_url():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            return data.get('firebase_url')
    return None

def save_url(url):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'firebase_url': url}, f)

def connect():
    global firebase_url
    url = get_url()
    
    if not url:
        print("\n[!] Firebase URL is not configured yet.")
        print("Example: https://your-project-default-rtdb.firebaseio.com/")
        url = input("Enter your Firebase Realtime Database URL: ").strip()
        if not url:
            print("[-] URL cannot be empty.")
            return False
            
    # URL এর শেষে '/' না থাকলে যোগ করে দেওয়া
    if not url.endswith('/'):
        url += '/'
        
    try:
        print("[*] Trying to connect to Firebase Cloud...")
        # ফায়ারবেসের সাথে কানেকশন টেস্ট করা
        response = requests.get(url + '.json')
        
        if response.status_code == 200 or response.status_code == 401:
            firebase_url = url
            save_url(url)
            return True
        else:
            print(f"[-] Connection failed. Status code: {response.status_code}")
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
            return False
    except Exception as e:
        print(f"[-] An error occurred: {e}")
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        return False

# অন্যান্য ফাইল থেকে ফায়ারবেস URL পাওয়ার জন্য
def get_db_url():
    return firebase_url

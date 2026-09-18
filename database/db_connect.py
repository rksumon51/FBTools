import os
import json
import pymongo
from pymongo.errors import ConnectionFailure

# লোকাল ফাইল যেখানে MongoDB URI সেভ থাকবে (যাতে বারবার দিতে না হয়)
# এই ফাইলটি .gitignore এ থাকায় গিটহাবে আপলোড হবে না
CONFIG_FILE = 'db_config.json'
client = None
db = None

def get_uri():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            return data.get('mongo_uri')
    return None

def save_uri(uri):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'mongo_uri': uri}, f)

def connect():
    global client, db
    
    uri = get_uri()
    
    # যদি আগে থেকে লিংক সেভ করা না থাকে, তবে ইউজারের কাছে চাইবে
    if not uri:
        print("\n[!] MongoDB URI is not configured yet.")
        uri = input("Enter your MongoDB Atlas Connection String (URI): ").strip()
        if not uri:
            print("[-] URI cannot be empty.")
            return False
            
    try:
        print("[*] Trying to connect to MongoDB Atlas...")
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        # কানেকশন ঠিক আছে কি না তা চেক করা
        client.admin.command('ping')
        
        # আপনার ডাটাবেসের নাম 'fb_auto_tools' রাখা হলো
        db = client['fb_auto_tools']
        
        # কানেকশন সফল হলে ভবিষ্যতে ব্যবহারের জন্য URI সেভ করে রাখা
        save_uri(uri)
        return True
        
    except ConnectionFailure:
        print("[-] Connection failed! Please check your URI or Internet connection.")
        # ভুল লিংক হলে ফাইলটি ডিলিট করে দেবে, যাতে পরের বার আবার নতুন লিংক চায়
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE) 
        return False
    except Exception as e:
        print(f"[-] An error occurred: {e}")
        return False

# অন্যান্য ফাইল থেকে ডাটাবেস এক্সেস করার জন্য এই ফাংশনটি কল করতে হবে
def get_db():
    return db

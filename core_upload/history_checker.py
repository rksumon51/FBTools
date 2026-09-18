from database.db_connect import get_db

def is_uploaded(source_id, video_id):
    db = get_db()
    if db is None: return False
    
    # ডাটাবেসে চেক করা হচ্ছে এই সোর্স থেকে ভিডিওটি আগে আপলোড হয়েছে কি না
    record = db.history.find_one({
        "source_id": str(source_id), 
        "video_id": str(video_id)
    })
    return True if record else False

def save_history(source_id, video_id, title):
    db = get_db()
    if db is None: return
    
    # আপলোড সফল হলে ডাটাবেসে টাইটেল সহ সেভ করা
    db.history.insert_one({
        "source_id": str(source_id),
        "video_id": str(video_id),
        "title": title
    })
    print(f"[+] Saved to Database History: {title}")

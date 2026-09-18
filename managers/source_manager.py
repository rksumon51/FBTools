from database.db_connect import get_db

def add_source():
    db = get_db()
    if db is None: return
    
    print("\n--- Add New Source Account ---")
    platform = input("Enter Platform (e.g., TikTok / YT): ").strip().upper()
    account_name = input("Enter Account Name (e.g., YK_Gaming): ").strip()
    profile_url = input("Enter Profile or Channel URL: ").strip()
    
    if not platform or not account_name or not profile_url:
        print("[-] All fields are required!")
        return
        
    if db.sources.find_one({"profile_url": profile_url}):
        print("[-] This account URL is already added!")
        return
        
    db.sources.insert_one({
        "platform": platform,
        "account_name": account_name,
        "profile_url": profile_url
    })
    print(f"[+] {platform} Account '{account_name}' added successfully!")

def view_sources():
    db = get_db()
    if db is None: return []
    
    sources = list(db.sources.find())
    print("\n--- Saved Source Accounts ---")
    if not sources:
        print("[-] No sources found. Please add a TikTok or YT account first.")
        return []
        
    for idx, src in enumerate(sources, 1):
        print(f"[{idx}] {src['platform']} | {src['account_name']} ({src['profile_url']})")
    return sources
    
def delete_source():
    db = get_db()
    sources = view_sources()
    if not sources: return
    
    try:
        choice = int(input("\nEnter the number of the account to delete (0 to cancel): "))
        if choice == 0: return
        if 1 <= choice <= len(sources):
            selected_source = sources[choice-1]
            db.sources.delete_one({"_id": selected_source['_id']})
            print(f"[+] Account '{selected_source['account_name']}' deleted successfully!")
        else:
            print("[-] Invalid selection.")
    except ValueError:
        print("[-] Please enter a valid number.")

def menu():
    while True:
        print("\n===============================")
        print("   TIKTOK & YT SOURCE MANAGER")
        print("===============================")
        print("[1] View All Accounts")
        print("[2] Add New Account")
        print("[3] Delete Account")
        print("-------------------------------")
        print("[0] Back to Main Menu")
        
        choice = input("\nSelect Option: ")
        if choice == '1':
            view_sources()
        elif choice == '2':
            add_source()
        elif choice == '3':
            delete_source()
        elif choice == '0':
            break
        else:
            print("[-] Invalid option. Try again.")

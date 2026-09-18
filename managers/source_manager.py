import requests
from database.db_connect import get_db_url

def add_source():
    url = get_db_url()
    if not url: return
    
    print("\n--- Add New Source Account ---")
    platform = input("Enter Platform (e.g., TikTok / YT): ").strip().upper()
    account_name = input("Enter Account Name (e.g., YK_Gaming): ").strip()
    profile_url = input("Enter Profile or Channel URL: ").strip()
    
    if not platform or not account_name or not profile_url:
        print("[-] All fields are required!")
        return
        
    try:
        res = requests.get(f"{url}sources.json").json()
        if res:
            for key, val in res.items():
                if val.get('profile_url') == profile_url:
                    print("[-] This account URL is already added!")
                    return
    except Exception:
        pass
        
    data = {
        "platform": platform,
        "account_name": account_name,
        "profile_url": profile_url
    }
    requests.post(f"{url}sources.json", json=data)
    print(f"[+] {platform} Account '{account_name}' added successfully!")

def view_sources():
    url = get_db_url()
    if not url: return []
    
    try:
        res = requests.get(f"{url}sources.json").json()
        print("\n--- Saved Source Accounts ---")
        if not res:
            print("[-] No sources found. Please add an account first.")
            return []
            
        sources = []
        for idx, (key, val) in enumerate(res.items(), 1):
            print(f"[{idx}] {val['platform']} | {val['account_name']} ({val['profile_url']})")
            sources.append((key, val))
        return sources
    except Exception as e:
        print("[-] Error fetching sources from Firebase.")
        return []
    
def delete_source():
    url = get_db_url()
    sources = view_sources()
    if not sources: return
    
    try:
        choice = int(input("\nEnter the number of the account to delete (0 to cancel): "))
        if choice == 0: return
        if 1 <= choice <= len(sources):
            selected_key, selected_source = sources[choice-1]
            requests.delete(f"{url}sources/{selected_key}.json")
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

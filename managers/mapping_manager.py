import requests
from database.db_connect import get_db_url

def create_mapping():
    url = get_db_url()
    if not url: return
    
    try:
        pages_res = requests.get(f"{url}pages.json").json() or {}
        sources_res = requests.get(f"{url}sources.json").json() or {}
    except Exception:
        print("[-] Error connecting to Firebase.")
        return
        
    if not pages_res:
        print("[-] No Facebook pages found. Add a page first from Option [4].")
        return
    if not sources_res:
        print("[-] No source accounts found. Add an account first from Option [5].")
        return
        
    pages = list(pages_res.items())
    sources = list(sources_res.items())
    
    print("\n--- Select a Facebook Page ---")
    for idx, (p_key, p_val) in enumerate(pages, 1):
        print(f"[{idx}] {p_val['page_name']} (ID: {p_val['page_id']})")
        
    try:
        p_choice = int(input("\nSelect Page Number: "))
        if p_choice < 1 or p_choice > len(pages):
            print("[-] Invalid selection.")
            return
        selected_page_key, selected_page_val = pages[p_choice-1]
        page_id_str = selected_page_val['page_id']
        
        print("\n--- Select Source Accounts to Link ---")
        for idx, (s_key, s_val) in enumerate(sources, 1):
            print(f"[{idx}] {s_val['platform']} | {s_val['account_name']}")
            
        print("\n(You can select multiple by using commas, e.g., 1,3)")
        s_choices = input("Select Source Numbers: ").split(',')
        
        selected_source_ids = []
        for sc in s_choices:
            sc = sc.strip()
            if sc.isdigit() and 1 <= int(sc) <= len(sources):
                selected_source_ids.append(sources[int(sc)-1][0])
                
        if not selected_source_ids:
            print("[-] No valid sources selected.")
            return
            
        # Firebase এ ম্যাপিং সেভ করা (page_id কে মেইন 'কি' হিসেবে ব্যবহার করে)
        mapping_data = {
            "page_name": selected_page_val['page_name'],
            "source_ids": selected_source_ids
        }
        requests.patch(f"{url}mappings.json", json={page_id_str: mapping_data})
        print(f"\n[+] Successfully linked {len(selected_source_ids)} source(s) to Page '{selected_page_val['page_name']}'!")
        
    except ValueError:
        print("[-] Invalid input. Please enter numbers.")

def view_mappings():
    url = get_db_url()
    if not url: return []
    
    try:
        mappings_res = requests.get(f"{url}mappings.json").json() or {}
        sources_res = requests.get(f"{url}sources.json").json() or {}
    except Exception:
        print("[-] Error fetching data from Firebase.")
        return []
        
    print("\n--- Current Account Links (Mappings) ---")
    if not mappings_res:
        print("[-] No links found.")
        return []
        
    idx = 1
    for page_id, mapping in mappings_res.items():
        print(f"\n[{idx}] FB Page: {mapping.get('page_name', 'Unknown')}")
        print("    Linked Sources:")
        for src_key in mapping.get('source_ids', []):
            src = sources_res.get(src_key)
            if src:
                print(f"      - {src['platform']} | {src['account_name']}")
            else:
                print(f"      - [Deleted Source]")
        idx += 1
    return mappings_res

def menu():
    while True:
        print("\n===============================")
        print("    LINK ACCOUNT (MAPPING)")
        print("===============================")
        print("[1] View Current Links")
        print("[2] Create New Link (Map Sources to Page)")
        print("-------------------------------")
        print("[0] Back to Main Menu")
        
        choice = input("\nSelect Option: ")
        if choice == '1':
            view_mappings()
        elif choice == '2':
            create_mapping()
        elif choice == '0':
            break
        else:
            print("[-] Invalid option. Try again.")

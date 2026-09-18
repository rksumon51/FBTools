from database.db_connect import get_db

def create_mapping():
    db = get_db()
    if db is None: return
    
    pages = list(db.pages.find())
    sources = list(db.sources.find())
    
    if not pages:
        print("[-] No Facebook pages found. Add a page first from Option [4].")
        return
    if not sources:
        print("[-] No source accounts found. Add an account first from Option [5].")
        return
        
    print("\n--- Select a Facebook Page ---")
    for idx, page in enumerate(pages, 1):
        print(f"[{idx}] {page['page_name']} (ID: {page['page_id']})")
        
    try:
        p_choice = int(input("\nSelect Page Number: "))
        if p_choice < 1 or p_choice > len(pages):
            print("[-] Invalid selection.")
            return
        selected_page = pages[p_choice-1]
        
        print("\n--- Select Source Accounts to Link ---")
        for idx, src in enumerate(sources, 1):
            print(f"[{idx}] {src['platform']} | {src['account_name']}")
            
        print("\n(You can select multiple by using commas, e.g., 1,3)")
        s_choices = input("Select Source Numbers: ").split(',')
        
        selected_source_ids = []
        for sc in s_choices:
            sc = sc.strip()
            if sc.isdigit() and 1 <= int(sc) <= len(sources):
                selected_source_ids.append(str(sources[int(sc)-1]['_id']))
                
        if not selected_source_ids:
            print("[-] No valid sources selected.")
            return
            
        # ডাটাবেসে সেভ বা আপডেট করা
        db.mappings.update_one(
            {"page_id": selected_page['page_id']},
            {
                "$set": {
                    "page_name": selected_page['page_name'], 
                    "source_ids": selected_source_ids
                }
            },
            upsert=True
        )
        print(f"\n[+] Successfully linked {len(selected_source_ids)} source(s) to Page '{selected_page['page_name']}'!")
        
    except ValueError:
        print("[-] Invalid input. Please enter numbers.")

def view_mappings():
    db = get_db()
    if db is None: return []
    
    mappings = list(db.mappings.find())
    print("\n--- Current Account Links (Mappings) ---")
    if not mappings:
        print("[-] No links found.")
        return []
        
    for idx, mapping in enumerate(mappings, 1):
        print(f"\n[{idx}] FB Page: {mapping['page_name']}")
        print("    Linked Sources:")
        for src_id in mapping['source_ids']:
            from bson.objectid import ObjectId
            src = db.sources.find_one({"_id": ObjectId(src_id)})
            if src:
                print(f"      - {src['platform']} | {src['account_name']}")
    return mappings

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

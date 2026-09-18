from database.db_connect import get_db

def add_page():
    db = get_db()
    if db is None: return
    
    print("\n--- Add New Facebook Page ---")
    page_name = input("Enter Page Name: ").strip()
    page_id = input("Enter Page ID: ").strip()
    access_token = input("Enter Page Access Token: ").strip()
    
    if not page_name or not page_id or not access_token:
        print("[-] All fields are required!")
        return
        
    # চেক করে দেখবে এই পেজ আইডিটি আগে থেকেই ডাটাবেসে আছে কি না
    if db.pages.find_one({"page_id": page_id}):
        print(f"[-] Page with ID '{page_id}' already exists in database!")
        return
        
    # ডাটাবেসে নতুন পেজ সেভ করা
    db.pages.insert_one({
        "page_name": page_name,
        "page_id": page_id,
        "access_token": access_token
    })
    print(f"[+] Page '{page_name}' added successfully to MongoDB!")

def view_pages():
    db = get_db()
    if db is None: return []
    
    pages = list(db.pages.find())
    print("\n--- Saved Facebook Pages ---")
    if not pages:
        print("[-] No pages found. Please add a page first.")
        return []
        
    for idx, page in enumerate(pages, 1):
        print(f"[{idx}] {page['page_name']} (ID: {page['page_id']})")
    return pages
    
def delete_page():
    db = get_db()
    pages = view_pages()
    if not pages: return
    
    try:
        choice = int(input("\nEnter the number of the page to delete (0 to cancel): "))
        if choice == 0: return
        if 1 <= choice <= len(pages):
            selected_page = pages[choice-1]
            # ডাটাবেস থেকে পেজ ডিলিট করা
            db.pages.delete_one({"_id": selected_page['_id']})
            # এই পেজের সাথে লিংক করা কোনো ম্যাপিং থাকলে সেটাও ডিলিট করে দেওয়া
            db.mappings.delete_many({"page_id": selected_page['page_id']})
            print(f"[+] Page '{selected_page['page_name']}' deleted successfully!")
        else:
            print("[-] Invalid selection.")
    except ValueError:
        print("[-] Please enter a valid number.")

def menu():
    while True:
        print("\n===============================")
        print("       FACEBOOK PAGE MANAGER")
        print("===============================")
        print("[1] View All Pages")
        print("[2] Add New Page")
        print("[3] Delete Page")
        print("-------------------------------")
        print("[0] Back to Main Menu")
        
        choice = input("\nSelect Option: ")
        if choice == '1':
            view_pages()
        elif choice == '2':
            add_page()
        elif choice == '3':
            delete_page()
        elif choice == '0':
            break
        else:
            print("[-] Invalid option. Try again.")

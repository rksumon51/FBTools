import requests
from database.db_connect import get_db_url

def add_page():
    url = get_db_url()
    if not url: return
    
    print("\n--- Add New Facebook Page ---")
    page_name = input("Enter Page Name: ").strip()
    page_id = input("Enter Page ID: ").strip()
    access_token = input("Enter Page Access Token: ").strip()
    
    if not page_name or not page_id or not access_token:
        print("[-] All fields are required!")
        return
        
    # চেক করে দেখবে এই পেজ আইডিটি আগে থেকেই ডাটাবেসে আছে কি না
    try:
        res = requests.get(f"{url}pages.json").json()
        if res:
            for key, val in res.items():
                if val.get('page_id') == page_id:
                    print(f"[-] Page with ID '{page_id}' already exists in database!")
                    return
    except Exception:
        pass
        
    # ডাটাবেসে নতুন পেজ সেভ করা
    data = {
        "page_name": page_name,
        "page_id": page_id,
        "access_token": access_token
    }
    requests.post(f"{url}pages.json", json=data)
    print(f"[+] Page '{page_name}' added successfully to Firebase!")

def view_pages():
    url = get_db_url()
    if not url: return []
    
    try:
        res = requests.get(f"{url}pages.json").json()
        print("\n--- Saved Facebook Pages ---")
        if not res:
            print("[-] No pages found. Please add a page first.")
            return []
            
        pages = []
        for idx, (key, val) in enumerate(res.items(), 1):
            print(f"[{idx}] {val['page_name']} (ID: {val['page_id']})")
            # ডিলিট করার সুবিধার জন্য ফায়ারবেসের ইউনিক কি (key) সহ সেভ রাখা হচ্ছে
            pages.append((key, val))
        return pages
    except Exception as e:
        print("[-] Error fetching pages from Firebase.")
        return []
    
def delete_page():
    url = get_db_url()
    pages = view_pages()
    if not pages: return
    
    try:
        choice = int(input("\nEnter the number of the page to delete (0 to cancel): "))
        if choice == 0: return
        if 1 <= choice <= len(pages):
            selected_key, selected_page = pages[choice-1]
            
            # ডাটাবেস থেকে পেজ ডিলিট করা
            requests.delete(f"{url}pages/{selected_key}.json")
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

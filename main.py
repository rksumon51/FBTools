import os
import sys
import subprocess

from database import db_connect
# from managers import page_manager
# from managers import source_manager
# from managers import mapping_manager
# from core_upload import upload_live
# from core_upload import upload_schedule

DB_CONNECTED = False 

def clear_screen():
    os.system('clear')

def check_connection():
    if not DB_CONNECTED:
        print("\n[!] Error: Please connect Firebase first using Option [3]")
        input("Press Enter to return to menu...")
        return False
    return True

def update_tool():
    print("\n[*] Fetching latest updates from GitHub...")
    try:
        subprocess.run(["git", "pull"], check=True)
        print("[+] Update successful! The codebase is now up to date.")
        print("[*] Please restart the tool by typing 'fbtools'.")
        sys.exit()
    except subprocess.CalledProcessError:
        print("[-] Update failed. Make sure this directory is a valid git repository.")
    input("Press Enter to continue...")

def main_menu():
    global DB_CONNECTED
    while True:
        clear_screen()
        status = "🟢 Connected" if DB_CONNECTED else "🔴 Disconnected"
        
        print("=================================================")
        print("             FB AUTO UPLOAD TOOLS (v1.0)")
        print(f"         [Firebase Status: {status}]")
        print("=================================================")
        print("\n[1] Start Upload (Without Schedule / Live)")
        print("[2] Start Upload (With Schedule)")
        print("-------------------------------------------------")
        print("[3] Connect Firebase Database")
        print("[4] Facebook Page (Add/Edit/Delete)")
        print("[5] TikTok & YT Account (Add/Edit/Delete)")
        print("[6] Link Account (Mapping Sources to Pages)")
        print("-------------------------------------------------")
        print("[7] Update Tool (Pull latest from GitHub)")
        print("[0] Exit\n")
        
        choice = input("Select Option: ")
        
        if choice == '1':
            if check_connection():
                print("[*] Loading Live Upload Module...")
                # upload_live.run()
                input("Press Enter...")
        elif choice == '2':
            if check_connection():
                print("[*] Loading Scheduled Upload Module...")
                # upload_schedule.run()
                input("Press Enter...")
        elif choice == '3':
            print("[*] Connecting to Firebase...")
            DB_CONNECTED = db_connect.connect()
            if DB_CONNECTED:
                print("[+] Firebase Connected Successfully!")
            input("Press Enter...")
        elif choice == '4':
            if check_connection():
                print("[*] Opening Page Manager...")
                # page_manager.menu() 
                input("Press Enter...")
        elif choice == '5':
            if check_connection():
                print("[*] Opening Source Manager...")
                # source_manager.menu()
                input("Press Enter...")
        elif choice == '6':
            if check_connection():
                print("[*] Opening Mapping Manager...")
                # mapping_manager.menu()
                input("Press Enter...")
        elif choice == '7':
            update_tool()
        elif choice == '0':
            print("[*] Exiting tool...")
            sys.exit()
        else:
            print("[-] Invalid Option! Please select between 0-7.")
            input("Press Enter...")

if __name__ == "__main__":
    main_menu()

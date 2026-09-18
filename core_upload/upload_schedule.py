import time
from core_upload import upload_live

def run():
    print("\n===============================")
    print("    SCHEDULE UPLOAD STARTED")
    print("===============================")
    
    try:
        interval = int(input("[*] Enter time interval between uploads (in minutes): "))
        if interval <= 0:
            print("[-] Interval must be greater than 0.")
            return
    except ValueError:
        print("[-] Invalid input! Please enter a valid number.")
        return
        
    print(f"\n[*] Bot is now running in Schedule Mode (Every {interval} minutes).")
    print("[*] Tip: Press CTRL+C to stop and return to the main menu.\n")
    
    try:
        while True:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n=============================================")
            print(f"[*] Starting upload cycle at: {current_time}")
            print(f"=============================================")
            
            # আমাদের আগে তৈরি করা লাইভ আপলোড লজিকটি কল করা হচ্ছে
            upload_live.run()
            
            print(f"\n[*] Cycle complete! Bot is sleeping for {interval} minutes...")
            print(f"[*] Next cycle will start automatically. Do not close Termux.")
            
            # মিনিটকে সেকেন্ডে কনভার্ট করে টুলটিকে স্লিপ (sleep) মোডে রাখা হচ্ছে
            time.sleep(interval * 60)
            
    except KeyboardInterrupt:
        print("\n\n[*] Schedule Mode Stopped by user. Returning to menu...")

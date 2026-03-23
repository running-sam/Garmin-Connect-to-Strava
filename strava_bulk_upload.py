import os
import time
import shutil
import datetime
from collections import defaultdict
from stravalib.client import Client

# --------------------------
# CONFIGURATION
# --------------------------
CLIENT_ID = "########" #add your Client ID here
CLIENT_SECRET = "####################" #add your Client Secret here
FOLDER = "###[update with route to folder where exports are stored]########"
DONE_FOLDER = os.path.join(FOLDER, "Done")

if not os.path.exists(DONE_FOLDER):
    os.makedirs(DONE_FOLDER)

# --------------------------
# STRAVA AUTH
# --------------------------
client = Client()
auth_url = client.authorization_url(
    client_id=CLIENT_ID,
    redirect_uri="http://localhost",
    scope=['read', 'activity:write']
)

print("\n1. Open this URL:\n", auth_url)
code = input("\n2. Paste code here: ").strip()

token = client.exchange_code_for_token(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=code
)
client.access_token = token["access_token"]
print("\n--- Authenticated: Turbo Newest-First Mode ---\n")

# --------------------------
# INDEXING
# --------------------------
file_groups = defaultdict(list)
for f in os.listdir(FOLDER):
    if f.lower().endswith((".fit", ".gpx", ".tcx")):
        name, ext = os.path.splitext(f)
        file_groups[name].append(ext.lower())

# --------------------------
# UPLOAD LOOP (TURBO)
# --------------------------
for activity_name, extensions in sorted(file_groups.items(), reverse=True):
    if ".fit" in extensions:
        best_ext = ".fit"
    elif ".tcx" in extensions:
        best_ext = ".tcx"
    else:
        best_ext = ".gpx"

    best_file = activity_name + best_ext
    path = os.path.join(FOLDER, best_file)
    
    if not os.path.exists(path):
        continue

    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Processing: {best_file}")

    try:
        with open(path, "rb") as f:
            upload = client.upload_activity(
                activity_file=f,
                data_type=best_ext[1:],
                name=best_file
            )

            # --- TURBO POLLING ---
            # We check immediately. If it's a duplicate, it usually fails instantly.
            while not upload.is_complete:
                upload.poll()
                if upload.is_error:
                    break
                time.sleep(1) # Fast polling for status

            if upload.is_error:
                err_msg = str(upload.error).lower()
                if "duplicate" in err_msg or "activities/" in err_msg:
                    print(f"  >> Duplicate. Quick-moving to Done.")
                    for ext in extensions:
                        src = os.path.join(FOLDER, activity_name + ext)
                        if os.path.exists(src):
                            shutil.move(src, os.path.join(DONE_FOLDER, activity_name + ext))
                    # NO long sleep for duplicates!
                    time.sleep(0.5) 
                else:
                    print(f"  !! Upload Error: {upload.error}")
            else:
                print(f"  ✅ SUCCESS! New activity uploaded.")
                for ext in extensions:
                    src = os.path.join(FOLDER, activity_name + ext)
                    if os.path.exists(src):
                        shutil.move(src, os.path.join(DONE_FOLDER, activity_name + ext))
                
                # SAFETY SLEEP: Only slow down when we actually ADD data
                print("  Waiting 15s to respect API limits...")
                time.sleep(15)

    except Exception as e:
        error_str = str(e).lower()
        if "duplicate" in error_str or "activities/" in error_str:
            print(f"  >> Duplicate (Exception). Quick-moving.")
            for ext in extensions:
                src = os.path.join(FOLDER, activity_name + ext)
                if os.path.exists(src):
                    shutil.move(src, os.path.join(DONE_FOLDER, activity_name + ext))
        elif "rate limit" in error_str or "429" in error_str:
            print("\n🛑 Daily/15-min Limit hit. Taking a 15 min nap...")
            time.sleep(900)
        else:
            print(f"  System Error: {e}")

print("\n--- Finished! ---")

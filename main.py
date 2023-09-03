# TSKSW (TEMUKAN SEMUA KATA SANDI WIFI)
# - ROFI -

import os
import subprocess
import re
import datetime

os.system("cls")

hasil_perintah = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
nama_profil = re.findall("All User Profile     : (.*)\r", hasil_perintah)

daftar_wifi = []

if len(nama_profil) != 0:
    for nama in nama_profil:
        info_profil = subprocess.run(["netsh", "wlan", "show", "profil", nama], capture_output=True).stdout.decode()
        if re.search("Security key           : Absent", info_profil):
            continue
        else:
            info_kunci_pass = subprocess.run(["netsh", "wlan", "show", "profil", nama, "key=clear"], capture_output=True).stdout.decode()
            kata_sandi = re.search("Key Content            : (.*)\r", info_kunci_pass)
            if kata_sandi is None:
                daftar_wifi.append(f"""SSID: {nama}
Kata Sandi: None
""")
            else:
                daftar_wifi.append(f""" SSID: {nama}
 Kata Sandi: {kata_sandi[1]}
 """)

    for wifi in daftar_wifi:
        print(f"{wifi}")

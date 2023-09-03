# TSKSW (TEMUKAN SEMUA KATA SANDI WIFI)
# - ROFI -

import os
import subprocess
import re
import json
import datetime

os.system("cls")

sekarang = datetime.datetime.now()
nama_file = f"{sekarang.strftime('%d-%m-%Y_%H-%M-%S')}.json"
hasil_perintah = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
nama_profil = re.findall("All User Profile     : (.*)\r", hasil_perintah)

daftar_wifi = []

if len(nama_profil) != 0:
    
    for nama in nama_profil:
        profil_wifi = {}
        info_profil = subprocess.run(["netsh", "wlan", "show", "profil", nama], capture_output=True).stdout.decode()
        
        if re.search("Security key           : Absent", info_profil):
            continue    
        
        else:
            profil_wifi["SSID"] = nama
            info_kunci_pass = subprocess.run(["netsh", "wlan", "show", "profil", nama, "key=clear"], capture_output=True).stdout.decode()
            kata_sandi = re.search("Key Content            : (.*)\r", info_kunci_pass)  
            
            if kata_sandi is None:
                profil_wifi["Kata Sandi"] = None  
            
            else:
                profil_wifi["Kata Sandi"] = kata_sandi[1]
            
            daftar_wifi.append(profil_wifi)

hasil_json = json.dumps(daftar_wifi, indent=4)

print(f"\n{hasil_json}")

with open(nama_file, 'w') as file:
    file.write(hasil_json)

print(f"\nHasil telah disimpan dalam file: {nama_file}\n")

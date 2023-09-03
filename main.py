import subprocess
import re
import json
import datetime

# Mendapatkan timestamp saat ini
sekarang = datetime.datetime.now()
nama_file = f"hasil_wifi_{sekarang.strftime('%Y-%m-%d_%H-%M-%S')}.json"

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
            profil_wifi["ssid"] = nama
            info_kunci_pass = subprocess.run(["netsh", "wlan", "show", "profil", nama, "key=clear"], capture_output=True).stdout.decode()
            kata_sandi = re.search("Key Content            : (.*)\r", info_kunci_pass)
            if kata_sandi is None:
                profil_wifi["kata_sandi"] = None
            else:
                profil_wifi["kata_sandi"] = kata_sandi[1]
            daftar_wifi.append(profil_wifi)

# Mengkonversi daftar_wifi menjadi format JSON
json_hasil = json.dumps(daftar_wifi, indent=4)

# Menyimpan hasil JSON ke dalam file
with open(nama_file, 'w') as file:
    file.write(json_hasil)

print(f"Hasil telah disimpan dalam file: {nama_file}")
            

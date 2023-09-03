import subprocess
import re
import json
import datetime

def get_wifi_profiles():
    # Mendapatkan timestamp saat ini
    sekarang = datetime.datetime.now()
    nama_file = f"hasil_wifi_{sekarang.strftime('%Y-%m-%d_%H-%M-%S')}.json"

    try:
        hasil_perintah = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True, check=True).stdout

        nama_profil = re.findall("All User Profile     : (.*)\r", hasil_perintah)

        daftar_wifi = []

        for nama in nama_profil:
            profil_wifi = {}
            info_profil = subprocess.run(["netsh", "wlan", "show", "profil", nama], capture_output=True, text=True, check=True).stdout
            if "Security key           : Absent" in info_profil:
                continue
            else:
                profil_wifi["ssid"] = nama
                info_kunci_pass = subprocess.run(["netsh", "wlan", "show", "profil", nama, "key=clear"], capture_output=True, text=True, check=True).stdout
                kata_sandi = re.search("Key Content            : (.*)\r", info_kunci_pass)
                profil_wifi["kata_sandi"] = kata_sandi[1] if kata_sandi else None
                daftar_wifi.append(profil_wifi)

        # Mengkonversi daftar_wifi menjadi format JSON
        json_hasil = json.dumps(daftar_wifi, indent=4)

        # Menyimpan hasil JSON ke dalam file
        with open(nama_file, 'w') as file:
            file.write(json_hasil)

        print(f"Hasil telah disimpan dalam file: {nama_file}")
    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    get_wifi_profiles()
    

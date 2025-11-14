import os
import pandas as pd
from datetime import datetime, date

# === SETTING ===
folder_path = "data_semua/"  # Ganti dengan path ke foldermu
kata_kunci = "This Data Download Powered By DonasiAja"
overwrite_file = True  # Ubah ke True jika ingin menimpa file asli

# Cek apakah file dimodifikasi hari ini


def is_modified_today(file_path):
    modified_time = os.path.getmtime(file_path)
    modified_date = datetime.fromtimestamp(modified_time).date()
    return modified_date == date.today()


# Proses semua file Excel di folder
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx") and not filename.startswith("~$"):
        file_path = os.path.join(folder_path, filename)

        if is_modified_today(file_path):
            print(f"📂 Memproses: {filename}")
            try:
                # Baca file dan abaikan 7 baris pertama, baris ke-8 jadi header
                df = pd.read_excel(file_path, header=7, engine="openpyxl")

                # Hapus baris yang mengandung kata kunci
                mask = df.apply(lambda row: row.astype(str).str.contains(
                    kata_kunci, case=False).any(), axis=1)
                df_bersih = df[~mask]

                # Simpan
                output_path = file_path if overwrite_file else os.path.join(
                    folder_path, f"bersih_{filename}")
                df_bersih.to_excel(output_path, index=False,
                                   sheet_name="Donasi")
                print(f"✅ Disimpan: {output_path}")
            except Exception as e:
                print(f"❌ Gagal memproses {filename}: {e}")

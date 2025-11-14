import pandas as pd
from datetime import datetime

# STEP 1: BACA DATA
df = pd.read_excel("kenapa ya.xlsx")  # Ganti dengan nama file kamu

# Kolom tetap (dari gambar)
fixed_cols = [
    "No", "Tanggal", "No CS", "Donatur", "Whatsapp",
    "Donasi Sebelumnya", "Periode Prospek", "Program", "Entri Donatur"
]
final_cols = ["Catatan", "Next Action"]

# Ambil kolom setelah 'Whatsapp' hingga sebelum 'Catatan'
start = df.columns.get_loc("Whatsapp") + 1
end = df.columns.get_loc("Catatan")
all_middle_cols = df.columns[start:end].tolist()

# Hapus kolom yang termasuk fixed dan final
interaction_cols = [
    col for col in all_middle_cols
    if col not in fixed_cols + final_cols
]

# Fungsi untuk ekstrak dan urutkan interaksi yang valid (tahun 2025)


def extract_sorted_interactions(row):
    interactions = []
    for i in range(0, len(interaction_cols), 4):
        if i + 3 >= len(interaction_cols):
            break

        tgl = row[interaction_cols[i]]
        act = row[interaction_cols[i+1]]
        rsp = row[interaction_cols[i+2]]
        dns = row[interaction_cols[i+3]]

        if pd.isna(tgl) and pd.isna(act) and pd.isna(rsp) and pd.isna(dns):
            continue

        try:
            tgl_obj = pd.to_datetime(tgl, dayfirst=True, errors='coerce')
            if pd.notna(tgl_obj) and tgl_obj.year != 2025:
                tgl = None
                tgl_obj = pd.NaT
        except:
            tgl_obj = pd.NaT

        interactions.append({
            "Tanggal": tgl,
            "Tanggal_obj": tgl_obj,
            "Action": act,
            "Respon": rsp,
            "Donasi": dns
        })

    interactions = sorted(
        interactions,
        key=lambda x: x["Tanggal_obj"] if pd.notnull(
            x["Tanggal_obj"]) else datetime.max
    )
    return interactions


# Hitung jumlah interaksi terbanyak
max_interaksi = max([
    len(extract_sorted_interactions(row))
    for _, row in df.iterrows()
])

# Susun ulang tiap baris
new_rows = []

for _, row in df.iterrows():
    new_row = {col: row[col] for col in fixed_cols + final_cols if col in row}
    interactions = extract_sorted_interactions(row)

    for i, inter in enumerate(interactions):
        new_row[f"Tanggal {i+1}"] = inter["Tanggal"]
        new_row[f"Action {i+1}"] = inter["Action"]
        new_row[f"Respon {i+1}"] = inter["Respon"]
        new_row[f"Donasi {i+1}"] = inter["Donasi"]

    for j in range(len(interactions)+1, max_interaksi+1):
        new_row[f"Tanggal {j}"] = ""
        new_row[f"Action {j}"] = ""
        new_row[f"Respon {j}"] = ""
        new_row[f"Donasi {j}"] = ""

    new_rows.append(new_row)

# Susun kolom output akhir
output_cols = fixed_cols
for i in range(1, max_interaksi + 1):
    output_cols += [f"Tanggal {i}", f"Action {i}",
                    f"Respon {i}", f"Donasi {i}"]
output_cols += final_cols

# Simpan hasil akhir ke file Excel
final_df = pd.DataFrame(new_rows)[output_cols]
final_df.to_excel("data_rapih_berurutan.xlsx", index=False)
print("✅ Selesai! File disimpan sebagai: data_rapih_berurutan.xlsx")

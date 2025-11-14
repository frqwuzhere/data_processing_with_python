import requests
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
import time

# Info akun WordPress
USERNAME = "faruq"
PASSWORD = "6tTvTTUkpVqu"

# URL login
login_url = "https://temanbaik.id/wp-login.php"

# Ambil tahun sekarang
current_year = datetime.today().year

# Set tanggal mulai ke 1 Januari tahun ini
start_date_str = f"{current_year}-06-26"


# def is_random_number(num):
#     num = str(num)

#     # Nomor harus hanya angka
#     if not num.isdigit():
#         return False

#     # Harus valid dari segi panjang dan awalan
#     starts_valid = num.startswith("08") or num.startswith(
#         "8") or num.startswith("62")
#     length_valid = 8 < len(num) <= 14

#     if not (starts_valid and length_valid):
#         return False

#     # Cek jika terlalu banyak angka sama (seperti 08888888888)
#     if len(set(num)) <= 3:
#         return False

#     # Cek pola berulang (seperti 081234567812345678)
#     if len(num) > 6 and num[:int(len(num)/2)] == num[int(len(num)/2):]:
#         return False

#     # Cek pola urutan (seperti 08123456789)
#     if num[2:].isdigit() and num[2:] in '1234567890'*2:
#         return False

#     return True

# # Standarisasi nomor agar diawali dengan 62


# def format_nomor(nomor):
#     nomor = str(nomor)
#     if nomor.startswith('6'):
#         return nomor
#     elif nomor.startswith('8'):
#         return '62' + nomor
#     else:
#         return nomor  # Bisa disesuaikan jika ada kondisi lain


def download_donasi_by_range(start_date_str, day_range=2):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    today = datetime.today()

    current_start = start_date

    with requests.Session() as s:
        # Login session
        payload = {
            'log': USERNAME,
            'pwd': PASSWORD,
            'wp-submit': 'Log In',
            'redirect_to': 'https://temanbaik.id/wp-admin/',
            'testcookie': '1'
        }
        login = s.post(login_url, data=payload)

        if login.status_code == 200 and "logout" in login.text.lower():
            print("✅ Login berhasil.")

            while current_start <= today:
                current_end = current_start + timedelta(days=day_range - 1)
                if current_end > today:
                    current_end = today

                # Format tanggal untuk parameter URL
                start_str = current_start.strftime("%Y-%m-%d")
                end_str = current_end.strftime("%Y-%m-%d")

                download_url = (
                    f"https://temanbaik.id/wp-admin/admin-post.php?"
                    f"action=download_data_donasi&c_id=all&c_date=daterange"
                    f"&c_range={start_str}_{end_str}&status=all"

                )

                print(
                    f"⬇️  Mendownload data dari {start_str} sampai {end_str}")

                # Download file
                try:
                    response = s.get(download_url, timeout=30)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(
                        f"❌ Error saat mengunduh dari {start_str} - {end_str}: {e}")
                    current_start = current_end + timedelta(days=1)
                    continue  # skip to next date range

                content_type = response.headers.get("Content-Type", "")
                if "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in content_type:
                    excel_data = BytesIO(response.content)
                    df = pd.read_excel(excel_data, engine="openpyxl")

                    df_cleaned = df[:-3]
                    new_header = df_cleaned.iloc[6].values
                    df_cleaned = df_cleaned[7:]
                    df_cleaned.columns = new_header
                    print(
                        f"✅ Data dari {start_str} - {end_str} berhasil dibaca. Jumlah baris: {len(df_cleaned)}")

                    # Reset index
                    df_cleaned = df_cleaned.reset_index(drop=True)

                    # Tampilkan data hasil bersih
                    df_cleaned

                    # Simpan ke Excel lokal (opsional)
                    filename = f"donasi_{start_str}_to_{end_str}.xlsx"
                    if len(df_cleaned == 0):
                        df_cleaned.to_excel(
                            f"data_test/{filename}", index=False, sheet_name="Donasi")
                        print(f"💾 Disimpan ke file: {filename}\n")
                        time.sleep(30)
                    else:
                        print("Data Kosong")
                else:
                    print(
                        f"⚠️ Gagal download untuk range {start_str} - {end_str}")
                    print("Status:", response.status_code)
                    print("Content-Type:", content_type)
                    print("Cuplikan:\n", response.content[:300].decode(
                        errors="ignore"))

                # Pindah ke range berikutnya
                current_start = current_end + timedelta(days=1)
        else:
            print("❌ Login gagal. Cek username/password.")


# Jalankan fungsi
# start at 7th July, with 1 date range
download_donasi_by_range("2025-08-01", day_range=1)

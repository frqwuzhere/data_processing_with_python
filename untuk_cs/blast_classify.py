import pandas as pd

df = pd.read_excel("Tracking_Data/Database.xlsx", sheet_name="Donasi")


# PER PROGRAM, BADGE, UNTUK PER SHEET

# def pisahkan_user_final(df, output_prefix='hasil_final'):
#     crm_list = df['CRM'].dropna().unique()  # ambil nama-nama CRM yang unik

#     for crm_name in crm_list:
#         df_crm = df[df['CRM'] == crm_name]
#         output_file = f"data_blast/program_badge_timing/{output_prefix}_{crm_name}.xlsx"
#         sheet_counter = {}

#         with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
#             # --- Data Jumat ---
#             df_jumat = df_crm[df_crm['Day_Mode'].str.lower() == 'fri']
#             grouped_jumat = df_jumat.groupby(['klasifikasi_program', 'Badge'])[
#                 ['Whatsapp', 'Donatur']].agg(list).reset_index()

#             for _, row in grouped_jumat.iterrows():
#                 program = row['klasifikasi_program']
#                 badge = row['Badge']
#                 users = row['Whatsapp']
#                 name = row['Donatur']

#                 base_name = f"jumat_{badge}"
#                 sheet_counter[base_name] = sheet_counter.get(base_name, 0) + 1
#                 sheet_name = f"{base_name}_{sheet_counter[base_name]}"
#                 sheet_name = sheet_name.replace('/', '-').replace('\\', '-')
#                 sheet_name = sheet_name[:31]

#                 df_users = pd.DataFrame({
#                     'Whatsapp': users,
#                     'Donatur': name,
#                     'Program': program,
#                     'Badge': badge
#                 })
#                 df_users.to_excel(writer, sheet_name=sheet_name,
#                                   index=False, startrow=1)
#                 worksheet = writer.sheets[sheet_name]
#                 worksheet.write(
#                     0, 0, f"CRM: {crm_name}, Hari: Jumat, Program: {program}, Badge: {badge}")

#             # --- Data Non-Jumat ---
#             df_nonjumat = df_crm[df_crm['Day_Mode'].str.lower() != 'fri']
#             grouped_nonjumat = df_nonjumat.groupby(['Date_Category', 'klasifikasi_program', 'Badge'])[
#                 ['Whatsapp', 'Donatur']].agg(list).reset_index()

#             for _, row in grouped_nonjumat.iterrows():
#                 kategori = row['Date_Category']
#                 program = row['klasifikasi_program']
#                 badge = row['Badge']
#                 users = row['Whatsapp']
#                 name = row['Donatur']

#                 base_name = f"{kategori}_{badge}"
#                 sheet_counter[base_name] = sheet_counter.get(base_name, 0) + 1
#                 sheet_name = f"{base_name}_{sheet_counter[base_name]}"
#                 sheet_name = sheet_name.replace('/', '-').replace('\\', '-')
#                 sheet_name = sheet_name[:31]

#                 df_users = pd.DataFrame({
#                     'Whatsapp': users,
#                     'Donatur': name,
#                     'Program': program,
#                     'Badge': badge
#                 })
#                 df_users.to_excel(writer, sheet_name=sheet_name,
#                                   index=False, startrow=1)
#                 worksheet = writer.sheets[sheet_name]
#                 worksheet.write(
#                     0, 0, f"CRM: {crm_name}, Kategori Hari: {kategori}, Program: {program}, Badge: {badge}")

#         print(f"✅ File berhasil dibuat untuk CRM {crm_name}: {output_file}")


# UNTUK SATU SHEET SAJA PER CS

def pisahkan_user_final(df):
    df = df[df['Kategori'] != 'INVALID']
    crm_list = df['CRM'].dropna().unique()

    for crm_name in crm_list:
        df_crm = df[df['CRM'] == crm_name].copy()

        # Urutkan dan susun ulang kolom
        df_crm_sorted = df_crm.sort_values(
            by=['Day_Mode', 'Date_Classification', 'klasifikasi_program', 'Badge'])

        # Susun ulang kolom sesuai urutan yang diminta
        df_output = df_crm_sorted[[
            'Whatsapp', 'Donatur', 'Day_Mode', 'Date_Classification', 'klasifikasi_program', 'Badge'
        ]]

        # Buat nama file
        output_file = f"data_blast/program_badge_timing/{crm_name}.xlsx"

        # Tulis ke Excel
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            df_output.to_excel(writer, sheet_name='Rekap',
                               index=False, startrow=0)

        print(f"✅ File berhasil dibuat untuk CRM {crm_name}: {output_file}")


pisahkan_user_final(df)

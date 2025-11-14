import pandas as pd

df = pd.read_excel("2025/Summary_2025.xlsx")

# Ganti "" kosong dengan NULL untuk menghindari error saat import awal
df = df.replace(r'^\s*$', None, regex=True)

df.to_excel("2025/summary.xlsx", index=False,
            na_rep='NULL', sheet_name="Donasi")

import xlwings as xw

wb = xw.Book('Daily_Activity_cekat.xlsx')
sheet = wb.sheets[0]
data = sheet.range('A1').expand().value  # Ambil semua data termasuk header

# Bagi data (tanpa menghilangkan validation di file asli)
chunk_size = 1000
header = data[0]
rows = data[1:]

for i in range(0, len(rows), chunk_size):
    start = i + 1
    end = min(i + chunk_size, len(rows))
    chunk_data = [header] + rows[i:end]

    # Buat workbook baru via Excel
    new_wb = xw.Book()
    new_ws = new_wb.sheets[0]
    new_ws.range('A1').value = chunk_data

    # Simpan file baru
    filename = f'Daily_Activity_2060_{start}_{end}.xlsx'
    new_wb.save(filename)
    new_wb.close()
    print(f'Saved: {filename}')

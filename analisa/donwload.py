import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+mysqlconnector://wp_plegw:VD@L9l9r_3%O4wzF@103.229.73.62:3306/wp_ajskr")
# conn = mysql.connector.connect(
#     host="103.229.73.62",
#     user="wp_plegw",
#     password="VD@L9l9r_3%O4wzF",
#     database="wp_ajskr"
# )

query = "SELECT donasi.campaign_id, donasi.invoice_id, donasi.name, donasi.whatsapp, donasi.nominal, fundraising.display_name,campaign.title, donasi.created_at FROM wp_ajskr.tEZ3UbOt_dja_donate as donasi LEFT JOIN wp_ajskr.tEZ3UbOt_dja_campaign as campaign ON donasi.campaign_id = campaign.campaign_id LEFT JOIN wp_ajskr.tEZ3UbOt_dja_aff_code user_aff ON donasi.campaign_id = user_aff.campaign_id LEFT JOIN wp_ajskr.tEZ3UbOt_users fundraising ON user_aff.user_id = fundraising.ID WHERE donasi.created_at BETWEEN '2025-06-26' and '2025-07-25' AND donasi.status = 1 AND fundraising.display_name IN ('Teman Baik', 'Teman Baik 1', 'Teman Baik 2', 'Pungky Septiawan', 'Organik TemanBaik', 'Cekat AI', 'Bintang Quran')"
df = pd.read_sql(query, engine)
df.to_csv("output.csv", index=False)

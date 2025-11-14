from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd

# Database credentials
username = "wp_plegw"
password = "VD@L9l9r_3%O4wzF"
host = "103.229.73.62"
port = 3306
database = "wp_ajskr"

# URL-encode username & password in case they have special characters
username_enc = quote_plus(username)
password_enc = quote_plus(password)

# Create SQLAlchemy engine
engine = create_engine(
    f"mysql+pymysql://{username_enc}:{password_enc}@{host}:{port}/{database}"
)

# Run a query and load results into Pandas
query = """SELECT donasi.invoice_id as Invoice_ID, donasi.name as Donatur, donasi.nominal as Total, donasi.whatsapp as Whatsapp, campaign.title as Program, CASE WHEN donasi.status = 1 THEN 'Success' ELSE 'Waiting' END as Payment_Status, donasi.payment_account as Payment_Account, donasi.created_at as Date FROM wp_ajskr.tEZ3UbOt_dja_donate donasi LEFT JOIN wp_ajskr.tEZ3UbOt_dja_campaign as campaign ON donasi.campaign_id = campaign.campaign_id WHERE donasi.created_at >= '2025-06-01' order by 8 asc;"""
data_from_mysql = pd.read_sql(query, engine)

data_from_mysql['Day'] = data_from_mysql['Date'].dt.strftime("%a")
data_from_mysql['Time'] = data_from_mysql['Date'].dt.strftime("%H:%M:%S")
data_from_mysql = data_from_mysql.rename(columns={
    "Payment_Status": "Payment Status",
    "Payment_Account": "Payment Account",
    "Invoice_ID": "Invoice ID"
})

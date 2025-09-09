from sqlalchemy import create_engine, text
import pandas as pd
from urllib.parse import quote_plus

# === CONFIGURATION ===
db_host = "localhost"
db_port = 5432               # Your PostgreSQL port
db_name = "postgres"             # Database name
db_user = "postgres"         # Your username
db_password = quote_plus("Vzu542@1988")  # Encode special chars in password
table_name = "edc_data"    # Table name in Postgres
excel_file_path = r"C:\Users\vinay\Dropbox\EDC_Data_12AUG2025.xlsx"

# === READ EXCEL FILE ===
df = pd.read_excel(excel_file_path)

# Auto-detect column types for SQL
def map_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "BIGINT"
    elif pd.api.types.is_float_dtype(dtype):
        return "DOUBLE PRECISION"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMP"
    else:
        return "TEXT"

columns_with_types = [f'"{col}" {map_dtype(df[col].dtype)}' for col in df.columns]

# === CONNECT TO DATABASE ===
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# === CREATE TABLE ===
create_table_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({", ".join(columns_with_types)});'
with engine.begin() as conn:  # auto-commit
    conn.execute(text(create_table_sql))

# === INSERT DATA ===
df.to_sql(table_name, engine, if_exists="append", index=False)

print(f"Data from {excel_file_path} successfully inserted into '{table_name}' table in '{db_name}' database.")
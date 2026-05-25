
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.client import Client
from models.child import Child
from models.spouses import SpouseAssociation

# ← החלף את הפרמטרים לפי הגדרות SQL Server בבית הספר
SERVER   = 'localhost'                  # שם השרת
DATABASE = 'Project'       # ← שם ה-DB שייצרי
DRIVER   =  'ODBC Driver 17 for SQL Server'                # Driver מהרשימה למטה



# יצירת connection string ל-SQL Server עם SQLAlchemy
connection_string = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)

engine = create_engine(
    "mssql+pyodbc:///?odbc_connect=" + connection_string
)
with engine.connect() as conn:
    with engine.connect() as conn:
        print(conn.exec_driver_sql("SELECT DB_NAME()").fetchone())
# יצירת הטבלאות אוטומטית אם לא קיימות
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():

    return Session()

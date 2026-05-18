
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.client import Base

# ← החלף את הפרמטרים לפי הגדרות SQL Server בבית הספר
SERVER   = 'localhost'                  # שם השרת
DATABASE = 'project'       # ← שם ה-DB שייצרי
DRIVER   = ['SQL Server', 'ODBC Driver 17 for SQL Server', 'SQL Server Native Client RDA 11.0', 'Microsoft Access Driver (*.mdb, *.accdb)', 'Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)', 'Microsoft Access Text Driver (*.txt, *.csv)']                 # Driver מהרשימה למטה



# יצירת connection string ל-SQL Server עם SQLAlchemy
engine = create_engine(
    f'mssql+pyodbc://{SERVER}/{DATABASE}'
    f'?driver={DRIVER.replace(" ", "+")}'
    f'&Trusted_Connection=yes'           # Windows auth, ללא סיסמה
)

# יצירת הטבלאות אוטומטית אם לא קיימות
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

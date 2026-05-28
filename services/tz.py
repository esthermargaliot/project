"""
extract_teudat_zehut.py
-----------------------
חילוץ נתונים מספח תז ישראלי סרוק (PDF).
תומך ב-PDF עם טקסט מוטמע וב-PDF סרוק (OCR).

דרישות:
    pip install pymupdf pytesseract Pillow
    sudo apt-get install tesseract-ocr tesseract-ocr-heb
"""
import pyodbc


import re
import fitz  # PyMuPDF

from PIL import Image
import io
from dataclasses import dataclass, asdict
from typing import Optional
import json
from PIL import ImageFilter
import os
import pytesseract

# נתיב ל־tesseract.exe שלך
#pytesseract.pytesseract.tesseract_cmd = r"Y:\שונות\רחלי ק\OCR\Tesseract-OCR\tesseract.exe"

# חשוב: תיקיית השפות (tessdata)
#os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR"

# בדיקה שהשפות נטענות
#print(pytesseract.get_languages(config=''))

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
@dataclass
class TeudatZehutData:
    """

    lastName = Column(String(100))
    firstName = Column(String(100))

    street = Column(String(100))
    city = Column(String(100))
    HouseNumber = Column(String(100))
    ApartmentNumber = Column(String(100))
מבנה נתונים לספח תז."""
    id: Optional[str] = None       # מספר זהות
    lastName: Optional[str] = None     # שם משפחה
    firstName: Optional[str] = None         # שם פרטי
    street: Optional[str] = None            # שם האב
    city: Optional[str] = None      # תאריך לידה
    HouseNumber: Optional[str] = None        # מקום לידה
    min: Optional[str] = None                # מין
    leom: Optional[str] = None               # לאום
    dat: Optional[str] = None                # דת
    status_mishpachti: Optional[str] = None  # מצב משפחתי
    aretz_leida: Optional[str] = None        # ארץ לידה
    #taarich_aliya: Optional[str] = None      # תאריך עלייה
    taarich_tokef: Optional[str] = None      # תאריך תוקף
    raw_text: Optional[str] = None           # טקסט גולמי (לדיבאג)


def _extract_text_from_pdf(pdf_path: str) -> str:
    """
    מחלץ טקסט מ-PDF — קודם מנסה חילוץ טקסט ישיר,
    ואם הוא ריק (PDF סרוק) — עובר ל-OCR עם תמיכה בעברית.
    """
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        text = page.get_text("text").strip()
        if text:
            full_text += text + "\n"
        else:
            # PDF סרוק — רסטריזציה + OCR
            mat = fitz.Matrix(5, 5)
            pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            img = img.convert("L")
            img = img.filter(ImageFilter.SHARPEN)
            ocr_text = pytesseract.image_to_string(
                img,
                lang="heb+eng",
                config="--oem 3 --psm 4"
            )
            full_text += ocr_text + "\n"

    doc.close()
    return full_text



def _clean(text: str) -> str:
    """ניקוי בסיסי של מחרוזת."""
    return text.strip().strip(":").strip()


def _find_field(text: str, patterns: list[str]) -> Optional[str]:
    """
    מחפש ערך לשדה לפי רשימת תבניות regex.
    מחזיר את הערך הראשון שנמצא.
    """
    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
        if match:
            return _clean(match.group(1))
    return None


def _extract_id_number(text: str) -> Optional[str]:
    """חילוץ מספר זהות (9 ספרות)."""
    patterns = [
        r"מספר\s*זהות[:\s]+(\d{9})",
        r"ת\.?ז\.?[:\s]+(\d{9})",
        r"(?<!\d)(\d{9})(?!\d)",  # 9 ספרות עצמאיות
    ]
    return _find_field(text, patterns)


def _extract_date(text: str, field_keywords: list[str]) -> Optional[str]:
    """חילוץ תאריך (DD/MM/YYYY או DD.MM.YYYY) לפי מילות מפתח."""
    date_pattern = r"(\d{1,2}[./]\d{1,2}[./]\d{2,4})"
    for keyword in field_keywords:
        pattern = rf"{keyword}[:\s]+{date_pattern}"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return _clean(match.group(1))
    return None


def parse_teudat_zehut(pdf_path: str) -> TeudatZehutData:

    import re

    def clean_ocr_text(text: str) -> str:
        # הסרת תווי בקרה בלתי קריאים
        text = re.sub(r"[\u200e\u200f\u202c\u202d]", "", text)
        # הסרת סימנים מיוחדים
        text = re.sub(r"[^\w\s\d\u0590-\u05FF./-]", " ", text)
        # המרת ריבוי רווחים לרווח אחד
        text = re.sub(r"\s+", " ", text)
        return text

    import unicodedata

    def clean_ocr_text(text: str) -> str:
        # הסרת תווי בקרה
        text = re.sub(r"[\u200e\u200f\u202c\u202d]", "", text)
        # הסרת סימנים מיוחדים
        text = re.sub(r"[^\w\s\d\u0590-\u05FF./-]", " ", text)
        # המרת ריבוי רווחים לרווח אחד
        text = re.sub(r"\s+", " ", text)
        # נורמליזציה של תווים בעברית
        text = unicodedata.normalize('NFC', text)
        return text.strip()

    raw_text = _extract_text_from_pdf(pdf_path)
    clean_text = clean_ocr_text(raw_text)
    data = TeudatZehutData(raw_text=clean_text)

    # מספר זהות
    data.mispar_zehut = _extract_id_number(raw_text)


    # שם משפחה
    data.shem_mishpacha = _find_field(raw_text, [
        r"שם\s*משפחה[:\s]+([^\n\d]+)",
        r"FAMILY\s*NAME[:\s]+([^\n]+)",
    ])




    # שם פרטי
    data.shem_prati = _find_field(raw_text, [
        r"שם\s*פרטי[:\s]+([^\n\d]+)",
        r"FIRST\s*NAME[:\s]+([^\n]+)",
        r"שם[:\s]+([^\n\d]+)",
    ])


    # שם האב
    data.shem_av = _find_field(raw_text, [
        r"שם\s*(?:ה)?אב[:\s]+([^\n\d]+)",
        r"FATHER['\u2019]?S?\s*NAME[:\s]+([^\n]+)",
    ])

    # תאריך לידה
    data.taarich_leida = _extract_date(clean_text, [
        r"תאריך לידה", r"DATE OF BIRTH", r"D\.O\.B"
    ])

    # מקום לידה
    data.makom_leida = _find_field(raw_text, [
        r"עיר\s*לידה[:\s]+([^\n\d]+)",
        r"מקום\s*לידה[:\s]+([^\n\d]+)",
        r"PLACE\s*OF\s*BIRTH[:\s]+([^\n]+)",
    ])

    # ארץ לידה
    data.aretz_leida = _find_field(raw_text, [
        r"ארץ\s*לידה[:\s]+([^\n\d]+)",
        r"COUNTRY\s*OF\s*BIRTH[:\s]+([^\n]+)",
    ])

    # מין
    data.min = _find_field(raw_text, [
        r"מין[:\s]+(זכר|נקבה|Male|Female)",
        r"SEX[:\s]+(M|F|Male|Female|זכר|נקבה)",
    ])

    # לאום
    data.leom = _find_field(raw_text, [
        r"לאום[:\s]+([^\n\d]+)",
        r"NATIONALITY[:\s]+([^\n]+)",
    ])

    # דת
    data.dat = _find_field(raw_text, [
        r"דת[:\s]+([^\n\d]+)",
        r"RELIGION[:\s]+([^\n]+)",
    ])

    # מצב משפחתי
    data.status_mishpachti = _find_field(raw_text, [
        r"מצב\s*(?:משפחתי|אישי)[:\s]+([^\n\d]+)",
        r"MARITAL\s*STATUS[:\s]+([^\n]+)",
    ])

    # תאריך עלייה
    data.taarich_aliya = _extract_date(raw_text, [
        "תאריך עלייה", "עלייה", "DATE OF IMMIGRATION"
    ])

    # תאריך תוקף
    data.taarich_tokef = _extract_date(raw_text, [
        "תאריך תוקף", "תוקף", "VALID UNTIL", "EXPIRY"
    ])



    return data


import fitz  # PyMuPDF


def convert_pdf_to_bw(input_path: str, output_path: str):
    doc = fitz.open(input_path)
    new_doc = fitz.open()

    for page in doc:
        # יצירת תמונה של העמוד
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), colorspace=fitz.csGRAY)
        img_bytes = pix.tobytes("png")

        # הוספה כעמוד חדש
        img_doc = fitz.open("png", img_bytes)
        new_doc.insert_pdf(img_doc)

    new_doc.save(output_path)
    new_doc.close()
    doc.close()
    print(f"PDF שחור-לבן נשמר ב: {output_path}")
    print("hhb")


def extract_and_print(pdf_path: str) -> dict:
    """
    פונקציית עזר — מחלצת ומדפיסה את הנתונים כ-JSON.

    Args:
        pdf_path: נתיב לקובץ PDF.

    Returns:
        מילון עם הנתונים המחולצים (ללא raw_text).
    """
    data = parse_teudat_zehut(pdf_path)
    result = asdict(data)
    result.pop("raw_text", None)  # לא להדפיס טקסט גולמי

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


# ──────────────────────────────────────────────
# הרצה ישירה לצורך בדיקה
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import sys


    data = parse_teudat_zehut(r"Y:\שונות\רחלי ק\ספח תעודת זהות דיגיטלי.pdf")
    print(data.raw_text)
    print(data.mispar_zehut)  # '123456789'
    print(data.shem_mishpacha)  # 'כהן'
    if len(sys.argv) < 2:
        print("שימוש: python extract_teudat_zehut.py <נתיב_לקובץ.pdf>")
        sys.exit(1)

    path = sys.argv[1]
    print(f"\n📄 מחלץ נתונים מ: {path}\n")
    # הנתיב לקובץ PDF שאת רוצה לחלץ ממנו נתונים
    pdf_path = r"Y:\שונות\רחלי ק\ספח תעודת זהות דיגיטלי.pdf"

    # קריאה לפונקציות מתוך אותו קובץ בלי import מעגלי
    data = parse_teudat_zehut(pdf_path)
    convert_pdf_to_bw(pdf_path, r"Y:\רחלי ק\שם.pdf")
    extract_and_print(r"Y:\רחלי ק\שם.pdf")

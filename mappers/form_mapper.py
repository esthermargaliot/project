
from bs4 import BeautifulSoup
import numpy as np
from services.embedding_model import get_model

model = get_model()

# =========================
# ALIASES (RULE LAYER)
# =========================
FIELD_ALIASES = {
    "client.id": ["מספר זהות"],
    "client.firstName": ["שם פרטי", "first name", "firstname", "שם"],
    "client.lastName": ["שם משפחה", "last name", "lastname", "משפחה"],
    "client.city": ["עיר", "city", "יישוב" ,"עיר מגורים","מען"],
    "client.street": ["רחוב", "street","רחוב מגורים"],
    "client.HouseNumber": ["מספר בית", "house number", "house"],
    "client.ApartmentNumber": ["דירה", "apartment", "apt"],


    "children.gender": ["מין", "gender"],
    "children.status": ["מעמד", "status","אזרחות"],
    "spouse.firstName": ["בן זוג שם פרטי", "first name", "שם פרטי בן זוג"],
    "spouse.lastName": ["בן זוג שם משפחה", "last name"],
    "spouse.marital_status": ["מצב אישי", "marital status"],
    "spouse.id":["id"],
    "children.first_name":["שם פרטי"],
    "children.date_of_birth":["תאריך לידה"],
    "children.id":["מספר זהות"]
}


# =========================
# EMBEDDING UTIL
# =========================
def cosine_matrix(a, b):
    return np.dot(a, b.T)

def normalize(text):
    if not text:
        return ""

    text = text.lower().strip()

    text = re.sub(r'[:*]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def alias_match(label_text, key):

    label_text = normalize(label_text)

    for alias in FIELD_ALIASES.get(key, []):

        if normalize(alias) == label_text:
            return True

    return False

import re

def detect_children_count(flat_data):
    indices = set()

    for key in flat_data.keys():
        m = re.match(r"children\.(\d+)\.", key)
        if m:
            indices.add(int(m.group(1)))

    return max(indices) + 1 if indices else 0
def find_alias_key(label_text, db_keys):
    """
    🥇 returns key if alias exists else None
    """
    for key in db_keys:
        if alias_match(label_text, key):
            return key
    return None

def extract_fields(html):
    soup = BeautifulSoup(html, "html.parser")

    fields = []
    current_section = None

    for el in soup.find_all(["h1", "h2", "h3", "label", "input", "select"]):

        # 1. עדכון section
        if el.name in ["h1", "h2", "h3"]:
            text = el.get_text(strip=True).lower()

            if "בן" in text or "בת זוג" in text:
                current_section = "spouse"

            elif "ילד" in text or "ילדים" in text:
                current_section = "children"

            else:
                current_section = "client"

            continue

        # 2. רק inputs נכנסים לרשימה
        if el.name == "input":
            label = el.get("name") or el.get("id")

            fields.append({
                "name": label,
                "label": label,
                "section": current_section
            })

    return fields


def build_dom_groups(html):
    soup = BeautifulSoup(html, "html.parser")

    fields = []
    seen = set()

    for el in soup.find_all(["input", "select", "textarea"]):

        field_id = el.get("id")
        field_name = el.get("name")
        placeholder = el.get("placeholder")

        # מניעת כפילויות
        key = (field_id, field_name)

        if key in seen:
            continue

        seen.add(key)

        # ------------------------
        # LABEL
        # ------------------------

        label = None

        # <label for="">
        if field_id:
            lbl = soup.find("label", attrs={"for": field_id})
            if lbl:
                label = lbl.get_text(" ", strip=True)

        # <label><input>
        if not label:
            parent_label = el.find_parent("label")
            if parent_label:
                label = parent_label.get_text(" ", strip=True)

        # aria-label
        if not label:
            label = el.get("aria-label")

        # placeholder
        if not label:
            label = placeholder

        # title
        if not label:
            label = el.get("title")

        # טקסט של האב
        if not label:
            parent = el.parent
            if parent:
                txt = parent.get_text(" ", strip=True)
                if txt:
                    label = txt

        # אם עדיין אין שום מידע
        if not label and not field_name and not field_id:
            continue

        # ------------------------
        # SECTION
        # ------------------------

        section = "client"

        parent = el

        while parent:

            text = parent.get_text(" ", strip=True).lower()

            if "ילד" in text or "ילדים" in text:
                section = "children"
                break

            if "בן זוג" in text or "בת זוג" in text:
                section = "spouse"
                break

            parent = parent.parent

        fields.append({
            "id": field_id,
            "name": field_name,
            "label": label or field_name or field_id,
            "placeholder": placeholder,
            "section": section
        })

    print(f"Fields extracted: {len(fields)}")

    return fields
def detect_section(label_text):
    text = label_text.lower()

    if any(x in text for x in ["ילד", "ילדים", "בן", "בת"]):
        return "children"

    if any(x in text for x in ["בן זוג", "אישה", "בעל", "spouse"]):
        return "spouse"

    return "client"
# =========================
# MAIN MAPPER
# =========================
SIMILARITY_THRESHOLD = 0.95
def detect_children_block(el):
    parent = el

    while parent:

        text = parent.get_text(" ", strip=True).lower()

        if "ילד" in text or "ילדים" in text:
            return parent

        parent = parent.find_parent()

    return None
def detect_section_from_group(group):

    text = group.get("title", "").lower()

    if "ילד" in text or "ילדים" in text:
        return "children"

    if "בן" in text or "בת זוג" in text or "בן/בת" in text:
        return "spouse"

    return "client"
from selenium.webdriver.common.by import By
def find_by_intent(driver, keywords):
    for text in keywords:
        try:
            return driver.find_element(By.XPATH, f"//*[contains(text(),'{text}')]")
        except:
            pass
    return None


def click_add_child(driver):
    keywords = ["הוסף ילד", "הוספת ילד", "add child", "child"]

    el = find_by_intent(driver, keywords)

    if not el:
        raise Exception("לא נמצא כפתור הוספת ילד")

    el.click()
def map_form_to_db(html, flat_data):

    used_keys = set()

    result = {}
    mapping_log = []

    # =========================
    # 1. DOM GROUPING
    # =========================
    fields = build_dom_groups(html)

    print("Fields:", len(fields))

    for f in fields:
        print(f)
    print("\n===== CHECK INPUT NAMES =====")

    for f in fields:
        print(
            "id:", f["id"],
            "| name:", f["name"],
            "| label:", f["label"]
        )

    print("=============================\n")

    if not fields:
        return result

    # =========================
    # 3. PREP DB EMBEDDINGS
    # =========================
    db_keys = list(flat_data.keys())

    db_vectors = model.encode(
        ["database field: " + k for k in db_keys],
        normalize_embeddings=True
    )
    db_vectors = np.array(db_vectors)

    label_texts = []

    for f in fields:
        label = f.get("label")

        if not label:
            label = f.get("name")

        if not label:
            label = ""

        label_texts.append(label)
    input_names = [f["name"] for f in fields]

    label_vectors = model.encode(
        ["form field: " + t for t in label_texts],
        normalize_embeddings=True
    )
    label_vectors = np.array(label_vectors)

    scores = cosine_matrix(label_vectors, db_vectors)

    # =========================
    # 4. MATCHING LOOP
    # =========================
    for i, field in enumerate(fields):

        section = field["section"]
        label_text = field["label"]
        input_name = field["name"]
        print(
            "Mapping:",
            label_text,
            "->",
            input_name
        )

        matched_key = find_alias_key(label_text, db_keys)
        source = None
        score = None

        # -------------------------
        # Alias first
        # -------------------------
        if matched_key is not None:

            if matched_key in used_keys:
                matched_key = None
            else:
                source = "alias"
                score = 1.0
                used_keys.add(matched_key)

        # -------------------------
        # Embedding fallback
        # -------------------------
        if matched_key is None:

            best_score = -1
            best_key = None

            for j, key in enumerate(db_keys):

                s = float(scores[i][j])

                # קטן boost לפי section
                if section and key.startswith(section):
                    s += 0.03

                if s > best_score:
                    best_score = s
                    best_key = key

            if best_score >= SIMILARITY_THRESHOLD:

                if best_key not in used_keys:
                    matched_key = best_key
                    source = "embedding"
                    score = best_score
                    used_keys.add(best_key)

        # -------------------------
        # SAVE RESULT
        # -------------------------
        if matched_key is not None:

            value = flat_data.get(matched_key)

            if value is not None:
                result[input_name] = value

        # -------------------------
        # LOGGING
        # -------------------------
        mapping_log.append({
            "label": label_text,
            "input": input_name,
            "matched_key": matched_key,
            "source": source,
            "score": score,
            "section": section
        })

    # =========================
    # 5. DEBUG OUTPUT

    # =========================


    return result

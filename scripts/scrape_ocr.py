import re
import os
import cv2
import pandas as pd
from PIL import Image, ImageOps, ImageEnhance
from datetime import datetime
from playwright.sync_api import sync_playwright
import pytesseract

URL = "https://www.winamax.fr/paris-sportifs/sports/100000"
CSV_PATH = "data/historique.csv"

def preprocess(img_path):
    img = Image.open(img_path).convert("L")
    img = ImageOps.invert(img)
    img = ImageEnhance.Contrast(img).enhance(2.5)
    tmp = img_path.replace(".png", "_prep.png")
    img.save(tmp)
    return tmp

def ocr_image(img_path):
    return pytesseract.image_to_string(
        Image.open(img_path),
        config="--psm 6 -l fra"
    )

def parse(text):
    rows = []
    blocks = text.split("COTE BOOST")
    for b in blocks:
        cote = re.findall(r"\b\d+,\d+\b", b)
        heure = re.findall(r"\b\d{2}:\d{2}\b", b)
        if cote:
            rows.append({
                "timestamp": datetime.utcnow().isoformat(),
                "heure_event": heure[0] if heure else "",
                "texte": re.sub(r"\s+", " ", b.strip()),
                "cote_boostee": cote[-1].replace(",", "."),
                "bookmaker": "winamax"
            })
    return rows

def deduplicate(df):
    return df.drop_duplicates(
        subset=["heure_event", "texte", "cote_boostee", "bookmaker"],
        keep="first"
    )

def main():
    os.makedirs("data", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 2200})
        page.goto(URL, timeout=60000)
        page.wait_for_selector("text=COTE BOOST", timeout=20000)
        page.wait_for_timeout(3000)
        page.screenshot(path="screen.png", full_page=True)
        browser.close()

    prep = preprocess("screen.png")
    text = ocr_image(prep)
    rows = parse(text)

    if not rows:
        return

    df_new = pd.DataFrame(rows)

    if os.path.exists(CSV_PATH):
        df_old = pd.read_csv(CSV_PATH)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df = deduplicate(df)
    df.to_csv(CSV_PATH, index=False)

if __name__ == "__main__":
    main()

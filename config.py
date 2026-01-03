"""
Configuration du scraper Winamax
"""
import os
from pathlib import Path

# URL cible
TARGET_URL = "https://www.winamax.fr/paris-sportifs/sports/100000"

# Chemins de sortie
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
SCREENSHOTS_DIR = OUTPUT_DIR / "screenshots"
JSON_DIR = OUTPUT_DIR / "json"
CSV_DIR = OUTPUT_DIR / "csv"

# Créer les dossiers s'ils n'existent pas
for directory in [OUTPUT_DIR, SCREENSHOTS_DIR, JSON_DIR, CSV_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Paramètres de scraping
HEADLESS = True
TIMEOUT = 30
DELAY = 2  # Délai en secondes entre les actions
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Paramètres Selenium
SELENIUM_OPTIONS = {
    "headless": HEADLESS,
    "disable-gpu": True,
    "no-sandbox": True,
    "disable-dev-shm-usage": True,
    "window-size": "1920,1080"
}

# Paramètres Playwright
PLAYWRIGHT_OPTIONS = {
    "headless": HEADLESS,
    "viewport": {"width": 1920, "height": 1080},
    "user_agent": USER_AGENT
}

# Paramètres OCR
TESSERACT_CONFIG = r'--oem 3 --psm 6 -l fra'
OCR_PREPROCESSING = {
    "scale_factor": 2,  # Agrandir l'image
    "threshold": True,  # Binarisation
    "denoise": True     # Réduction du bruit
}

# Sélecteurs CSS pour le scraping
SELECTORS = {
    "cote_cards": ".boost-card, [class*='boost'], [class*='cote']",
    "time": ".time, .hour, [class*='time'], [class*='hour']",
    "sport": ".sport, .competition, [class*='sport']",
    "description": ".description, .match-desc, [class*='desc']",
    "original_odds": ".original-odd, [class*='original']",
    "boosted_odds": ".boosted-odd, [class*='boost']"
}

# Format de date
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"

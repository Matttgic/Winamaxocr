"""
Scraper utilisant OCR (Tesseract) pour extraire les cotes depuis des screenshots
"""
import re
import asyncio
from datetime import datetime
from PIL import Image
import pytesseract
import cv2
import numpy as np
from playwright.async_api import async_playwright
import config


class OCRScraper:
    def __init__(self, headless=None):
        self.headless = headless if headless is not None else config.HEADLESS
    
    def preprocess_image(self, image_path):
        """Prétraitement de l'image pour améliorer l'OCR"""
        # Lire l'image
        img = cv2.imread(str(image_path))
        
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Agrandir l'image
        if config.OCR_PREPROCESSING['scale_factor'] > 1:
            scale = config.OCR_PREPROCESSING['scale_factor']
            width = int(gray.shape[1] * scale)
            height = int(gray.shape[0] * scale)
            gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_CUBIC)
        
        # Réduction du bruit
        if config.OCR_PREPROCESSING['denoise']:
            gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Binarisation adaptative
        if config.OCR_PREPROCESSING['threshold']:
            gray = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
        
        # Sauvegarder l'image prétraitée
        preprocessed_path = config.SCREENSHOTS_DIR / f"preprocessed_{datetime.now().strftime(config.DATETIME_FORMAT)}.png"
        cv2.imwrite(str(preprocessed_path), gray)
        
        return preprocessed_path
    
    def extract_text_from_image(self, image_path):
        """Extrait le texte d'une image avec Tesseract"""
        try:
            # Prétraiter l'image
            preprocessed = self.preprocess_image(image_path)
            
            # Utiliser Tesseract
            text = pytesseract.image_to_string(
                Image.open(preprocessed),
                lang='fra',
                config=config.TESSERACT_CONFIG
            )
            
            return text
        
        except Exception as e:
            print(f"❌ Erreur OCR: {e}")
            return ""
    
    def parse_ocr_text(self, text):
        """Parse le texte OCR pour extraire les données structurées"""
        cotes = []
        
        # Diviser par lignes
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        current_cote = {
            'timestamp': datetime.now().isoformat(),
            'method': 'ocr',
            'heure': '',
            'sport': '',
            'description': '',
            'cote_originale': '',
            'cote_boostee': ''
        }
        
        for i, line in enumerate(lines):
            # Chercher "COTE BOOSTEE"
            if re.search(r'(COTE.*BOOST|BOOST.*COTE)', line, re.I):
                # Sauvegarder la cote précédente si complète
                if current_cote['cote_boostee']:
                    cotes.append(current_cote.copy())
                    current_cote = {
                        'timestamp': datetime.now().isoformat(),
                        'method': 'ocr',
                        'heure': '',
                        'sport': '',
                        'description': '',
                        'cote_originale': '',
                        'cote_boostee': ''
                    }
            
            # Extraire l'heure
            time_match = re.search(r'\b([0-2]?[0-9]:[0-5][0-9])\b', line)
            if time_match and not current_cote['heure']:
                current_cote['heure'] = time_match.group(1)
            
            # Extraire les cotes
            odds = re.findall(r'\b(\d+[,\.]\d{2})\b', line)
            if odds:
                if not current_cote['cote_originale'] and len(odds) >= 1:
                    current_cote['cote_originale'] = odds[0].replace('.', ',')
                if len(odds) >= 2:
                    current_cote['cote_boostee'] = odds[-1].replace('.', ',')
            
            # Extraire le texte descriptif
            if (len(line) > 10 and 
                'COTE' not in line.upper() and 
                'BOOST' not in line.upper() and
                not re.match(r'^\d+[,\.]\d{2}$', line)):
                
                if not current_cote['sport']:
                    current_cote['sport'] = line
                elif not current_cote['description']:
                    current_cote['description'] = line
        
        # Ajouter la dernière cote
        if current_cote['cote_boostee']:
            cotes.append(current_cote)
        
        return cotes
    
    async def capture_screenshot(self):
        """Capture un screenshot de la page"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            try:
                await page.goto(config.TARGET_URL, wait_until='networkidle')
                await page.wait_for_timeout(config.DELAY * 1000)
                
                # Scroll
                for _ in range(3):
                    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    await page.wait_for_timeout(1000)
                
                # Screenshot
                timestamp = datetime.now().strftime(config.DATETIME_FORMAT)
                screenshot_path = config.SCREENSHOTS_DIR / f"ocr_{timestamp}.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                
                return screenshot_path
            
            finally:
                await browser.close()
    
    def scrape(self):
        """Scrape avec OCR"""
        try:
            print("🚀 Démarrage du scraping avec OCR...")
            
            # Capturer un screenshot
            screenshot_path = asyncio.run(self.capture_screenshot())
            print(f"📸 Screenshot: {screenshot_path}")
            
            # Extraire le texte
            print("👁️ Extraction du texte avec OCR...")
            text = self.extract_text_from_image(screenshot_path)
            
            # Parser les données
            cotes = self.parse_ocr_text(text)
            
            return cotes
        
        except Exception as e:
            print(f"❌ Erreur OCR Scraper: {e}")
            import traceback
            traceback.print_exc()
            return []

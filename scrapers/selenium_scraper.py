"""
Scraper utilisant Selenium pour extraire les cotes boostées
"""
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import config


class SeleniumScraper:
    def __init__(self, headless=None):
        self.headless = headless if headless is not None else config.HEADLESS
        self.driver = None
        
    def setup_driver(self):
        """Configure le driver Selenium"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless=new")
        
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"user-agent={config.USER_AGENT}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(config.TIMEOUT)
        
    def scroll_page(self):
        """Scroll la page pour charger tout le contenu dynamique"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        for _ in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def extract_cotes_data(self):
        """Extrait les données des cartes de cotes"""
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        cotes = []
        
        # Rechercher les éléments contenant "COTE BOOSTEE"
        boost_elements = soup.find_all(string=re.compile(r'COTE.*BOOST', re.I))
        
        for element in boost_elements:
            try:
                # Remonter pour trouver le conteneur parent
                card = element.find_parent('div', class_=lambda x: x and any(
                    keyword in str(x).lower() for keyword in ['card', 'boost', 'bet']
                ))
                
                if not card:
                    continue
                
                # Extraire les informations
                cote_data = {
                    'timestamp': datetime.now().isoformat(),
                    'heure': '',
                    'sport': '',
                    'description': '',
                    'cote_originale': '',
                    'cote_boostee': ''
                }
                
                # Chercher l'heure (format HH:MM)
                time_match = re.search(r'\b([0-2]?[0-9]:[0-5][0-9])\b', card.get_text())
                if time_match:
                    cote_data['heure'] = time_match.group(1)
                
                # Chercher les cotes (format X,XX ou X.XX)
                odds = re.findall(r'\b(\d+[,\.]\d{2})\b', card.get_text())
                if len(odds) >= 2:
                    cote_data['cote_originale'] = odds[0].replace('.', ',')
                    cote_data['cote_boostee'] = odds[-1].replace('.', ',')
                
                # Description et sport
                text_content = card.get_text(separator=' ', strip=True)
                lines = [l.strip() for l in text_content.split('\n') if l.strip()]
                
                for line in lines:
                    if 'COTE' not in line.upper() and len(line) > 10:
                        if not cote_data['sport']:
                            cote_data['sport'] = line
                        elif not cote_data['description']:
                            cote_data['description'] = line
                
                if cote_data['cote_boostee'] and cote_data['heure']:
                    cotes.append(cote_data)
            
            except Exception as e:
                print(f"⚠️ Erreur extraction élément: {e}")
                continue
        
        return cotes
    
    def scrape(self):
        """Scrape la page des cotes boostées"""
        try:
            print("🚀 Démarrage du scraping avec Selenium...")
            self.setup_driver()
            
            print(f"📄 Chargement de {config.TARGET_URL}")
            self.driver.get(config.TARGET_URL)
            
            time.sleep(config.DELAY * 2)
            
            # Scroll pour charger le contenu
            self.scroll_page()
            
            # Prendre un screenshot
            timestamp = datetime.now().strftime(config.DATETIME_FORMAT)
            screenshot_path = config.SCREENSHOTS_DIR / f"selenium_{timestamp}.png"
            self.driver.save_screenshot(str(screenshot_path))
            print(f"📸 Screenshot: {screenshot_path}")
            
            # Extraire les données
            cotes = self.extract_cotes_data()
            
            return cotes
            
        except Exception as e:
            print(f"❌ Erreur Selenium: {e}")
            import traceback
            traceback.print_exc()
            return []
        
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 Driver Selenium fermé")

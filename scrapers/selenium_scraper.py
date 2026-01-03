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
        
        # Utiliser chromedriver du système (préinstallé sur GitHub Actions)
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"⚠️ Erreur avec le driver système: {e}")
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception as e2:
                print(f"❌ Erreur avec webdriver-manager: {e2}")
                raise
        
        self.driver.set_page_load_timeout(config.TIMEOUT)
    
    def accept_cookies(self):
        """Accepte les cookies si la popup apparaît"""
        try:
            # Attendre que la popup de cookies apparaisse
            wait = WebDriverWait(self.driver, 5)
            
            # Chercher le bouton "Tout accepter" (plusieurs sélecteurs possibles)
            cookie_selectors = [
                "button[aria-label='Tout accepter']",
                "button:contains('Tout accepter')",
                "button[class*='accept']",
                "[id*='cookie'] button",
                "[class*='cookie'] button",
                "button[title='Tout accepter']"
            ]
            
            for selector in cookie_selectors:
                try:
                    if 'contains' in selector:
                        # Utiliser XPath pour :contains
                        button = wait.until(EC.element_to_be_clickable(
                            (By.XPATH, "//button[contains(text(), 'Tout accepter')]")
                        ))
                    else:
                        button = wait.until(EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, selector)
                        ))
                    
                    button.click()
                    print("✅ Cookies acceptés")
                    time.sleep(2)  # Attendre que la popup disparaisse
                    return True
                except:
                    continue
            
            # Si aucun bouton trouvé, essayer de fermer la popup avec le X
            try:
                close_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close'], button.close, [class*='close']")
                close_button.click()
                print("✅ Popup fermée")
                time.sleep(2)
                return True
            except:
                pass
            
            print("⚠️ Impossible de fermer la popup de cookies")
            return False
            
        except Exception as e:
            print(f"ℹ️ Pas de popup de cookies détectée (c'est normal): {e}")
            return False
    
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
        
        # Rechercher les éléments contenant "COTE BOOSTEE" ou "BOOST"
        boost_elements = soup.find_all(string=re.compile(r'(COTE.*BOOST|BOOST.*COTE)', re.I))
        
        if not boost_elements:
            print("⚠️ Aucun élément 'COTE BOOSTEE' trouvé dans le HTML")
            # Essayer de trouver des éléments avec des classes typiques
            boost_elements = soup.find_all('div', class_=re.compile(r'boost|promo|featured', re.I))
        
        print(f"🔍 Trouvé {len(boost_elements)} éléments potentiels")
        
        for element in boost_elements:
            try:
                # Remonter pour trouver le conteneur parent
                card = None
                if isinstance(element, str):
                    card = element.find_parent('div', class_=lambda x: x and any(
                        keyword in str(x).lower() for keyword in ['card', 'boost', 'bet', 'event']
                    ))
                else:
                    card = element
                
                if not card:
                    continue
                
                cote_data = {
                    'timestamp': datetime.now().isoformat(),
                    'method': 'selenium',
                    'heure': '',
                    'sport': '',
                    'description': '',
                    'cote_originale': '',
                    'cote_boostee': ''
                }
                
                card_text = card.get_text(separator=' ', strip=True)
                
                # Extraire l'heure (format HH:MM)
                time_match = re.search(r'\b([0-2]?[0-9]:[0-5][0-9])\b', card_text)
                if time_match:
                    cote_data['heure'] = time_match.group(1)
                
                # Extraire toutes les cotes (format X,XX ou X.XX)
                odds = re.findall(r'\b(\d+[,\.]\d{2})\b', card_text)
                if len(odds) >= 2:
                    cote_data['cote_originale'] = odds[0].replace('.', ',')
                    cote_data['cote_boostee'] = odds[-1].replace('.', ',')
                elif len(odds) == 1:
                    cote_data['cote_boostee'] = odds[0].replace('.', ',')
                
                # Extraire le texte descriptif
                lines = [l.strip() for l in card_text.split('\n') if l.strip()]
                relevant_lines = []
                
                for line in lines:
                    if (len(line) > 5 and 
                        'COTE' not in line.upper() and 
                        'BOOST' not in line.upper() and
                        not re.match(r'^\d+[,\.]\d{2}$', line) and
                        not re.match(r'^\d{1,2}:\d{2}$', line)):
                        relevant_lines.append(line)
                
                if len(relevant_lines) >= 1:
                    cote_data['sport'] = relevant_lines[0]
                if len(relevant_lines) >= 2:
                    cote_data['description'] = ' '.join(relevant_lines[1:])
                
                # Valider qu'on a au moins une cote
                if cote_data['cote_boostee']:
                    cotes.append(cote_data)
                    print(f"✅ Cote extraite: {cote_data['cote_boostee']} - {cote_data['sport']}")
            
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
            
            # Attendre un peu que la page charge
            time.sleep(config.DELAY)
            
            # Accepter les cookies
            self.accept_cookies()
            
            # Attendre encore un peu après avoir accepté les cookies
            time.sleep(config.DELAY)
            
            # Scroll pour charger le contenu
            print("📜 Scroll de la page...")
            self.scroll_page()
            
            # Prendre un screenshot APRÈS avoir accepté les cookies
            timestamp = datetime.now().strftime(config.DATETIME_FORMAT)
            screenshot_path = config.SCREENSHOTS_DIR / f"selenium_{timestamp}.png"
            self.driver.save_screenshot(str(screenshot_path))
            print(f"📸 Screenshot: {screenshot_path}")
            
            # Extraire les données
            print("🔍 Extraction des données...")
            cotes = self.extract_cotes_data()
            
            if not cotes:
                print("⚠️ Aucune cote extraite - vérifiez le screenshot")
            else:
                print(f"✨ {len(cotes)} cotes extraites avec succès!")
            
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

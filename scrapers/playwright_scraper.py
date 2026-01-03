"""
Scraper utilisant Playwright pour extraire les cotes boostées
"""
import re
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import config


class PlaywrightScraper:
    def __init__(self, headless=None):
        self.headless = headless if headless is not None else config.HEADLESS
    
    async def scrape_async(self):
        """Scrape la page avec Playwright (async)"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=config.USER_AGENT
            )
            
            page = await context.new_page()
            
            try:
                print(f"📄 Chargement de {config.TARGET_URL}")
                await page.goto(config.TARGET_URL, wait_until='networkidle', timeout=config.TIMEOUT * 1000)
                
                # Attendre un peu pour le contenu dynamique
                await page.wait_for_timeout(config.DELAY * 1000)
                
                # Scroll pour charger plus de contenu
                for _ in range(3):
                    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    await page.wait_for_timeout(1000)
                
                # Prendre un screenshot
                timestamp = datetime.now().strftime(config.DATETIME_FORMAT)
                screenshot_path = config.SCREENSHOTS_DIR / f"playwright_{timestamp}.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                print(f"📸 Screenshot: {screenshot_path}")
                
                # Récupérer le contenu HTML
                content = await page.content()
                
                # Parser avec BeautifulSoup
                cotes = self.extract_cotes_data(content)
                
                return cotes
            
            except Exception as e:
                print(f"❌ Erreur Playwright: {e}")
                import traceback
                traceback.print_exc()
                return []
            
            finally:
                await browser.close()
                print("🔒 Browser Playwright fermé")
    
    def extract_cotes_data(self, html_content):
        """Extrait les données des cartes de cotes"""
        soup = BeautifulSoup(html_content, 'html.parser')
        cotes = []
        
        # Rechercher tous les éléments contenant "COTE BOOSTEE" ou "BOOST"
        boost_elements = soup.find_all(string=re.compile(r'(COTE.*BOOST|BOOST.*COTE)', re.I))
        
        for element in boost_elements:
            try:
                # Trouver le conteneur parent
                card = element.find_parent('div', class_=lambda x: x and any(
                    keyword in str(x).lower() for keyword in ['card', 'boost', 'bet', 'event']
                ))
                
                if not card:
                    # Essayer de remonter plus haut
                    card = element.find_parent('div')
                    if not card:
                        continue
                
                cote_data = {
                    'timestamp': datetime.now().isoformat(),
                    'method': 'playwright',
                    'heure': '',
                    'sport': '',
                    'competition': '',
                    'description': '',
                    'cote_originale': '',
                    'cote_boostee': ''
                }
                
                # Récupérer tout le texte de la carte
                card_text = card.get_text(separator='\n', strip=True)
                
                # Extraire l'heure (format HH:MM)
                time_match = re.search(r'\b([0-2]?[0-9]:[0-5][0-9])\b', card_text)
                if time_match:
                    cote_data['heure'] = time_match.group(1)
                
                # Extraire toutes les cotes (format X,XX ou X.XX)
                odds = re.findall(r'\b(\d+[,\.]\d{2})\b', card_text)
                if len(odds) >= 2:
                    cote_data['cote_originale'] = odds[0].replace('.', ',')
                    cote_data['cote_boostee'] = odds[-1].replace('.', ',')
                
                # Extraire le sport et la description
                lines = [l.strip() for l in card_text.split('\n') if l.strip()]
                
                # Filtrer les lignes pertinentes (ignorer "COTE BOOSTEE", les cotes, etc.)
                relevant_lines = []
                for line in lines:
                    if (len(line) > 5 and 
                        'COTE' not in line.upper() and 
                        'BOOST' not in line.upper() and
                        not re.match(r'^\d+[,\.]\d{2}$', line) and
                        not re.match(r'^\d{1,2}:\d{2}$', line)):
                        relevant_lines.append(line)
                
                # Assigner sport, competition et description
                if len(relevant_lines) >= 1:
                    cote_data['sport'] = relevant_lines[0]
                if len(relevant_lines) >= 2:
                    cote_data['competition'] = relevant_lines[1]
                if len(relevant_lines) >= 3:
                    cote_data['description'] = ' '.join(relevant_lines[2:])
                elif len(relevant_lines) == 2:
                    cote_data['description'] = relevant_lines[1]
                
                # Valider que nous avons au moins les données minimales
                if cote_data['cote_boostee'] and (cote_data['heure'] or cote_data['sport']):
                    cotes.append(cote_data)
            
            except Exception as e:
                print(f"⚠️ Erreur extraction: {e}")
                continue
        
        # Dédupliquer par cote boostée + heure
        unique_cotes = []
        seen = set()
        for cote in cotes:
            key = (cote['heure'], cote['cote_boostee'])
            if key not in seen:
                seen.add(key)
                unique_cotes.append(cote)
        
        return unique_cotes
    
    def scrape(self):
        """Point d'entrée synchrone"""
        try:
            print("🚀 Démarrage du scraping avec Playwright...")
            return asyncio.run(self.scrape_async())
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return []

"""
Script principal pour scraper les cotes boostées Winamax
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import config
from scrapers.playwright_scraper import PlaywrightScraper
from scrapers.selenium_scraper import SeleniumScraper
from scrapers.ocr_scraper import OCRScraper
from utils.data_exporter import DataExporter


def main():
    parser = argparse.ArgumentParser(
        description='Scraper de cotes boostées Winamax'
    )
    parser.add_argument(
        '--method',
        choices=['selenium', 'playwright', 'ocr', 'all'],
        default='playwright',
        help='Méthode de scraping à utiliser'
    )
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Désactiver le mode headless (afficher le navigateur)'
    )
    parser.add_argument(
        '--export',
        choices=['json', 'csv', 'all'],
        default='all',
        help='Format d\'export des données'
    )
    parser.add_argument(
        '--delay',
        type=int,
        default=config.DELAY,
        help='Délai en secondes entre les actions'
    )
    
    args = parser.parse_args()
    
    # Mettre à jour la config
    if args.no_headless:
        config.HEADLESS = False
    config.DELAY = args.delay
    
    print("=" * 60)
    print("🎰 WINAMAX COTES BOOSTÉES SCRAPER")
    print("=" * 60)
    print(f"⏰ Début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Méthode: {args.method}")
    print(f"📊 Export: {args.export}")
    print("=" * 60)
    
    results = []
    
    try:
        if args.method == 'playwright' or args.method == 'all':
            print("\n🎭 Scraping avec Playwright...")
            scraper = PlaywrightScraper(headless=config.HEADLESS)
            data = scraper.scrape()
            if data:
                results.extend(data)
                print(f"✅ {len(data)} cotes extraites avec Playwright")
        
        if args.method == 'selenium' or args.method == 'all':
            print("\n🤖 Scraping avec Selenium...")
            scraper = SeleniumScraper(headless=config.HEADLESS)
            data = scraper.scrape()
            if data:
                results.extend(data)
                print(f"✅ {len(data)} cotes extraites avec Selenium")
        
        if args.method == 'ocr' or args.method == 'all':
            print("\n👁️ Scraping avec OCR...")
            scraper = OCRScraper(headless=config.HEADLESS)
            data = scraper.scrape()
            if data:
                results.extend(data)
                print(f"✅ {len(data)} cotes extraites avec OCR")
        
        # Export des résultats
        if results:
            exporter = DataExporter()
            timestamp = datetime.now().strftime(config.DATETIME_FORMAT)
            
            if args.export in ['json', 'all']:
                json_file = exporter.export_json(results, f"cotes_{timestamp}.json")
                print(f"\n💾 JSON exporté: {json_file}")
            
            if args.export in ['csv', 'all']:
                csv_file = exporter.export_csv(results, f"cotes_{timestamp}.csv")
                print(f"💾 CSV exporté: {csv_file}")
            
            print(f"\n✨ Scraping terminé avec succès!")
            print(f"📊 Total: {len(results)} cotes boostées extraites")
        else:
            print("\n⚠️ Aucune donnée extraite")
    
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("=" * 60)
    print(f"⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    main()

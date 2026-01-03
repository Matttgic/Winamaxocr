"""
Script de test pour vérifier que tout fonctionne
"""
import sys
from pathlib import Path

# Ajouter le répertoire au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

def test_imports():
    """Test que tous les imports fonctionnent"""
    print("🧪 Test des imports...")
    try:
        import config
        from scrapers import PlaywrightScraper, SeleniumScraper, OCRScraper
        from utils import DataExporter
        print("✅ Tous les imports OK")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_config():
    """Test de la configuration"""
    print("\n🧪 Test de la configuration...")
    try:
        import config
        
        # Vérifier que les dossiers existent
        assert config.OUTPUT_DIR.exists(), "Dossier output manquant"
        assert config.SCREENSHOTS_DIR.exists(), "Dossier screenshots manquant"
        assert config.JSON_DIR.exists(), "Dossier json manquant"
        assert config.CSV_DIR.exists(), "Dossier csv manquant"
        
        print(f"✅ URL cible: {config.TARGET_URL}")
        print(f"✅ Timeout: {config.TIMEOUT}s")
        print(f"✅ Délai: {config.DELAY}s")
        print(f"✅ Mode headless: {config.HEADLESS}")
        
        return True
    except AssertionError as e:
        print(f"❌ Erreur config: {e}")
        return False

def test_dependencies():
    """Test que toutes les dépendances sont installées"""
    print("\n🧪 Test des dépendances...")
    
    dependencies = {
        'selenium': 'selenium',
        'playwright': 'playwright',
        'pytesseract': 'pytesseract',
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'bs4': 'beautifulsoup4',
        'requests': 'requests',
        'pandas': 'pandas',
        'numpy': 'numpy'
    }
    
    all_ok = True
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - pip install {package}")
            all_ok = False
    
    return all_ok

def test_tesseract():
    """Test que Tesseract est installé"""
    print("\n🧪 Test de Tesseract OCR...")
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract version: {version}")
        return True
    except Exception as e:
        print(f"❌ Tesseract non installé ou non trouvé: {e}")
        print("   Installez Tesseract depuis: https://github.com/UB-Mannheim/tesseract/wiki")
        return False

def test_playwright_browser():
    """Test que les navigateurs Playwright sont installés"""
    print("\n🧪 Test des navigateurs Playwright...")
    try:
        import asyncio
        from playwright.async_api import async_playwright
        
        async def check_browser():
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                await browser.close()
                return True
        
        result = asyncio.run(check_browser())
        print("✅ Navigateur Chromium installé")
        return result
    except Exception as e:
        print(f"❌ Navigateur Playwright non installé: {e}")
        print("   Exécutez: playwright install chromium")
        return False

def test_data_export():
    """Test de l'export de données"""
    print("\n🧪 Test de l'export de données...")
    try:
        from utils import DataExporter
        
        exporter = DataExporter()
        
        # Données de test
        test_data = [
            {
                'heure': '20:00',
                'sport': 'Test Sport',
                'description': 'Match test',
                'cote_originale': '2,00',
                'cote_boostee': '2,50'
            }
        ]
        
        # Test JSON
        json_file = exporter.export_json(test_data, 'test.json')
        assert json_file.exists(), "Fichier JSON non créé"
        print(f"✅ Export JSON: {json_file}")
        
        # Test CSV
        csv_file = exporter.export_csv(test_data, 'test.csv')
        assert csv_file.exists(), "Fichier CSV non créé"
        print(f"✅ Export CSV: {csv_file}")
        
        # Nettoyer
        json_file.unlink()
        csv_file.unlink()
        
        return True
    except Exception as e:
        print(f"❌ Erreur export: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print("=" * 60)
    print("🧪 TESTS DU SCRAPER WINAMAX")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Dépendances", test_dependencies),
        ("Tesseract OCR", test_tesseract),
        ("Playwright", test_playwright_browser),
        ("Export de données", test_data_export)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Exception dans {name}: {e}")
            results.append((name, False))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("=" * 60)
    print(f"Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! Vous pouvez lancer le scraper.")
        return 0
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())

# 🎰 Winamax Cotes Boostées Scraper

Scraper automatique pour les cotes boostées de Winamax avec 3 méthodes différentes (Selenium, Playwright, OCR) et exécution automatique via GitHub Actions toutes les 30 minutes.

[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Fonctionnalités

- ✅ **3 méthodes de scraping** : Selenium, Playwright (recommandé), OCR
- ⏰ **Exécution automatique** : Toutes les 30 minutes via GitHub Actions (00:05, 00:35, 01:05, etc.)
- 📊 **Export multiple** : JSON et CSV
- 📸 **Screenshots** : Capture de page complète
- 🔄 **Commit automatique** : Les résultats sont automatiquement sauvegardés
- 📱 **Compatible smartphone** : Consultez les résultats depuis l'app GitHub Mobile

## ⚡ Démarrage rapide (GitHub Actions)

### 1️⃣ Créer le repository

```bash
# Créer un nouveau repo sur GitHub : winamax-scraper
# Cloner et pousser le code
git clone https://github.com/VOTRE_USERNAME/winamax-scraper.git
cd winamax-scraper
# Copier tous les fichiers du projet ici
git add .
git commit -m "🚀 Initial commit"
git push origin main
```

### 2️⃣ Activer les permissions

1. Aller dans **Settings** → **Actions** → **General**
2. Workflow permissions → **Read and write permissions**
3. Sauvegarder

### 3️⃣ C'est tout ! 🎉

Le scraper s'exécutera automatiquement toutes les 30 minutes (00:05, 00:35, 01:05...).

Les résultats sont dans : `output/json/` et `output/csv/`

📱 **Depuis votre smartphone** : Téléchargez l'app **GitHub Mobile** pour consulter les résultats en temps réel !

---

## 📋 Installation locale (optionnel)

Si vous voulez tester localement avant de déployer :

### Prérequis

```bash
python --version  # Python 3.8+
```

### Installation

```bash
# Cloner le repository
git clone https://github.com/VOTRE_USERNAME/winamax-scraper.git
cd winamax-scraper

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Installer Playwright
playwright install chromium

# Installer Tesseract OCR (pour la méthode OCR)
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr tesseract-ocr-fra
# Mac:
brew install tesseract tesseract-lang
```

### Test

```bash
# Tester que tout fonctionne
python test_scraper.py

# Exécuter le scraper
python main.py --method playwright
```

---

## 📦 Structure du projet

```
winamax-scraper/
├── .github/
│   └── workflows/
│       └── scrape_cotes.yml      # Configuration GitHub Actions
├── scrapers/
│   ├── __init__.py
│   ├── selenium_scraper.py       # Méthode 1: Selenium
│   ├── playwright_scraper.py     # Méthode 2: Playwright (recommandé)
│   └── ocr_scraper.py            # Méthode 3: OCR avec Tesseract
├── utils/
│   ├── __init__.py
│   └── data_exporter.py          # Export JSON/CSV
├── output/
│   ├── json/                     # Résultats JSON
│   ├── csv/                      # Résultats CSV
│   └── screenshots/              # Captures d'écran
├── main.py                       # Script principal
├── config.py                     # Configuration
├── test_scraper.py               # Tests
├── requirements.txt              # Dépendances Python
├── .gitignore
├── README.md                     # Ce fichier
└── GITHUB_ACTIONS_SETUP.md       # Guide détaillé GitHub Actions
```

---

## 🚀 Utilisation

### Avec GitHub Actions (automatique)

Le workflow s'exécute automatiquement toutes les 30 minutes avec un décalage de 5 minutes pour ne pas rater les cotes qui apparaissent pile à l'heure.

**Planning** : 00:05, 00:35, 01:05, 01:35, 02:05, 02:35... ⏰

#### Exécution manuelle

1. Aller dans l'onglet **Actions** sur GitHub
2. Sélectionner "Scrape Cotes Boostées Winamax"
3. Cliquer sur **Run workflow**

### Localement (manuel)

```bash
# Méthode Playwright (recommandé - rapide)
python main.py --method playwright

# Méthode Selenium
python main.py --method selenium

# Méthode OCR
python main.py --method ocr

# Toutes les méthodes
python main.py --method all

# Options supplémentaires
python main.py --method playwright --no-headless  # Voir le navigateur
python main.py --method playwright --export json  # Seulement JSON
python main.py --method all --delay 5             # Délai personnalisé
```

---

## 📊 Format des données

### JSON

```json
{
  "timestamp": "2026-01-03T14:35:00",
  "count": 5,
  "cotes": [
    {
      "timestamp": "2026-01-03T14:35:12",
      "method": "playwright",
      "heure": "20:00",
      "sport": "Premier League",
      "competition": "Brighton - Burnley",
      "description": "Plus de 2,5 buts",
      "cote_originale": "2,83",
      "cote_boostee": "3,50"
    }
  ]
}
```

### CSV

```csv
timestamp,method,heure,sport,competition,description,cote_originale,cote_boostee
2026-01-03T14:35:12,playwright,20:00,Premier League,Brighton - Burnley,Plus de 2,5 buts,2.83,3.50
```

---

## 🔍 Détails des méthodes

| Méthode | Vitesse | Précision | Avantages | Inconvénients |
|---------|---------|-----------|-----------|---------------|
| **Playwright** ⭐ | ⚡⚡⚡ | ✅✅✅ | Rapide, moderne, fiable | Nécessite Node.js |
| **Selenium** | ⚡⚡ | ✅✅✅ | Compatible partout | Plus lent |
| **OCR** | ⚡ | ✅✅ | Fonctionne même si le HTML change | Moins précis |

💡 **Recommandation** : Utilisez **Playwright** pour la rapidité et la fiabilité.

---

## ⏰ Configuration du planning GitHub Actions

### Modifier les horaires

Éditez `.github/workflows/scrape_cotes.yml` :

```yaml
on:
  schedule:
    # Format: minute heure jour mois jour_semaine
    - cron: '5,35 * * * *'  # Actuel: :05 et :35 de chaque heure
    
    # Autres exemples:
    # - cron: '0,30 * * * *'  # :00 et :30
    # - cron: '*/15 * * * *'  # Toutes les 15 minutes
    # - cron: '0 */2 * * *'   # Toutes les 2 heures
```

### Pourquoi le décalage de 5 minutes ?

Les cotes boostées apparaissent souvent **pile à l'heure** (20:00:00, 21:00:00).

Si le scraper tourne à 20:00:00 mais que la cote apparaît à 20:00:20, elle est **ratée** ! 😱

Solution : Exécuter à **20:05** et **20:35** → aucune cote ratée ! ✅

---

## 📱 Consultation depuis smartphone

### GitHub Mobile App

1. Télécharger **GitHub Mobile** (iOS/Android)
2. Se connecter à votre compte
3. Ouvrir le repo `winamax-scraper`
4. Naviguer dans `output/json/` ou `output/csv/`
5. Cliquer sur un fichier → **View raw** → Partager/Télécharger

### Navigateur web

Allez sur `github.com/VOTRE_USERNAME/winamax-scraper/tree/main/output`

---

## 🛑 Arrêter/Modifier le scraping

### Désactiver temporairement

1. **Actions** → Workflow → **⋮** → **Disable workflow**

### Changer la fréquence

Modifiez le cron dans `.github/workflows/scrape_cotes.yml`

### Supprimer

Supprimez le fichier `.github/workflows/scrape_cotes.yml`

---

## ⚙️ Configuration avancée

### config.py

```python
# URL cible
TARGET_URL = "https://www.winamax.fr/paris-sportifs/sports/100000"

# Paramètres de scraping
HEADLESS = True        # Mode sans interface
TIMEOUT = 30           # Timeout en secondes
DELAY = 2              # Délai entre actions

# Export
OUTPUT_DIR = "output"
```

---

## 🐛 Dépannage

### Le workflow ne s'exécute pas

- ✅ Vérifier que `.github/workflows/scrape_cotes.yml` existe
- ✅ Activer "Read and write permissions" dans Settings → Actions

### Erreur "playwright: not found"

```bash
playwright install chromium
```

### Erreur Tesseract

Windows : Télécharger depuis [ici](https://github.com/UB-Mannheim/tesseract/wiki)

Linux :
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-fra
```

### Aucune donnée extraite

- Le site a peut-être changé de structure
- Essayez une autre méthode : `--method all`
- Vérifiez les logs dans Actions

---

## ⚠️ Avertissement

Ce projet est **à des fins éducatives uniquement**.

- ✅ Respectez les conditions d'utilisation de Winamax
- ✅ Ne surchargez pas leurs serveurs (le scraping toutes les 30 min est raisonnable)
- ✅ Les paris sportifs comportent des risques

---

## 📄 Licence

MIT License - Libre d'utilisation pour des projets personnels et éducatifs.

---

## 🤝 Contribution

Les contributions sont bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit (`git commit -m 'Ajout fonctionnalité'`)
4. Push (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

---

## 📚 Documentation complète

- [📖 Guide GitHub Actions détaillé](GITHUB_ACTIONS_SETUP.md)
- [🔧 Configuration avancée](config.py)
- [🧪 Tests](test_scraper.py)

---

## 💡 Idées d'améliorations

- [ ] Notifications Discord/Telegram lors de nouvelles cotes
- [ ] Dashboard web pour visualiser l'historique
- [ ] Filtre par sport favori
- [ ] Alerte si cote > X
- [ ] Export vers Google Sheets
- [ ] Analyse statistique des meilleures cotes

---

**Fait avec ❤️ pour ne plus jamais rater une cote boostée !** 🚀

Questions ? Ouvrez une [Issue](../../issues) !

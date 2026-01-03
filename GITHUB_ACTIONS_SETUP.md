# 🤖 Configuration GitHub Actions

Ce guide explique comment configurer l'exécution automatique du scraper toutes les 30 minutes.

## ⏰ Planning d'exécution

Le workflow s'exécute automatiquement **toutes les 30 minutes** avec un **décalage de 5 minutes** :

- ✅ 00:05, 00:35
- ✅ 01:05, 01:35
- ✅ 02:05, 02:35
- ✅ ... et ainsi de suite

Ce décalage de 5 minutes permet de **ne pas rater les cotes qui apparaissent pile à l'heure** (20:00:00, 21:00:00, etc.).

## 📋 Prérequis

1. Créer un repository GitHub
2. Activer GitHub Actions (gratuit pour les repos publics)

## 🚀 Installation

### 1. Créer le repository

```bash
# Depuis votre smartphone, utilisez l'app GitHub ou via le navigateur
# Créer un nouveau repository : winamax-scraper
```

### 2. Pousser le code

```bash
git init
git add .
git commit -m "Initial commit: Winamax scraper"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/winamax-scraper.git
git push -u origin main
```

### 3. Activer GitHub Actions

Le workflow dans `.github/workflows/scrape_cotes.yml` sera automatiquement détecté et activé.

## 🔧 Configuration du workflow

### Horaires personnalisés

Pour modifier les horaires, éditez `.github/workflows/scrape_cotes.yml` :

```yaml
on:
  schedule:
    # Format cron: minute heure jour mois jour_semaine
    - cron: '5,35 * * * *'  # Actuel: :05 et :35 de chaque heure
    
    # Exemples d'autres configurations:
    # - cron: '0,30 * * * *'  # :00 et :30 (à l'heure pile)
    # - cron: '10,40 * * * *' # :10 et :40
    # - cron: '*/15 * * * *'  # Toutes les 15 minutes
    # - cron: '0 * * * *'     # Toutes les heures à :00
```

### Exécution manuelle

Depuis GitHub.com :
1. Aller dans l'onglet **Actions**
2. Sélectionner le workflow "Scrape Cotes Boostées Winamax"
3. Cliquer sur **Run workflow**

### Méthode de scraping

Par défaut, le workflow utilise **Playwright** (rapide et fiable).

Pour changer la méthode, éditez le fichier workflow :

```yaml
- name: 🎯 Run scraper
  run: |
    python main.py --method playwright --export all  # Méthode actuelle
    # python main.py --method selenium --export all   # Alternative
    # python main.py --method ocr --export all        # OCR
    # python main.py --method all --export all        # Toutes les méthodes
```

## 📊 Consulter les résultats

### Via GitHub

1. Les résultats sont automatiquement **commit et push** dans le dossier `output/`
2. Naviguez dans votre repo : `output/json/` ou `output/csv/`

### Structure des fichiers

```
output/
├── json/
│   ├── cotes_2026-01-03_14-05-30.json
│   ├── cotes_2026-01-03_14-35-15.json
│   └── ...
├── csv/
│   ├── cotes_2026-01-03_14-05-30.csv
│   └── ...
└── screenshots/
    ├── playwright_2026-01-03_14-05-30.png
    └── ...
```

### Depuis votre smartphone

- **App GitHub** : Naviguez dans les fichiers du repo
- **GitHub Mobile** : Voir les commits et les fichiers
- **Navigateur web** : github.com/VOTRE_USERNAME/winamax-scraper

## 🔍 Vérifier l'exécution

### Logs en temps réel

1. Onglet **Actions**
2. Cliquer sur une exécution
3. Voir les logs détaillés de chaque étape

### Notifications

GitHub envoie des emails en cas d'échec du workflow.

Pour personnaliser les notifications :
- **Settings** → **Notifications** → **Actions**

## ⚠️ Limites GitHub Actions

### Plan gratuit (repos publics)
- ✅ Minutes illimitées
- ✅ Stockage : 500 MB
- ✅ Pas de limite d'exécutions

### Plan gratuit (repos privés)
- ⚠️ 2000 minutes/mois
- ⚠️ Stockage : 500 MB

### Calcul de consommation

Avec 30 minutes d'intervalle :
- 48 exécutions/jour
- ~2 minutes/exécution
- **~96 minutes/jour** pour un repo privé

💡 **Solution** : Utilisez un repository **public** pour des exécutions illimitées.

## 🛑 Arrêter le scraping automatique

### Temporairement

1. Onglet **Actions**
2. Workflow "Scrape Cotes Boostées"
3. ⋮ (menu) → **Disable workflow**

### Définitivement

Supprimer ou commenter dans `.github/workflows/scrape_cotes.yml` :

```yaml
on:
  # schedule:
  #   - cron: '5,35 * * * *'
  workflow_dispatch:  # Garder l'exécution manuelle
```

## 🔐 Sécurité

### Tokens et secrets

Le workflow utilise automatiquement `GITHUB_TOKEN` pour :
- Commit les résultats
- Push vers le repository

Aucune configuration supplémentaire n'est nécessaire.

### Données sensibles

⚠️ Les données scrapées sont **publiques** si votre repo est public.

Pour un repo privé :
1. **Settings** → **General**
2. Scroll vers le bas
3. **Change repository visibility** → Private

## 📱 Utilisation depuis smartphone

### Voir les résultats

1. **GitHub Mobile App** : Téléchargez l'app officielle
2. Naviguez vers votre repo
3. Consultez les fichiers dans `output/`

### Télécharger les données

- Depuis l'app : View raw → Share → Télécharger
- Depuis le web : Cliquer sur le fichier → Download

### Exécuter manuellement

1. App GitHub → Repo → Actions
2. Workflow → Run workflow → Run

## 🐛 Dépannage

### Le workflow ne s'exécute pas

```bash
# Vérifier que le fichier workflow est au bon endroit
.github/workflows/scrape_cotes.yml

# Vérifier la syntaxe YAML
# Utilisez un validateur YAML en ligne
```

### Erreurs de permissions

Si le push échoue :

1. **Settings** → **Actions** → **General**
2. **Workflow permissions**
3. Sélectionner **Read and write permissions**
4. Sauvegarder

### Aucune donnée extraite

- Vérifier les logs du workflow
- Le site a peut-être changé de structure
- Essayer une autre méthode de scraping

## 💡 Astuces

### Combiner avec d'autres outils

Export automatique vers :
- **Google Sheets** : Utiliser une GitHub Action tierce
- **Discord/Telegram** : Notifications avec webhooks
- **Email** : Alertes via SendGrid

### Optimisation

```yaml
# Utiliser le cache pour accélérer
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

## 📈 Monitoring

### Tableau de bord

Créez un fichier `dashboard.md` avec un script qui analyse les JSON :

```python
# Générer des statistiques
# - Nombre de cotes par jour
# - Cotes les plus fréquentes
# - Meilleurs boosts
```

### Alertes personnalisées

Ajoutez une étape dans le workflow pour envoyer des alertes si certaines conditions sont remplies :

```yaml
- name: 🔔 Check for high odds
  run: |
    python check_odds.py --threshold 5.0
```

## ✅ Checklist de déploiement

- [ ] Repository créé sur GitHub
- [ ] Code pushé avec tous les fichiers
- [ ] Workflow présent dans `.github/workflows/`
- [ ] Permissions "Read and write" activées
- [ ] Premier test d'exécution manuelle réussi
- [ ] Vérification que les résultats sont commit
- [ ] Application mobile installée (optionnel)

## 🎉 C'est prêt !

Votre scraper tournera automatiquement toutes les 30 minutes et vous ne raterez plus aucune cote boostée ! 🚀

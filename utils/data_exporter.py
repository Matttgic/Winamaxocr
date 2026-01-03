"""
Utilitaires pour exporter les données scrapées
"""
import json
import csv
from datetime import datetime
from pathlib import Path
import config


class DataExporter:
    def export_json(self, data, filename=None):
        """Exporte les données en JSON"""
        if filename is None:
            timestamp = datetime.now().strftime(config.DATETIME_FORMAT)
            filename = f"cotes_{timestamp}.json"
        
        filepath = config.JSON_DIR / filename
        
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'count': len(data),
            'cotes': data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def export_csv(self, data, filename=None):
        """Exporte les données en CSV"""
        if filename is None:
            timestamp = datetime.now().strftime(config.DATETIME_FORMAT)
            filename = f"cotes_{timestamp}.csv"
        
        filepath = config.CSV_DIR / filename
        
        if not data:
            return filepath
        
        # Déterminer toutes les clés possibles
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        return filepath
    
    def append_to_history(self, data, history_file='history.json'):
        """Ajoute les données à un fichier historique"""
        filepath = config.JSON_DIR / history_file
        
        # Charger l'historique existant
        history = []
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []
        
        # Ajouter les nouvelles données
        history.extend(data)
        
        # Sauvegarder
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        return filepath

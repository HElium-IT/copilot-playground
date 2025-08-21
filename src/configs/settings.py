"""
Configurazioni e impostazioni dell'applicazione
"""

import os
from typing import Dict, Any
import json
from pathlib import Path

class Settings:
    def __init__(self):
        self.config_dir = Path.home() / ".studio_app"
        self.config_file = self.config_dir / "config.json"
        self.default_settings = {
            "github_copilot_api_key": "",
            "theme": "dark",
            "layout": {
                "chat_width_percent": 50,
                "notes_panel_visible": True,
                "toolbar_visible": True
            },
            "window": {
                "width": 1200,
                "height": 800,
                "maximized": False
            },
            "plugins": {
                "enabled": ["chat", "notes", "code_editor"]
            }
        }
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Carica le impostazioni dal file di configurazione"""
        if not self.config_file.exists():
            self.save_settings(self.default_settings)
            return self.default_settings.copy()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # Unisce con le impostazioni predefinite per eventuali nuove chiavi
                merged = self.default_settings.copy()
                merged.update(settings)
                return merged
        except (json.JSONDecodeError, Exception):
            return self.default_settings.copy()
    
    def save_settings(self, settings: Dict[str, Any] = None):
        """Salva le impostazioni nel file di configurazione"""
        if settings is None:
            settings = self.settings
        
        self.config_dir.mkdir(exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
    
    def get(self, key: str, default=None):
        """Ottiene un valore dalle impostazioni"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Imposta un valore nelle impostazioni"""
        self.settings[key] = value
        self.save_settings()
    
    def get_github_api_key(self) -> str:
        """Ottiene la chiave API di GitHub Copilot"""
        # Prima controlla la variabile d'ambiente
        api_key = os.getenv("GITHUB_COPILOT_API_KEY")
        if api_key:
            return api_key
        
        # Poi controlla nelle impostazioni
        return self.settings.get("github_copilot_api_key", "")
    
    def set_github_api_key(self, api_key: str):
        """Imposta la chiave API di GitHub Copilot"""
        self.set("github_copilot_api_key", api_key)

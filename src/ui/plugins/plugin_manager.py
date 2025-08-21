"""
Gestore dei plugin per l'architettura modulare
"""

import os
import importlib
import importlib.util
from typing import Dict, List, Any, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.configs.settings import Settings

class PluginBase(ABC):
    """Classe base per tutti i plugin"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Restituisce il nome del plugin"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Restituisce la descrizione del plugin"""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Restituisce la versione del plugin"""
        pass
    
    @abstractmethod
    def initialize(self, settings: 'Settings') -> bool:
        """Inizializza il plugin"""
        pass
    
    @abstractmethod
    def create_widget(self, parent):
        """Crea il widget del plugin"""
        pass
    
    def cleanup(self):
        """Pulisce le risorse del plugin"""
        pass

class PluginManager:
    def __init__(self, settings: 'Settings'):
        self.settings = settings
        self.loaded_plugins: Dict[str, PluginBase] = {}
        self.available_plugins: Dict[str, str] = {}
        
        self.discover_plugins()
    
    def discover_plugins(self):
        """Scopre i plugin disponibili"""
        plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
        
        if not os.path.exists(plugins_dir):
            os.makedirs(plugins_dir)
            return
        
        for item in os.listdir(plugins_dir):
            if item.endswith('.py') and not item.startswith('__'):
                plugin_name = item[:-3]  # Rimuovi .py
                self.available_plugins[plugin_name] = os.path.join(plugins_dir, item)
    
    def load_plugin(self, plugin_name: str) -> bool:
        """Carica un plugin"""
        if plugin_name in self.loaded_plugins:
            return True
        
        if plugin_name not in self.available_plugins:
            print(f"Plugin '{plugin_name}' non trovato")
            return False
        
        try:
            plugin_path = self.available_plugins[plugin_name]
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Cerca la classe del plugin
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, PluginBase) and 
                    attr != PluginBase):
                    plugin_class = attr
                    break
            
            if plugin_class is None:
                print(f"Nessuna classe plugin valida trovata in '{plugin_name}'")
                return False
            
            # Crea un'istanza del plugin
            plugin_instance = plugin_class()
            
            # Inizializza il plugin
            if plugin_instance.initialize(self.settings):
                self.loaded_plugins[plugin_name] = plugin_instance
                print(f"Plugin '{plugin_name}' caricato con successo")
                return True
            else:
                print(f"Errore nell'inizializzazione del plugin '{plugin_name}'")
                return False
                
        except Exception as e:
            print(f"Errore nel caricamento del plugin '{plugin_name}': {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """Scarica un plugin"""
        if plugin_name not in self.loaded_plugins:
            return False
        
        try:
            plugin = self.loaded_plugins[plugin_name]
            plugin.cleanup()
            del self.loaded_plugins[plugin_name]
            print(f"Plugin '{plugin_name}' scaricato")
            return True
        except Exception as e:
            print(f"Errore nello scaricamento del plugin '{plugin_name}': {e}")
            return False
    
    def get_loaded_plugins(self) -> Dict[str, PluginBase]:
        """Restituisce i plugin caricati"""
        return self.loaded_plugins.copy()
    
    def get_available_plugins(self) -> List[str]:
        """Restituisce la lista dei plugin disponibili"""
        return list(self.available_plugins.keys())
    
    def get_plugin(self, plugin_name: str) -> PluginBase:
        """Restituisce un plugin specifico"""
        return self.loaded_plugins.get(plugin_name)
    
    def is_plugin_loaded(self, plugin_name: str) -> bool:
        """Controlla se un plugin è caricato"""
        return plugin_name in self.loaded_plugins

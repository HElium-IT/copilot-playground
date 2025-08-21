"""
Finestra principale dell'applicazione con layout customizzabile
"""

import tkinter as tk
import customtkinter as ctk
from typing import Dict, Any
from src.ui.components.toolbar import Toolbar
from src.ui.components.chat_panel import ChatPanel
from src.ui.components.notes_panel import NotesPanel
from src.ui.plugins.plugin_manager import PluginManager
from src.config.settings import Settings

class MainWindow:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.plugin_manager = PluginManager(settings)
        
        # Crea la finestra principale
        self.root = ctk.CTk()
        self.root.title("Studio App - GitHub Copilot Integration")
        
        # Configura la finestra
        window_config = self.settings.get("window", {})
        self.root.geometry(f"{window_config.get('width', 1200)}x{window_config.get('height', 800)}")
        
        if window_config.get('maximized', False):
            self.root.state('zoomed')
        
        # Configura il layout
        self.setup_layout()
        
        # Configura gli event handlers
        self.setup_events()
        
        # Carica i plugin
        self.load_plugins()
    
    def setup_layout(self):
        """Configura il layout principale"""
        # Configura il grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Toolbar (row 0)
        self.toolbar = Toolbar(self.root, self.plugin_manager, self.settings)
        self.toolbar.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 0))
        
        # Frame principale per il contenuto (row 1)
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configura il layout del frame principale
        self.setup_main_layout()
    
    def setup_main_layout(self):
        """Configura il layout del frame principale"""
        layout_config = self.settings.get("layout", {})
        chat_width_percent = layout_config.get("chat_width_percent", 50)
        
        # Calcola i pesi delle colonne
        chat_weight = chat_width_percent / 100
        notes_weight = (100 - chat_width_percent) / 100
        
        # Configura il grid del frame principale
        self.main_frame.grid_columnconfigure(0, weight=int(chat_weight * 100))
        self.main_frame.grid_columnconfigure(1, weight=int(notes_weight * 100))
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Chat panel (colonna sinistra)
        self.chat_panel = ChatPanel(self.main_frame, self.settings, self.plugin_manager)
        self.chat_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 2.5), pady=0)
        
        # Notes panel (colonna destra)
        if layout_config.get("notes_panel_visible", True):
            self.notes_panel = NotesPanel(self.main_frame, self.settings)
            self.notes_panel.grid(row=0, column=1, sticky="nsew", padx=(2.5, 0), pady=0)
        else:
            self.notes_panel = None
    
    def setup_events(self):
        """Configura gli event handlers"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Configure>", self.on_window_configure)
    
    def on_closing(self):
        """Gestisce la chiusura dell'applicazione"""
        # Salva la configurazione della finestra
        if self.root.state() == 'zoomed':
            self.settings.set("window", {
                **self.settings.get("window", {}),
                "maximized": True
            })
        else:
            self.settings.set("window", {
                "width": self.root.winfo_width(),
                "height": self.root.winfo_height(),
                "maximized": False
            })
        
        # Chiudi l'applicazione
        self.root.destroy()
    
    def on_window_configure(self, event):
        """Gestisce il ridimensionamento della finestra"""
        if event.widget == self.root:
            # Aggiorna la configurazione del layout se necessario
            pass
    
    def load_plugins(self):
        """Carica i plugin abilitati"""
        enabled_plugins = self.settings.get("plugins", {}).get("enabled", [])
        for plugin_name in enabled_plugins:
            self.plugin_manager.load_plugin(plugin_name)
    
    def toggle_notes_panel(self):
        """Mostra/nasconde il pannello delle note"""
        layout_config = self.settings.get("layout", {})
        notes_visible = layout_config.get("notes_panel_visible", True)
        
        if notes_visible and self.notes_panel:
            self.notes_panel.grid_remove()
            self.notes_panel = None
            layout_config["notes_panel_visible"] = False
        elif not notes_visible:
            self.notes_panel = NotesPanel(self.main_frame, self.settings)
            self.notes_panel.grid(row=0, column=1, sticky="nsew", padx=(2.5, 0), pady=0)
            layout_config["notes_panel_visible"] = True
        
        self.settings.set("layout", layout_config)
    
    def adjust_layout(self, chat_width_percent: int):
        """Regola la larghezza del pannello chat"""
        layout_config = self.settings.get("layout", {})
        layout_config["chat_width_percent"] = chat_width_percent
        self.settings.set("layout", layout_config)
        
        # Ricostruisce il layout
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.setup_main_layout()
    
    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()

"""
Toolbar principale con pulsanti per gestire i plugin e il layout
"""

import customtkinter as ctk
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.ui.plugins.plugin_manager import PluginManager
    from src.config.settings import Settings

class Toolbar(ctk.CTkFrame):
    def __init__(self, parent, plugin_manager: 'PluginManager', settings: 'Settings'):
        super().__init__(parent)
        self.plugin_manager = plugin_manager
        self.settings = settings
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura l'interfaccia della toolbar"""
        # Configura il layout
        self.grid_columnconfigure(0, weight=1)
        
        # Frame per i pulsanti a sinistra
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Frame per i pulsanti a destra
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="e", padx=5, pady=5)
        
        # Pulsanti principali
        self.create_main_buttons()
        
        # Pulsanti di configurazione
        self.create_config_buttons()
    
    def create_main_buttons(self):
        """Crea i pulsanti principali per i plugin"""
        # Pulsante Chat
        self.chat_btn = ctk.CTkButton(
            self.left_frame,
            text="💬 Chat",
            width=80,
            command=self.toggle_chat
        )
        self.chat_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Pulsante Note
        self.notes_btn = ctk.CTkButton(
            self.left_frame,
            text="📝 Note",
            width=80,
            command=self.toggle_notes
        )
        self.notes_btn.grid(row=0, column=1, padx=(0, 5))
        
        # Pulsante Editor
        self.editor_btn = ctk.CTkButton(
            self.left_frame,
            text="📄 Editor",
            width=80,
            command=self.toggle_editor
        )
        self.editor_btn.grid(row=0, column=2, padx=(0, 5))
        
        # Pulsante Plugin Manager
        self.plugins_btn = ctk.CTkButton(
            self.left_frame,
            text="🔧 Plugin",
            width=80,
            command=self.open_plugin_manager
        )
        self.plugins_btn.grid(row=0, column=3, padx=(0, 5))
    
    def create_config_buttons(self):
        """Crea i pulsanti di configurazione"""
        # Slider per regolare la larghezza del chat
        self.layout_label = ctk.CTkLabel(
            self.right_frame,
            text="Layout:"
        )
        self.layout_label.grid(row=0, column=0, padx=(0, 5))
        
        layout_config = self.settings.get("layout", {})
        chat_width = layout_config.get("chat_width_percent", 50)
        
        self.layout_slider = ctk.CTkSlider(
            self.right_frame,
            from_=20,
            to=80,
            number_of_steps=12,
            command=self.on_layout_change
        )
        self.layout_slider.set(chat_width)
        self.layout_slider.grid(row=0, column=1, padx=(0, 5))
        
        # Pulsante Impostazioni
        self.settings_btn = ctk.CTkButton(
            self.right_frame,
            text="⚙️",
            width=30,
            command=self.open_settings
        )
        self.settings_btn.grid(row=0, column=2, padx=(0, 5))
    
    def toggle_chat(self):
        """Attiva/disattiva il pannello chat"""
        print("Toggle chat panel")
        # TODO: Implementa la logica per mostrare/nascondere il chat
    
    def toggle_notes(self):
        """Attiva/disattiva il pannello note"""
        # Chiama il metodo della finestra principale
        if hasattr(self.master.master, 'toggle_notes_panel'):
            self.master.master.toggle_notes_panel()
    
    def toggle_editor(self):
        """Attiva/disattiva l'editor di codice"""
        print("Toggle code editor")
        # TODO: Implementa la logica per l'editor di codice
    
    def open_plugin_manager(self):
        """Apre il gestore dei plugin"""
        from src.ui.dialogs.plugin_manager_dialog import PluginManagerDialog
        dialog = PluginManagerDialog(self, self.plugin_manager, self.settings)
    
    def on_layout_change(self, value):
        """Gestisce il cambio di layout"""
        chat_width = int(value)
        if hasattr(self.master.master, 'adjust_layout'):
            self.master.master.adjust_layout(chat_width)
    
    def open_settings(self):
        """Apre la finestra delle impostazioni"""
        from src.ui.dialogs.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self, self.settings)

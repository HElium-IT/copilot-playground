"""
Dialog per la gestione dei plugin
"""

import customtkinter as ctk
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.ui.plugins.plugin_manager import PluginManager
    from src.configs.settings import Settings

class PluginManagerDialog(ctk.CTkToplevel):
    def __init__(self, parent, plugin_manager: 'PluginManager', settings: 'Settings'):
        super().__init__(parent)
        self.plugin_manager = plugin_manager
        self.settings = settings
        
        self.title("Gestione Plugin")
        self.geometry("600x500")
        self.transient(parent)
        self.grab_set()
        
        # Centra la finestra
        self.center_window()
        
        self.setup_ui()
        self.refresh_plugin_list()
    
    def center_window(self):
        """Centra la finestra rispetto al parent"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"600x500+{x}+{y}")
    
    def setup_ui(self):
        """Configura l'interfaccia"""
        # Frame principale
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titolo
        title_label = ctk.CTkLabel(
            main_frame,
            text="🔧 Gestione Plugin",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Frame per la lista plugin
        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Header della lista
        header_frame = ctk.CTkFrame(list_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(
            header_frame,
            text="Plugin Disponibili",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=10, pady=10)
        
        self.refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Aggiorna",
            width=100,
            command=self.refresh_plugin_list
        )
        self.refresh_btn.pack(side="right", padx=10, pady=10)
        
        # Scrollable frame per i plugin
        self.scrollable_frame = ctk.CTkScrollableFrame(list_frame)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Info panel
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=(0, 10))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="ℹ️ Info Plugin",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.info_text = ctk.CTkTextbox(
            info_frame,
            height=80,
            wrap="word"
        )
        self.info_text.pack(fill="x", padx=15, pady=(0, 15))
        
        # Pulsanti
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        self.close_btn = ctk.CTkButton(
            buttons_frame,
            text="Chiudi",
            command=self.destroy
        )
        self.close_btn.pack(side="right")
    
    def refresh_plugin_list(self):
        """Aggiorna la lista dei plugin"""
        # Pulisci la lista corrente
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Ottieni i plugin disponibili
        available_plugins = self.plugin_manager.get_available_plugins()
        loaded_plugins = self.plugin_manager.get_loaded_plugins()
        
        if not available_plugins:
            # Messaggio se non ci sono plugin
            no_plugins_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="Nessun plugin trovato nella directory plugins/",
                font=ctk.CTkFont(size=12)
            )
            no_plugins_label.pack(pady=20)
            
            # Suggerimento per creare plugin
            suggestion_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="Puoi creare plugin personalizzati nella cartella src/ui/plugins/plugins/",
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            suggestion_label.pack(pady=(0, 20))
            return
        
        # Crea i widget per ogni plugin
        for plugin_name in available_plugins:
            plugin_frame = ctk.CTkFrame(self.scrollable_frame)
            plugin_frame.pack(fill="x", padx=5, pady=2)
            
            # Nome del plugin
            name_label = ctk.CTkLabel(
                plugin_frame,
                text=plugin_name,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            name_label.pack(side="left", padx=15, pady=10)
            
            # Status
            is_loaded = plugin_name in loaded_plugins
            status_text = "✅ Caricato" if is_loaded else "⭕ Non caricato"
            status_label = ctk.CTkLabel(
                plugin_frame,
                text=status_text,
                font=ctk.CTkFont(size=12)
            )
            status_label.pack(side="left", padx=(10, 0))
            
            # Pulsanti azione
            if is_loaded:
                # Info button
                info_btn = ctk.CTkButton(
                    plugin_frame,
                    text="Info",
                    width=60,
                    command=lambda p=plugin_name: self.show_plugin_info(p)
                )
                info_btn.pack(side="right", padx=(5, 15), pady=5)
                
                # Unload button
                unload_btn = ctk.CTkButton(
                    plugin_frame,
                    text="Scarica",
                    width=70,
                    command=lambda p=plugin_name: self.unload_plugin(p)
                )
                unload_btn.pack(side="right", padx=5, pady=5)
            else:
                # Load button
                load_btn = ctk.CTkButton(
                    plugin_frame,
                    text="Carica",
                    width=70,
                    command=lambda p=plugin_name: self.load_plugin(p)
                )
                load_btn.pack(side="right", padx=(5, 15), pady=5)
    
    def load_plugin(self, plugin_name: str):
        """Carica un plugin"""
        success = self.plugin_manager.load_plugin(plugin_name)
        if success:
            self.show_message("Successo", f"Plugin '{plugin_name}' caricato con successo!")
        else:
            self.show_message("Errore", f"Errore nel caricamento del plugin '{plugin_name}'")
        
        self.refresh_plugin_list()
    
    def unload_plugin(self, plugin_name: str):
        """Scarica un plugin"""
        success = self.plugin_manager.unload_plugin(plugin_name)
        if success:
            self.show_message("Successo", f"Plugin '{plugin_name}' scaricato con successo!")
        else:
            self.show_message("Errore", f"Errore nello scaricamento del plugin '{plugin_name}'")
        
        self.refresh_plugin_list()
    
    def show_plugin_info(self, plugin_name: str):
        """Mostra informazioni sul plugin"""
        plugin = self.plugin_manager.get_plugin(plugin_name)
        if plugin:
            info_text = f"Nome: {plugin.get_name()}\\n"
            info_text += f"Descrizione: {plugin.get_description()}\\n"
            info_text += f"Versione: {plugin.get_version()}"
            
            self.info_text.delete("1.0", "end")
            self.info_text.insert("1.0", info_text)
        else:
            self.info_text.delete("1.0", "end")
            self.info_text.insert("1.0", f"Informazioni non disponibili per '{plugin_name}'")
    
    def show_message(self, title: str, message: str):
        """Mostra un messaggio"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("350x150")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centra il dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (150 // 2)
        dialog.geometry(f"350x150+{x}+{y}")
        
        # Messaggio
        msg_label = ctk.CTkLabel(dialog, text=message, wraplength=300)
        msg_label.pack(pady=20)
        
        # Pulsante OK
        ok_btn = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
        ok_btn.pack(pady=10)

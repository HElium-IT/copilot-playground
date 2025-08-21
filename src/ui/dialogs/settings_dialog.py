"""
Dialog per la gestione delle impostazioni
"""

import customtkinter as ctk
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.config.settings import Settings

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent, settings: 'Settings'):
        super().__init__(parent)
        self.settings = settings
        
        self.title("Impostazioni")
        self.geometry("500x400")
        self.transient(parent)
        self.grab_set()
        
        # Centra la finestra
        self.center_window()
        
        self.setup_ui()
        self.load_settings()
    
    def center_window(self):
        """Centra la finestra rispetto al parent"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        self.geometry(f"500x400+{x}+{y}")
    
    def setup_ui(self):
        """Configura l'interfaccia"""
        # Frame principale
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titolo
        title_label = ctk.CTkLabel(
            main_frame,
            text="⚙️ Impostazioni",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Sezione API
        api_frame = ctk.CTkFrame(main_frame)
        api_frame.pack(fill="x", pady=(0, 10))
        
        api_label = ctk.CTkLabel(
            api_frame,
            text="GitHub Copilot API",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        api_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Campo API Key
        ctk.CTkLabel(
            api_frame,
            text="API Key:"
        ).pack(anchor="w", padx=15, pady=(0, 5))
        
        self.api_key_entry = ctk.CTkEntry(
            api_frame,
            placeholder_text="Inserisci la tua GitHub Copilot API Key",
            show="*",
            width=400
        )
        self.api_key_entry.pack(padx=15, pady=(0, 10))
        
        # Test API button
        self.test_api_btn = ctk.CTkButton(
            api_frame,
            text="Testa API",
            command=self.test_api_key
        )
        self.test_api_btn.pack(padx=15, pady=(0, 15))
        
        # Sezione Aspetto
        appearance_frame = ctk.CTkFrame(main_frame)
        appearance_frame.pack(fill="x", pady=(0, 10))
        
        appearance_label = ctk.CTkLabel(
            appearance_frame,
            text="Aspetto",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        appearance_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Tema
        ctk.CTkLabel(
            appearance_frame,
            text="Tema:"
        ).pack(anchor="w", padx=15, pady=(0, 5))
        
        self.theme_option = ctk.CTkOptionMenu(
            appearance_frame,
            values=["dark", "light"],
            command=self.on_theme_change
        )
        self.theme_option.pack(anchor="w", padx=15, pady=(0, 15))
        
        # Sezione Layout
        layout_frame = ctk.CTkFrame(main_frame)
        layout_frame.pack(fill="x", pady=(0, 20))
        
        layout_label = ctk.CTkLabel(
            layout_frame,
            text="Layout",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        layout_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Checkbox per pannello note
        self.notes_visible_var = ctk.BooleanVar()\n        self.notes_checkbox = ctk.CTkCheckBox(\n            layout_frame,\n            text=\"Mostra pannello note\",\n            variable=self.notes_visible_var\n        )\n        self.notes_checkbox.pack(anchor=\"w\", padx=15, pady=(0, 10))\n        \n        # Pulsanti\n        buttons_frame = ctk.CTkFrame(main_frame, fg_color=\"transparent\")\n        buttons_frame.pack(fill=\"x\", pady=(0, 10))\n        \n        self.cancel_btn = ctk.CTkButton(\n            buttons_frame,\n            text=\"Annulla\",\n            command=self.cancel\n        )\n        self.cancel_btn.pack(side=\"right\", padx=(5, 0))\n        \n        self.save_btn = ctk.CTkButton(\n            buttons_frame,\n            text=\"Salva\",\n            command=self.save_settings\n        )\n        self.save_btn.pack(side=\"right\")\n    \n    def load_settings(self):\n        \"\"\"Carica le impostazioni correnti\"\"\"\n        # API Key\n        api_key = self.settings.get_github_api_key()\n        if api_key:\n            self.api_key_entry.insert(0, api_key)\n        \n        # Tema\n        theme = self.settings.get(\"theme\", \"dark\")\n        self.theme_option.set(theme)\n        \n        # Layout\n        layout_config = self.settings.get(\"layout\", {})\n        notes_visible = layout_config.get(\"notes_panel_visible\", True)\n        self.notes_visible_var.set(notes_visible)\n    \n    def save_settings(self):\n        \"\"\"Salva le impostazioni\"\"\"\n        # Salva API Key\n        api_key = self.api_key_entry.get().strip()\n        self.settings.set_github_api_key(api_key)\n        \n        # Salva tema\n        theme = self.theme_option.get()\n        self.settings.set(\"theme\", theme)\n        \n        # Salva layout\n        layout_config = self.settings.get(\"layout\", {})\n        layout_config[\"notes_panel_visible\"] = self.notes_visible_var.get()\n        self.settings.set(\"layout\", layout_config)\n        \n        # Applica le modifiche\n        ctk.set_appearance_mode(theme)\n        \n        self.destroy()\n    \n    def cancel(self):\n        \"\"\"Annulla le modifiche\"\"\"\n        self.destroy()\n    \n    def test_api_key(self):\n        \"\"\"Testa l'API key\"\"\"\n        api_key = self.api_key_entry.get().strip()\n        if not api_key:\n            self.show_message(\"Errore\", \"Inserisci prima un'API key\")\n            return\n        \n        # Simula il test (implementare la logica reale)\n        if len(api_key) > 10:\n            self.show_message(\"Successo\", \"API key valida!\")\n        else:\n            self.show_message(\"Errore\", \"API key non valida\")\n    \n    def on_theme_change(self, theme: str):\n        \"\"\"Gestisce il cambio di tema\"\"\"\n        ctk.set_appearance_mode(theme)\n    \n    def show_message(self, title: str, message: str):\n        \"\"\"Mostra un messaggio\"\"\"\n        dialog = ctk.CTkToplevel(self)\n        dialog.title(title)\n        dialog.geometry(\"300x150\")\n        dialog.transient(self)\n        dialog.grab_set()\n        \n        # Centra il dialog\n        dialog.update_idletasks()\n        x = (dialog.winfo_screenwidth() // 2) - (300 // 2)\n        y = (dialog.winfo_screenheight() // 2) - (150 // 2)\n        dialog.geometry(f\"300x150+{x}+{y}\")\n        \n        # Messaggio\n        msg_label = ctk.CTkLabel(dialog, text=message, wraplength=250)\n        msg_label.pack(pady=20)\n        \n        # Pulsante OK\n        ok_btn = ctk.CTkButton(dialog, text=\"OK\", command=dialog.destroy)\n        ok_btn.pack(pady=10)

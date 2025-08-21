"""
Dialog per la gestione delle impostazioni
"""

import customtkinter as ctk
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.configs.settings import Settings

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
        self.notes_visible_var = ctk.BooleanVar()
        self.notes_checkbox = ctk.CTkCheckBox(
            layout_frame, text="Mostra pannello note", variable=self.notes_visible_var
        )
        self.notes_checkbox.pack(anchor="w", padx=15, pady=(0, 10))

        # Pulsanti
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(0, 10))

        self.cancel_btn = ctk.CTkButton(
            buttons_frame, text="Annulla", command=self.cancel
        )
        self.cancel_btn.pack(side="right", padx=(5, 0))

        self.save_btn = ctk.CTkButton(
            buttons_frame, text="Salva", command=self.save_settings
        )
        self.save_btn.pack(side="right")

    def load_settings(self):
        """Carica le impostazioni correnti"""
        # API Key
        api_key = self.settings.get_github_api_key()
        if api_key:
            self.api_key_entry.insert(0, api_key)

        # Tema
        theme = self.settings.get("theme", "dark")
        self.theme_option.set(theme)

        # Layout
        layout_config = self.settings.get("layout", {})
        notes_visible = layout_config.get("notes_panel_visible", True)
        self.notes_visible_var.set(notes_visible)

    def save_settings(self):
        """Salva le impostazioni"""
        # Salva API Key
        api_key = self.api_key_entry.get().strip()
        self.settings.set_github_api_key(api_key)

        # Salva tema
        theme = self.theme_option.get()
        self.settings.set("theme", theme)

        # Salva layout
        layout_config = self.settings.get("layout", {})
        layout_config["notes_panel_visible"] = self.notes_visible_var.get()
        self.settings.set("layout", layout_config)

        # Applica le modifiche
        ctk.set_appearance_mode(theme)

        self.destroy()

    def cancel(self):
        """Annulla le modifiche"""
        self.destroy()

    def test_api_key(self):
        """Testa l'API key"""
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            self.show_message("Errore", "Inserisci prima un'API key")
            return

        # Simula il test (implementare la logica reale)
        if len(api_key) > 10:
            self.show_message("Successo", "API key valida!")
        else:
            self.show_message("Errore", "API key non valida")

    def on_theme_change(self, theme: str):
        """Gestisce il cambio di tema"""
        ctk.set_appearance_mode(theme)

    def show_message(self, title: str, message: str):
        """Mostra un messaggio"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.transient(self)
        dialog.grab_set()

        # Centra il dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (300 // 2)
        y = (dialog.winfo_screenheight() // 2) - (150 // 2)
        dialog.geometry(f"300x150+{x}+{y}")

        # Messaggio
        msg_label = ctk.CTkLabel(dialog, text=message, wraplength=250)
        msg_label.pack(pady=20)

        # Pulsante OK
        ok_btn = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
        ok_btn.pack(pady=10)

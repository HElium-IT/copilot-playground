"""
Plugin di esempio per l'editor di codice
"""

import customtkinter as ctk
import tkinter as tk
from src.ui.plugins.plugin_manager import PluginBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.configs.settings import Settings

class CodeEditorPlugin(PluginBase):
    def __init__(self):
        self.settings = None
        self.widget = None
    
    def get_name(self) -> str:
        return "Editor di Codice"
    
    def get_description(self) -> str:
        return "Un semplice editor di codice con sintassi highlighting di base"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def initialize(self, settings: 'Settings') -> bool:
        self.settings = settings
        return True
    
    def create_widget(self, parent):
        """Crea il widget dell'editor di codice"""
        if self.widget is not None:
            return self.widget
        
        # Frame principale
        main_frame = ctk.CTkFrame(parent)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📄 Editor di Codice",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=10, pady=10)
        
        # Dropdown per il linguaggio
        self.language_option = ctk.CTkOptionMenu(
            header_frame,
            values=["Python", "JavaScript", "HTML", "CSS", "JSON", "Markdown"],
            command=self.on_language_change
        )
        self.language_option.pack(side="right", padx=10, pady=10)
        
        # Toolbar
        toolbar_frame = ctk.CTkFrame(main_frame)
        toolbar_frame.pack(fill="x", padx=5, pady=(0, 5))
        
        # Pulsanti toolbar
        new_btn = ctk.CTkButton(
            toolbar_frame,
            text="Nuovo",
            width=60,
            command=self.new_file
        )
        new_btn.pack(side="left", padx=(10, 5), pady=5)
        
        open_btn = ctk.CTkButton(
            toolbar_frame,
            text="Apri",
            width=60,
            command=self.open_file
        )
        open_btn.pack(side="left", padx=5, pady=5)
        
        save_btn = ctk.CTkButton(
            toolbar_frame,
            text="Salva",
            width=60,
            command=self.save_file
        )
        save_btn.pack(side="left", padx=5, pady=5)
        
        # Editor di testo
        self.text_editor = ctk.CTkTextbox(
            main_frame,
            wrap="none",
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.text_editor.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        # Status bar
        self.status_frame = ctk.CTkFrame(main_frame)
        self.status_frame.pack(fill="x", padx=5, pady=(0, 5))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Pronto",
            font=ctk.CTkFont(size=10)
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        self.position_label = ctk.CTkLabel(
            self.status_frame,
            text="Riga: 1, Colonna: 1",
            font=ctk.CTkFont(size=10)
        )
        self.position_label.pack(side="right", padx=10, pady=5)
        
        # Bind eventi
        self.text_editor.bind("<KeyRelease>", self.on_text_change)
        self.text_editor.bind("<Button-1>", self.on_cursor_move)
        
        self.widget = main_frame
        return main_frame
    
    def new_file(self):
        """Crea un nuovo file"""
        self.text_editor.delete("1.0", "end")
        self.status_label.configure(text="Nuovo file")
    
    def open_file(self):
        """Apre un file"""
        try:
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                title="Apri file",
                filetypes=[
                    ("Tutti i file", "*.*"),
                    ("Python", "*.py"),
                    ("JavaScript", "*.js"),
                    ("HTML", "*.html"),
                    ("CSS", "*.css"),
                    ("JSON", "*.json"),
                    ("Markdown", "*.md")
                ]
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.text_editor.delete("1.0", "end")
                self.text_editor.insert("1.0", content)
                self.status_label.configure(text=f"Aperto: {filename}")
                
        except Exception as e:
            self.status_label.configure(text=f"Errore nell'apertura: {str(e)}")
    
    def save_file(self):
        """Salva il file"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                title="Salva file",
                defaultextension=".txt",
                filetypes=[
                    ("Tutti i file", "*.*"),
                    ("Python", "*.py"),
                    ("JavaScript", "*.js"),
                    ("HTML", "*.html"),
                    ("CSS", "*.css"),
                    ("JSON", "*.json"),
                    ("Markdown", "*.md"),
                    ("Testo", "*.txt")
                ]
            )
            
            if filename:
                content = self.text_editor.get("1.0", "end-1c")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.status_label.configure(text=f"Salvato: {filename}")
                
        except Exception as e:
            self.status_label.configure(text=f"Errore nel salvataggio: {str(e)}")
    
    def on_language_change(self, language: str):
        """Gestisce il cambio di linguaggio"""
        self.status_label.configure(text=f"Linguaggio: {language}")
        # Qui si potrebbe implementare syntax highlighting specifico
    
    def on_text_change(self, event=None):
        """Gestisce i cambiamenti nel testo"""
        self.update_cursor_position()
    
    def on_cursor_move(self, event=None):
        """Gestisce il movimento del cursore"""
        self.text_editor.after(10, self.update_cursor_position)
    
    def update_cursor_position(self):
        """Aggiorna la posizione del cursore"""
        try:
            cursor_pos = self.text_editor.index(tk.INSERT)
            line, column = cursor_pos.split('.')
            self.position_label.configure(text=f"Riga: {line}, Colonna: {int(column) + 1}")
        except:
            pass
    
    def cleanup(self):
        """Pulisce le risorse"""
        if self.widget:
            self.widget.destroy()
            self.widget = None

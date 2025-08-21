"""
Pannello note con supporto per multiple finestre
"""

import customtkinter as ctk
import tkinter as tk
from typing import Dict, List, TYPE_CHECKING
import uuid
import json
from pathlib import Path
import datetime
import tkinter.messagebox

if TYPE_CHECKING:
    from src.configs.settings import Settings

class NotesPanel(ctk.CTkFrame):
    def __init__(self, parent, settings: 'Settings'):
        super().__init__(parent)
        self.settings = settings
        self.notes: Dict[str, Dict] = {}
        self.active_note_id: str = None
        
        self.setup_ui()
        self.load_notes()
    
    def setup_ui(self):
        """Configura l'interfaccia del pannello note"""
        # Configura il layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header con controlli
        self.header = ctk.CTkFrame(self)
        self.header.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 0))
        self.header.grid_columnconfigure(1, weight=1)
        
        # Titolo
        self.title_label = ctk.CTkLabel(
            self.header,
            text="📝 Note",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Dropdown per selezionare la nota
        self.note_selector = ctk.CTkOptionMenu(
            self.header,
            values=["Nuova Nota"],
            command=self.on_note_selected
        )
        self.note_selector.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        # Pulsanti
        self.new_note_btn = ctk.CTkButton(
            self.header,
            text="➕",
            width=30,
            command=self.create_new_note
        )
        self.new_note_btn.grid(row=0, column=2, padx=2, pady=10)
        
        self.delete_note_btn = ctk.CTkButton(
            self.header,
            text="🗑️",
            width=30,
            command=self.delete_current_note
        )
        self.delete_note_btn.grid(row=0, column=3, padx=2, pady=10)
        
        self.save_btn = ctk.CTkButton(
            self.header,
            text="💾",
            width=30,
            command=self.save_current_note
        )
        self.save_btn.grid(row=0, column=4, padx=(2, 10), pady=10)
        
        # Area principale per le note
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Campo titolo
        self.title_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Titolo della nota..."
        )
        self.title_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        # Area di testo
        self.text_area = ctk.CTkTextbox(
            self.content_frame,
            wrap="word",
            font=ctk.CTkFont(size=12)
        )
        self.text_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        # Bind eventi per auto-save
        self.title_entry.bind("<KeyRelease>", self.on_content_changed)
        self.text_area.bind("<KeyRelease>", self.on_content_changed)
        
        # Timer per auto-save
        self.auto_save_timer = None
    
    def create_new_note(self):
        """Crea una nuova nota"""
        note_id = str(uuid.uuid4())
        note_title = f"Nota {len(self.notes) + 1}"
        
        note_data = {
            "id": note_id,
            "title": note_title,
            "content": "",
            "created_at": datetime.datetime.now().isoformat(),
            "modified_at": datetime.datetime.now().isoformat()
        }
        
        self.notes[note_id] = note_data
        self.update_note_selector()
        self.note_selector.set(note_title)
        self.load_note(note_id)
    
    def delete_current_note(self):
        """Elimina la nota corrente"""
        if not self.active_note_id:
            return
        
        # Conferma eliminazione
        result = tkinter.messagebox.askyesno(
            "Conferma eliminazione",
            "Sei sicuro di voler eliminare questa nota?"
        )
        
        if result:
            del self.notes[self.active_note_id]
            self.active_note_id = None
            self.update_note_selector()
            self.clear_content()
            self.save_notes()
    
    def save_current_note(self):
        """Salva la nota corrente"""
        if not self.active_note_id:
            return
        
        title = self.title_entry.get().strip()
        content = self.text_area.get("1.0", "end-1c")
        
        if not title:
            title = f"Nota {len(self.notes)}"
        
        self.notes[self.active_note_id].update({
            "title": title,
            "content": content,
            "modified_at": datetime.datetime.now().isoformat()
        })
        
        self.update_note_selector()
        self.save_notes()
    
    def on_note_selected(self, selection: str):
        """Gestisce la selezione di una nota"""
        if selection == "Nuova Nota":
            self.create_new_note()
            return
        
        # Trova la nota per titolo
        for note_id, note_data in self.notes.items():
            if note_data["title"] == selection:
                self.load_note(note_id)
                break
    
    def load_note(self, note_id: str):
        """Carica una nota nell'editor"""
        if note_id not in self.notes:
            return
        
        self.active_note_id = note_id
        note_data = self.notes[note_id]
        
        # Carica il contenuto
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, note_data["title"])
        
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", note_data["content"])
    
    def clear_content(self):
        """Pulisce il contenuto dell'editor"""
        self.title_entry.delete(0, "end")
        self.text_area.delete("1.0", "end")
    
    def update_note_selector(self):
        """Aggiorna il dropdown delle note"""
        note_titles = ["Nuova Nota"] + [note["title"] for note in self.notes.values()]
        self.note_selector.configure(values=note_titles)
    
    def on_content_changed(self, event=None):
        """Gestisce i cambiamenti nel contenuto per l'auto-save"""
        # Cancella il timer precedente
        if self.auto_save_timer:
            self.after_cancel(self.auto_save_timer)
        
        # Imposta un nuovo timer per il salvataggio automatico
        self.auto_save_timer = self.after(2000, self.auto_save)
    
    def auto_save(self):
        """Salvataggio automatico"""
        if self.active_note_id:
            self.save_current_note()
    
    def load_notes(self):
        """Carica le note dal file"""
        notes_file = Path.home() / ".studio_app" / "notes.json"
        
        if notes_file.exists():
            try:
                with open(notes_file, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
                self.update_note_selector()
                
                # Carica la prima nota se disponibile
                if self.notes:
                    first_note_id = list(self.notes.keys())[0]
                    self.load_note(first_note_id)
                    self.note_selector.set(self.notes[first_note_id]["title"])
                    
            except (json.JSONDecodeError, Exception) as e:
                print(f"Errore nel caricamento delle note: {e}")
    
    def save_notes(self):
        """Salva le note nel file"""
        notes_file = Path.home() / ".studio_app" / "notes.json"
        notes_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Errore nel salvataggio delle note: {e}")

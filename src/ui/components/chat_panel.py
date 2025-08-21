"""
Pannello chat per l'integrazione con GitHub Copilot
"""

import customtkinter as ctk
import tkinter as tk
from typing import TYPE_CHECKING, List, Dict
import asyncio
import threading
from src.services.copilot_service import CopilotService

if TYPE_CHECKING:
    from src.config.settings import Settings
    from src.ui.plugins.plugin_manager import PluginManager

class ChatPanel(ctk.CTkFrame):
    def __init__(self, parent, settings: 'Settings', plugin_manager: 'PluginManager'):
        super().__init__(parent)
        self.settings = settings
        self.plugin_manager = plugin_manager
        self.copilot_service = CopilotService(settings)
        
        self.messages: List[Dict[str, str]] = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura l'interfaccia del pannello chat"""
        # Configura il layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header del chat
        self.header = ctk.CTkFrame(self)
        self.header.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 0))
        self.header.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.header,
            text="💬 GitHub Copilot Chat",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Pulsante per pulire la chat
        self.clear_btn = ctk.CTkButton(
            self.header,
            text="🗑️",
            width=30,
            command=self.clear_chat
        )
        self.clear_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Area messaggi con scrollbar
        self.chat_frame = ctk.CTkFrame(self)
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame per i messaggi
        self.scrollable_frame = ctk.CTkScrollableFrame(self.chat_frame)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Frame per l'input
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=(0, 5))
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Input textbox
        self.input_textbox = ctk.CTkTextbox(
            self.input_frame,
            height=80,
            wrap="word"
        )
        self.input_textbox.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Pulsante invia
        self.send_btn = ctk.CTkButton(
            self.input_frame,
            text="Invia",
            width=80,
            command=self.send_message
        )
        self.send_btn.grid(row=0, column=1, padx=(0, 5), pady=5)
        
        # Bind eventi
        self.input_textbox.bind("<Control-Return>", lambda e: self.send_message())
        
        # Messaggio di benvenuto
        self.add_system_message("Benvenuto! Scrivi un messaggio per iniziare a chattare con GitHub Copilot.")
    
    def add_message(self, role: str, content: str):
        """Aggiunge un messaggio alla chat"""
        message_frame = ctk.CTkFrame(self.scrollable_frame)
        message_frame.grid(sticky="ew", padx=5, pady=2)
        message_frame.grid_columnconfigure(1, weight=1)
        
        # Icona del ruolo
        icon = "🤖" if role == "assistant" else "👤" if role == "user" else "🛠️"
        role_label = ctk.CTkLabel(
            message_frame,
            text=icon,
            font=ctk.CTkFont(size=16)
        )
        role_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nw")
        
        # Contenuto del messaggio
        content_label = ctk.CTkLabel(
            message_frame,
            text=content,
            font=ctk.CTkFont(size=12),
            wraplength=400,
            justify="left",
            anchor="w"
        )
        content_label.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        
        # Scroll automatico verso il basso
        self.after(100, self._scroll_to_bottom)
        
        # Salva il messaggio
        self.messages.append({"role": role, "content": content})
    
    def add_system_message(self, content: str):
        """Aggiunge un messaggio di sistema"""
        self.add_message("system", content)
    
    def send_message(self):
        """Invia un messaggio al chatbot"""
        content = self.input_textbox.get("1.0", "end-1c").strip()
        if not content:
            return
        
        # Pulisci l'input
        self.input_textbox.delete("1.0", "end")
        
        # Aggiungi il messaggio dell'utente
        self.add_message("user", content)
        
        # Disabilita il pulsante di invio
        self.send_btn.configure(state="disabled", text="...")
        
        # Invia la richiesta in un thread separato
        threading.Thread(
            target=self._send_message_async,
            args=(content,),
            daemon=True
        ).start()
    
    def _send_message_async(self, content: str):
        """Invia il messaggio in modo asincrono"""
        try:
            # Prepara i messaggi per l'API
            api_messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in self.messages
                if msg["role"] in ["user", "assistant"]
            ][-10:]  # Mantieni solo gli ultimi 10 messaggi
            
            # Chiamata all'API
            response = self.copilot_service.send_message(api_messages)
            
            # Aggiungi la risposta alla UI nel thread principale
            self.after(0, lambda: self._handle_response(response))
            
        except Exception as e:
            error_msg = f"Errore: {str(e)}"
            self.after(0, lambda: self._handle_error(error_msg))
    
    def _handle_response(self, response: str):
        """Gestisce la risposta dall'API"""
        self.add_message("assistant", response)
        self.send_btn.configure(state="normal", text="Invia")
    
    def _handle_error(self, error_msg: str):
        """Gestisce gli errori"""
        self.add_system_message(error_msg)
        self.send_btn.configure(state="normal", text="Invia")
    
    def _scroll_to_bottom(self):
        """Scrolla automaticamente verso il basso"""
        try:
            self.scrollable_frame._parent_canvas.yview_moveto(1.0)
        except:
            pass
    
    def clear_chat(self):
        """Pulisce la chat"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.messages.clear()
        self.add_system_message("Chat pulita. Scrivi un messaggio per ricominciare.")

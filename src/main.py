"""
Main entry point per l'applicazione Studio App
"""

import tkinter as tk
import customtkinter as ctk
from src.ui.main_window import MainWindow
from src.config.settings import Settings
import os
from dotenv import load_dotenv

def main():
    # Carica le variabili d'ambiente
    load_dotenv()
    
    # Configura il tema di customtkinter
    ctk.set_appearance_mode("dark")  # "light" o "dark"
    ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
    
    # Inizializza le impostazioni
    settings = Settings()
    
    # Crea e avvia l'applicazione principale
    app = MainWindow(settings)
    app.run()

if __name__ == "__main__":
    main()

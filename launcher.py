#!/usr/bin/env python3
"""
Launcher per Studio App con rilevamento automatico dell'ambiente
"""

import sys
import os

def check_display():
    """Controlla se è disponibile un display grafico"""
    return os.environ.get('DISPLAY') is not None or sys.platform == 'win32' or sys.platform == 'darwin'

def main():
    """Avvia l'applicazione nel modo appropriato"""
    # Aggiungi il percorso dell'app al Python path
    app_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, app_dir)
    
    if check_display():
        # Avvia l'interfaccia grafica
        print("🖥️ Avvio interfaccia grafica...")
        try:
            from src.main import main as gui_main
            gui_main()
        except Exception as e:
            print(f"❌ Errore nell'avvio dell'interfaccia grafica: {e}")
            print("🔧 Avvio test di sistema...")
            from test_app import main as test_main
            test_main()
    else:
        # Avvia in modalità test/headless
        print("🤖 Sistema headless rilevato, avvio test di sistema...")
        from test_app import main as test_main
        test_main()

if __name__ == "__main__":
    main()

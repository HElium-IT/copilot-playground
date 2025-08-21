#!/usr/bin/env python3
"""
Launcher per Studio App con rilevamento automatico dell'ambiente
"""

import sys
import os
import subprocess


def activate_venv():
    """Attiva l'ambiente virtuale se esiste"""
    venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")

    if os.path.exists(venv_path):
        if sys.platform == "win32":
            python_path = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            python_path = os.path.join(venv_path, "bin", "python")

        if os.path.exists(python_path) and sys.executable != python_path:
            print("🔧 Riavvio con ambiente virtuale...")
            # Riavvia lo script con l'interprete Python dell'ambiente virtuale
            subprocess.run([python_path] + sys.argv)
            sys.exit(0)
        elif os.path.exists(python_path):
            print("✅ Ambiente virtuale già attivo")
    else:
        print(
            "⚠️ Ambiente virtuale non trovato. Esegui install.bat/install.sh per crearlo."
        )

def check_display():
    """Controlla se è disponibile un display grafico"""
    return os.environ.get('DISPLAY') is not None or sys.platform == 'win32' or sys.platform == 'darwin'

def main():
    """Avvia l'applicazione nel modo appropriato"""
    # Attiva ambiente virtuale se necessario
    activate_venv()

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

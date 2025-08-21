#!/bin/bash

# Script di installazione per Studio App

echo "🚀 Installazione Studio App"
echo "=========================="

# Controlla Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato. Installa Python 3.8+ per continuare."
    exit 1
fi

echo "✅ Python trovato: $(python3 --version)"

# Crea ambiente virtuale se non esiste
if [ ! -d "venv" ]; then
    echo "🏗️ Creazione ambiente virtuale..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Errore nella creazione dell'ambiente virtuale"
        exit 1
    fi
    echo "✅ Ambiente virtuale creato"
else
    echo "✅ Ambiente virtuale esistente trovato"
fi

# Attiva ambiente virtuale
echo "🔧 Attivazione ambiente virtuale..."
source venv/bin/activate

# Installa dipendenze
echo "📦 Installazione dipendenze nell'ambiente virtuale..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dipendenze installate con successo"
else
    echo "❌ Errore nell'installazione delle dipendenze"
    exit 1
fi

# Esegui test
echo "🧪 Esecuzione test..."
python test_app.py

if [ $? -eq 0 ]; then
    echo "✅ Tutti i test sono passati"
else
    echo "❌ Alcuni test sono falliti"
    exit 1
fi

# Crea file .env se non esiste
if [ ! -f ".env" ]; then
    echo "📝 Creazione file .env..."
    cp .env.example .env
    echo "✅ File .env creato. Modifica il file per configurare le tue API keys."
fi

echo ""
echo "🎉 Installazione completata!"
echo ""
echo "📋 Prossimi passi:"
echo "1. Modifica il file .env per configurare le API keys"
echo "2. Attiva l'ambiente virtuale: source venv/bin/activate"
echo "3. Avvia l'app con: python launcher.py"
echo "4. Su sistemi con interfaccia grafica, si aprirà l'applicazione"
echo "5. Usa le impostazioni nell'app per configurare ulteriormente"
echo ""
echo "💡 Suggerimento: L'app può essere avviata anche con: python launcher.py"
echo "📚 Per maggiori informazioni, consulta il README.md"

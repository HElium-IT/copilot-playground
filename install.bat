@echo off
REM Script di installazione per Windows

echo 🚀 Installazione Studio App
echo ==========================

REM Controlla Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python non trovato. Installa Python 3.8+ per continuare.
    pause
    exit /b 1
)

echo ✅ Python trovato
python --version

REM Installa dipendenze
echo 📦 Installazione dipendenze...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Errore nell'installazione delle dipendenze
    pause
    exit /b 1
)

echo ✅ Dipendenze installate con successo

REM Esegui test
echo 🧪 Esecuzione test...
python test_app.py

if errorlevel 1 (
    echo ❌ Alcuni test sono falliti
    pause
    exit /b 1
)

echo ✅ Tutti i test sono passati

REM Crea file .env se non esiste
if not exist ".env" (
    echo 📝 Creazione file .env...
    copy .env.example .env
    echo ✅ File .env creato. Modifica il file per configurare le tue API keys.
)

echo.
echo 🎉 Installazione completata!
echo.
echo 📋 Prossimi passi:
echo 1. Modifica il file .env per configurare le API keys
echo 2. Avvia l'app con: python app.py
echo 3. Si aprirà l'applicazione con interfaccia grafica
echo 4. Usa le impostazioni nell'app per configurare ulteriormente
echo.
echo 📚 Per maggiori informazioni, consulta il README.md
pause

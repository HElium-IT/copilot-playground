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

REM Crea ambiente virtuale se non esiste
if not exist "venv" (
    echo 🏗️ Creazione ambiente virtuale...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Errore nella creazione dell'ambiente virtuale
        pause
        exit /b 1
    )
    echo ✅ Ambiente virtuale creato
) else (
    echo ✅ Ambiente virtuale esistente trovato
)

REM Attiva ambiente virtuale
echo 🔧 Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

REM Installa dipendenze
echo 📦 Installazione dipendenze nell'ambiente virtuale...
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
echo 2. Attiva l'ambiente virtuale: venv\Scripts\activate.bat
echo 3. Avvia l'app con: python launcher.py
echo 4. Si aprirà l'applicazione con interfaccia grafica
echo 5. Usa le impostazioni nell'app per configurare ulteriormente
echo.
echo 📚 Per maggiori informazioni, consulta il README.md
pause

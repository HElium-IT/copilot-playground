# Studio App - GitHub Copilot Integration

Un'applicazione di studio con layout customizzabile e integrazione GitHub Copilot.

## Caratteristiche

- **Chat integrata con GitHub Copilot**: Interfaccia chat per interagire con GitHub Copilot
- **Layout customizzabile**: Regola la dimensione dei pannelli secondo le tue preferenze
- **Sistema di note multiple**: Crea e gestisci multiple finestre di note
- **Architettura plugin**: Sistema modulare per aggiungere nuove funzionalità
- **Editor di codice integrato**: Editor con syntax highlighting di base
- **Interfaccia moderna**: Utilizzando CustomTkinter per un look moderno

## Struttura del Progetto

```
copilot-playground/
├── app.py                          # Entry point dell'applicazione
├── requirements.txt                # Dipendenze Python
├── src/
│   ├── main.py                    # Main entry point
│   ├── config/
│   │   └── settings.py            # Gestione configurazioni
│   ├── services/
│   │   └── copilot_service.py     # Servizio per GitHub Copilot API
│   └── ui/
│       ├── main_window.py         # Finestra principale
│       ├── components/
│       │   ├── toolbar.py         # Toolbar principale
│       │   ├── chat_panel.py      # Pannello chat
│       │   └── notes_panel.py     # Pannello note
│       ├── dialogs/
│       │   ├── settings_dialog.py # Dialog impostazioni
│       │   └── plugin_manager_dialog.py # Dialog gestione plugin
│       └── plugins/
│           ├── plugin_manager.py  # Gestore plugin
│           └── plugins/
│               └── code_editor.py # Plugin editor di codice
```

## Installazione Rapida

### Metodo 1: Script Automatico

**Linux/macOS:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:**
```cmd
install.bat
```

### Metodo 2: Manuale

1. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Testa l'installazione**:
   ```bash
   python test_app.py
   ```

3. **Configura l'API Key** (opzionale):
   ```bash
   cp .env.example .env
   # Modifica .env con le tue API keys
   ```

## Utilizzo

### Avvio Automatico
```bash
python launcher.py
```
Il launcher rileva automaticamente l'ambiente e avvia l'app appropriatamente.

### Avvio Manuale

**Interfaccia Grafica:**
```bash
python app.py
```

**Solo Test:**
```bash
python test_app.py
```

2. **Prima configurazione**:
   - Vai su "⚙️" nella toolbar per aprire le impostazioni
   - Configura la tua GitHub Copilot API Key
   - Seleziona il tema preferito (dark/light)

3. **Utilizzo della chat**:
   - Scrivi messaggi nel pannello chat a sinistra
   - Premi "Invia" o Ctrl+Enter per inviare
   - Le risposte appariranno nel pannello chat

4. **Gestione note**:
   - Usa il pannello note a destra per creare note multiple
   - Le note vengono salvate automaticamente
   - Usa il dropdown per passare tra le note

5. **Plugin**:
   - Clicca su "🔧 Plugin" per gestire i plugin
   - Carica/scarica plugin secondo necessità
   - I plugin aggiungono nuove funzionalità all'app

## Personalizzazione

### Layout
- Usa lo slider nella toolbar per regolare la larghezza del pannello chat
- Attiva/disattiva il pannello note dal pulsante "📝 Note"

### Plugin Personalizzati
Puoi creare plugin personalizzati creando file nella directory `src/ui/plugins/plugins/`:

```python
from src.ui.plugins.plugin_manager import PluginBase

class MyPlugin(PluginBase):
    def get_name(self) -> str:
        return "My Custom Plugin"
    
    def get_description(self) -> str:
        return "Description of my plugin"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def initialize(self, settings) -> bool:
        # Inizializzazione del plugin
        return True
    
    def create_widget(self, parent):
        # Crea l'interfaccia del plugin
        pass
```

## Configurazione GitHub Copilot

> **Nota**: Attualmente GitHub Copilot non ha un'API pubblica ufficiale per chat. L'app include:
> - Un sistema di risposta mock per testing
> - Supporto per OpenAI API come fallback
> - Struttura pronta per l'integrazione futura con l'API ufficiale

Per utilizzare OpenAI come fallback:
1. Ottieni un'API key da OpenAI
2. Imposta la variabile d'ambiente: `OPENAI_API_KEY=your_openai_key`

## Sviluppo

### Aggiungere Nuove Funzionalità

1. **Nuovi pannelli**: Crea componenti in `src/ui/components/`
2. **Nuovi servizi**: Aggiungi servizi in `src/services/`
3. **Nuovi plugin**: Crea plugin in `src/ui/plugins/plugins/`
4. **Nuove dialog**: Aggiungi dialog in `src/ui/dialogs/`

### Testing

```bash
# Avvia l'app in modalità debug
python app.py
```

## Requisiti di Sistema

- Python 3.8+
- Windows, macOS, o Linux
- Connessione internet per l'API

## Dipendenze Principali

- `customtkinter`: UI moderna
- `requests`: Chiamate API
- `python-dotenv`: Gestione variabili d'ambiente

## Roadmap

- [ ] Syntax highlighting avanzato nell'editor
- [ ] Supporto per più modelli AI
- [ ] Sistema di temi personalizzabili
- [ ] Export/import configurazioni
- [ ] Supporto per workspace multipli
- [ ] Integrazione con Git
- [ ] Sistema di backup automatico note

## Contribuire

1. Fork il progetto
2. Crea un branch per la tua feature
3. Commit le modifiche
4. Push al branch
5. Apri una Pull Request

## Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file LICENSE per i dettagli.

## Supporto

Per problemi o domande:
1. Controlla le impostazioni dell'API key
2. Verifica la connessione internet
3. Consulta i log nella console per errori
4. Apri un issue su GitHub

---

**Buono studio! 📚🚀**
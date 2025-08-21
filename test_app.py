#!/usr/bin/env python3
"""
Script di test per verificare la struttura dell'applicazione
"""

import sys
import os

# Aggiungi il percorso dell'app al Python path
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

def test_imports():
    """Testa che tutti i moduli possano essere importati correttamente"""
    print("🧪 Testando gli import...")
    
    try:
        from src.configs.settings import Settings
        print("✅ Settings importato correttamente")
    except Exception as e:
        print(f"❌ Errore nell'import di Settings: {e}")
        return False
    
    try:
        from src.services.copilot_service import CopilotService
        print("✅ CopilotService importato correttamente")
    except Exception as e:
        print(f"❌ Errore nell'import di CopilotService: {e}")
        return False
    
    try:
        from src.ui.plugins.plugin_manager import PluginManager, PluginBase
        print("✅ PluginManager importato correttamente")
    except Exception as e:
        print(f"❌ Errore nell'import di PluginManager: {e}")
        return False
    
    return True

def test_settings():
    """Testa la configurazione"""
    print("\n⚙️ Testando le impostazioni...")
    
    try:
        from src.configs.settings import Settings
        settings = Settings()
        
        # Testa get/set
        settings.set("test_key", "test_value")
        value = settings.get("test_key")
        
        if value == "test_value":
            print("✅ Sistema di configurazione funzionante")
            return True
        else:
            print("❌ Errore nel sistema di configurazione")
            return False
            
    except Exception as e:
        print(f"❌ Errore nel test delle impostazioni: {e}")
        return False

def test_plugin_system():
    """Testa il sistema dei plugin"""
    print("\n🔧 Testando il sistema dei plugin...")
    
    try:
        from src.configs.settings import Settings
        from src.ui.plugins.plugin_manager import PluginManager
        
        settings = Settings()
        plugin_manager = PluginManager(settings)
        
        # Testa discovery dei plugin
        available_plugins = plugin_manager.get_available_plugins()
        print(f"✅ Plugin scoperti: {available_plugins}")
        
        # Testa caricamento del plugin code_editor se disponibile
        if "code_editor" in available_plugins:
            success = plugin_manager.load_plugin("code_editor")
            if success:
                print("✅ Plugin code_editor caricato con successo")
            else:
                print("⚠️ Errore nel caricamento del plugin code_editor")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test del sistema plugin: {e}")
        return False

def test_copilot_service():
    """Testa il servizio Copilot"""
    print("\n🤖 Testando il servizio Copilot...")
    
    try:
        from src.configs.settings import Settings
        from src.services.copilot_service import CopilotService
        
        settings = Settings()
        copilot_service = CopilotService(settings)
        
        # Testa una chiamata mock
        test_messages = [{"role": "user", "content": "Hello, this is a test"}]
        response = copilot_service.send_message(test_messages)
        
        if response and len(response) > 0:
            print(f"✅ Servizio Copilot funzionante. Risposta: {response[:50]}...")
            return True
        else:
            print("❌ Errore nel servizio Copilot")
            return False
            
    except Exception as e:
        print(f"❌ Errore nel test del servizio Copilot: {e}")
        return False

def main():
    """Esegue tutti i test"""
    print("🚀 Studio App - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import dei moduli", test_imports),
        ("Sistema di configurazione", test_settings),
        ("Sistema dei plugin", test_plugin_system),
        ("Servizio Copilot", test_copilot_service)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Errore critico in '{test_name}': {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Risultati: {passed}/{total} test passati")
    
    if passed == total:
        print("🎉 Tutti i test sono passati! L'applicazione è pronta.")
        print("\n📝 Note:")
        print("- L'app è configurata correttamente")
        print("- Per avviare l'interfaccia grafica, usa: python app.py")
        print("- Su sistemi senza display, l'app può funzionare solo in modalità headless")
        print("- Configura l'API key nelle impostazioni per utilizzare le funzionalità complete")
    else:
        print("⚠️ Alcuni test sono falliti. Controlla i messaggi di errore sopra.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

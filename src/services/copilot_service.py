"""
Servizio per l'integrazione con GitHub Copilot API
"""

import requests
import json
from typing import List, Dict, Any, TYPE_CHECKING
import os

if TYPE_CHECKING:
    from src.config.settings import Settings

class CopilotService:
    def __init__(self, settings: 'Settings'):
        self.settings = settings
        self.api_key = settings.get_github_api_key()
        
        # Endpoint per GitHub Copilot (questo è un esempio, l'endpoint reale potrebbe essere diverso)
        # Nota: Al momento GitHub Copilot non ha un'API pubblica ufficiale per chat
        # Questo è un esempio di come potrebbe funzionare
        self.base_url = "https://api.github.com/copilot"
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def send_message(self, messages: List[Dict[str, str]]) -> str:
        """
        Invia un messaggio al servizio di chat
        
        Args:
            messages: Lista di messaggi nel formato [{"role": "user", "content": "..."}]
        
        Returns:
            Risposta del modello
        """
        if not self.api_key:
            return "⚠️ Errore: API key di GitHub Copilot non configurata. Vai nelle impostazioni per configurarla."
        
        try:
            # Per ora, dato che GitHub Copilot non ha un'API pubblica per chat,
            # usiamo OpenAI come fallback (se disponibile)
            return self._send_to_openai_fallback(messages)
            
        except Exception as e:
            return f"❌ Errore nella comunicazione con l'API: {str(e)}"
    
    def _send_to_openai_fallback(self, messages: List[Dict[str, str]]) -> str:
        """
        Fallback usando OpenAI API (se configurata)
        """
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            return self._mock_response(messages)
        
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {openai_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            return self._mock_response(messages)
    
    def _mock_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Risposta mock per testing senza API reale
        """
        last_message = messages[-1]["content"] if messages else ""
        
        mock_responses = [
            f"🤖 Ho ricevuto il tuo messaggio: '{last_message[:50]}...' \n\nQuesto è un esempio di risposta mock. Per utilizzare l'API reale, configura la tua API key nelle impostazioni.",
            f"💡 Interessante domanda! Stai chiedendo riguardo: '{last_message[:30]}...'\n\nPurtroppo al momento sto usando risposte simulate. Configura l'API per avere risposte reali.",
            f"🎯 Capisco che vuoi sapere di: '{last_message[:40]}...'\n\nQuando configurerai l'API key, potrai avere risposte più dettagliate e precise.",
            f"📚 La tua richiesta '{last_message[:35]}...' è molto interessante!\n\nRicorda di impostare l'API key per ottenere risposte complete."
        ]
        
        # Scegli una risposta in base alla lunghezza del messaggio
        response_index = len(last_message) % len(mock_responses)
        return mock_responses[response_index]
    
    def validate_api_key(self) -> bool:
        """
        Valida l'API key
        """
        if not self.api_key:
            return False
        
        try:
            # Test API call per validare la chiave
            # Per ora restituiamo True se la chiave è presente
            return len(self.api_key) > 10
        except:
            return False
    
    def get_models(self) -> List[str]:
        """
        Ottiene la lista dei modelli disponibili
        """
        return [
            "github-copilot-chat",
            "gpt-3.5-turbo",
            "gpt-4"
        ]

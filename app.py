#!/usr/bin/env python3
"""
Studio App - Un'applicazione di studio con layout customizzabile e integrazione GitHub Copilot
"""

__version__ = "0.1.0"
__author__ = "Your Name"

import sys
import os

# Aggiungi il percorso dell'app al Python path
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

from src.main import main

if __name__ == "__main__":
    main()

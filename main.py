"""Startpunkt: Yōkai no Michi – Hyakki Yagyō"""
import sys

if sys.platform == 'win32':
    # Ohne DPI-Bewusstsein skaliert Windows (125 %/150 %) das Fenster selbst –
    # dann ist das Vollbild zu groß, unscharf oder abgeschnitten.
    try:
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

from yokai.app import main

if __name__ == '__main__':
    main()

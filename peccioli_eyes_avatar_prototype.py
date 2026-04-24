import streamlit as st
import json
import hashlib
from pathlib import Path
from datetime import datetime
import random

st.set_page_config(
    page_title="Peccioli Eyes Avatar",
    page_icon="eye",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BRAND_BLUE = "#130089"
BRAND_YELLOW = "#FFDE59"
BRAND_BLUE_DARK = "#0a0052"
BRAND_BLUE_LIGHT = "#f0eeff"
BRAND_YELLOW_LIGHT = "#fffbe5"

DB_FILE = Path(__file__).parent / "peccioli_avatars.json"


def load_db():
    if DB_FILE.exists():
        try:
            return json.loads(DB_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_db(db):
    DB_FILE.write_text(json.dumps(db, indent=2, ensure_ascii=False), encoding="utf-8")


SHAPES = [
    {"id": "round", "label": "Tondo"},
    {"id": "almond", "label": "Mandorla"},
    {"id": "narrow", "label": "Stretto"},
    {"id": "wide", "label": "Largo"},
]

COLORS = [
    ("Giallo brand", "#FFDE59"),
    ("Blu brand", "#130089"),
    ("Verde bosco", "#2ea36a"),
    ("Terracotta", "#c84a1e"),
    ("Viola", "#7a3fb8"),
    ("Petrolio", "#0a5a7a"),
    ("Ambra", "#b8860b"),
    ("Grigio", "#636363"),
    ("Azzurro", "#4db3e8"),
    ("Rosa antico", "#c26a8a"),
    ("Nero", "#1a1a1a"),
    ("Bianco", "#ffffff"),
]

# COLLINE e LUNA rimossi dalla lista
SYMBOLS = [
    {"id": "campanile_peccioli", "label": "Campanile di Peccioli", "category": "peccioli"},
    {"id": "cipresso", "label": "Cipresso toscano", "category": "peccioli"},
    {"id": "uliva", "label": "Olivo", "category": "peccioli"},
    {"id": "gigante", "label": "Gigante di Peccioli", "category": "peccioli"},
    {"id": "mammut", "label": "Mammut", "category": "peccioli"},

    {"id": "trumpet", "label": "Tromba jazz", "category": "nola"},
    {"id": "mask", "label": "Maschera Mardi Gras", "category": "nola"},
    {"id": "fleur", "label": "Giglio di NOLA", "category": "nola"},
    {"id": "riverboat", "label": "Battello Mississippi", "category": "nola"},
    {"id": "balcony", "label": "Ferro battuto", "category": "nola"},

    {"id": "note", "label": "Nota musicale", "category": "temi"},
    {"id": "wave", "label": "Onda (resilienza)", "category": "temi"},
    {"id": "people", "label": "Comunita", "category": "temi"},
    {"id": "book", "label": "Libro (identita)", "category": "temi"},

    {"id": "star", "label": "Stella", "category": "astratti"},
    {"id": "heart", "label": "Cuore", "category": "astratti"},
    {"id": "eye_inside", "label": "Occhio nell'occhio", "category": "astratti"},
    {"id": "lightning", "label": "Fulmine", "category": "astratti"},
]

SYMBOL_CATEGORIES = [
    ("peccioli", "Peccioli"),
    ("nola", "New Orleans"),
    ("temi", "Temi del viaggio"),
    ("astratti", "Astratti"),
]

LASHES = [
    {"id": "classic", "label": "Classiche"},
    {"id": "long", "label": "Lunghe"},
    {"id": "short", "label": "Corte"},
    {"id": "thick", "label": "Folte"},
    {"id": "none", "label": "Assenti"},
]

BACKGROUNDS = [
    {"id": "blue-solid", "label": "Blu brand", "color": BRAND_BLUE},
    {"id": "yellow-solid", "label": "Giallo brand", "color": BRAND_YELLOW},
    {"id": "white-solid", "label": "Avorio", "color": "#fafafa"},
    {"id": "nola_jazz", "label": "Jazz notturno", "color": "#2a0a3a"},
    {"id": "peccioli_hills", "label": "Colline Peccioli", "color": "#2ea36a"},
    {"id": "ghizzano", "label": "Ghizzano", "color": "#c8226a"},
    {"id": "muro_occhi", "label": "Muro degli Occhi", "color": "#8a7a6a"},
    {"id": "macca", "label": "MACCA al tramonto", "color": "#d88a7a"},
    {"id": "peccioli_tower", "label": "Campanile di Peccioli", "color": "#b0a89c"},
    {"id": "french_quarter", "label": "French Quarter", "color": "#a85a3a"},
    {"id": "sunset_mississippi", "label": "Tramonto Mississippi", "color": "#ff9a8b"},
    {"id": "mardigras", "label": "Mardi Gras", "color": "#4ba5c5"},
]

DEFAULT_AVATAR = {
    "shape": "almond",
    "iris": "#FFDE59",
    "symbol": "trumpet",
    "symbol_color": "#130089",
    "lashes": "classic",
    "lashes_color": "#1a1a1a",
    "bg": "blue-solid",
    "border_color": "#ffffff",
}


def eye_path(shape):
    if shape == "round":
        return "M 40 100 A 60 60 0 1 1 160 100 A 60 60 0 1 1 40 100 Z"
    if shape == "almond":
        return "M 30 100 Q 100 30 170 100 Q 100 170 30 100 Z"
    if shape == "narrow":
        return "M 25 100 Q 100 65 175 100 Q 100 135 25 100 Z"
    if shape == "wide":
        return "M 25 100 Q 100 20 175 100 Q 100 180 25 100 Z"
    return ""


def render_symbol(sym_id, color):
    """Simboli dentro pupilla bianca. Disegnati a raggio ~10-12."""

    # PECCIOLI ==================================================
    if sym_id == "campanile_peccioli":
        # Campanile squadrato a 2 ordini con fascia archetti e cuspide piramidale
        parts = []
        parts.append('<g transform="translate(100 100)">')
        # Corpo principale
        parts.append('<rect x="-5" y="-3" width="10" height="14" fill="' + color + '"/>')
        # Fascia alla base del secondo ordine
        parts.append('<rect x="-5.5" y="-4" width="11" height="1.2" fill="' + color + '"/>')
        # Secondo ordine (piu' stretto)
        parts.append('<rect x="-4.5" y="-9" width="9" height="5.5" fill="' + color + '"/>')
        # Finestra ad arco nel secondo ordine
        parts.append('<path d="M -1.2 -4.5 L -1.2 -7 Q 0 -8.5 1.2 -7 L 1.2 -4.5 Z" fill="white"/>')
        # Fascia di archetti decorativi
        parts.append('<rect x="-5.5" y="-10" width="11" height="1" fill="' + color + '"/>')
        parts.append('<path d="M -5 -10 Q -4 -11.5 -3 -10 Q -2 -11.5 -1 -10 Q 0 -11.5 1 -10 Q 2 -11.5 3 -10 Q 4 -11.5 5 -10" fill="none" stroke="' + color + '" stroke-width="0.5"/>')
        # Cornicione superiore
        parts.append('<rect x="-5.8" y="-11" width="11.6" height="0.8" fill="' + color + '"/>')
        # Cuspide piramidale
        parts.append('<polygon points="-5.5,-11 5.5,-11 0,-18" fill="' + color + '"/>')
        # Cuspide finale
        parts.append('<circle cx="0" cy="-18.3" r="0.5" fill="' + color + '"/>')
        parts.append('<line x1="0" y1="-18.3" x2="0" y2="-19.5" stroke="' + color + '" stroke-width="0.3"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "cipresso":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M 0 -9 Q 3 -6 3 -3 Q 4 0 3 3 Q 4 5 2 7 L -2 7 Q -4 5 -3 3 Q -4 0 -3 -3 Q -3 -6 0 -9 Z" fill="' + color + '"/>')
        parts.append('<rect x="-0.8" y="7" width="1.6" height="3" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "uliva":
        # Ramoscello verticale con foglie lanceolate alternate e olive tonde
        parts = []
        parts.append('<g transform="translate(100 100)">')
        # Tronco centrale
        parts.append('<path d="M 0 10 Q 0.5 5 -0.3 0 Q 0.5 -5 0 -10" fill="none" stroke="' + color + '" stroke-width="1.2" stroke-linecap="round"/>')
        # 5 foglie lanceolate alternate
        parts.append('<ellipse cx="-3.5" cy="-6.5" rx="3.2" ry="1.3" fill="' + color + '" transform="rotate(-40 -3.5 -6.5)"/>')
        parts.append('<ellipse cx="3.5" cy="-3.5" rx="3.2" ry="1.3" fill="' + color + '" transform="rotate(40 3.5 -3.5)"/>')
        parts.append('<ellipse cx="-4" cy="0" rx="3.4" ry="1.4" fill="' + color + '" transform="rotate(-30 -4 0)"/>')
        parts.append('<ellipse cx="4" cy="3" rx="3.2" ry="1.3" fill="' + color + '" transform="rotate(30 4 3)"/>')
        parts.append('<ellipse cx="-3.5" cy="6.5" rx="3" ry="1.2" fill="' + color + '" transform="rotate(-30 -3.5 6.5)"/>')
        # 3 olive tonde
        parts.append('<circle cx="2.2" cy="-7" r="1.5" fill="' + color + '"/>')
        parts.append('<circle cx="-2" cy="-2" r="1.3" fill="' + color + '"/>')
        parts.append('<circle cx="2" cy="7" r="1.4" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "gigante":
        # Gigante di Peccioli: figura umana accovacciata che emerge dalla terra, con braccia staccate dal torso
        parts = []
        parts.append('<g transform="translate(100 100)">')
        # TESTA calva ovale
        parts.append('<ellipse cx="0" cy="-9.5" rx="2.2" ry="2.4" fill="' + color + '"/>')
        # COLLO
        parts.append('<rect x="-0.75" y="-7.5" width="1.5" height="1.3" fill="' + color + '"/>')
        # SPALLE (deltoidi)
        parts.append('<ellipse cx="-3.4" cy="-5.6" rx="1.7" ry="1.5" fill="' + color + '"/>')
        parts.append('<ellipse cx="3.4" cy="-5.6" rx="1.7" ry="1.5" fill="' + color + '"/>')
        # TORSO centrale (stretto, ben staccato dalle braccia)
        parts.append('<path d="M -2.9 -5 Q -3.9 -1.2 -3.9 2 Q -3.9 5.4 -2.4 7.8 L 2.4 7.8 Q 3.9 5.4 3.9 2 Q 3.9 -1.2 2.9 -5 L 1.9 -5.7 L -1.9 -5.7 Z" fill="' + color + '"/>')
        # BRACCIO SINISTRO che arriva a terra (ben distante dal torso)
        parts.append('<path d="M -4.8 -4.5 Q -7.2 -1 -8.6 2.9 Q -9.6 5.7 -10.1 7.8 L -6.7 7.8 Q -6.2 5.7 -5.7 3.4 Q -5.2 1 -4.8 -1.4 Q -4.5 -3.1 -4.5 -4.1 Z" fill="' + color + '"/>')
        # Mano sinistra a terra
        parts.append('<ellipse cx="-8.9" cy="7.8" rx="1.2" ry="0.6" fill="' + color + '"/>')
        # BRACCIO DESTRO che arriva a terra
        parts.append('<path d="M 4.8 -4.5 Q 7.2 -1 8.6 2.9 Q 9.6 5.7 10.1 7.8 L 6.7 7.8 Q 6.2 5.7 5.7 3.4 Q 5.2 1 4.8 -1.4 Q 4.5 -3.1 4.5 -4.1 Z" fill="' + color + '"/>')
        # Mano destra a terra
        parts.append('<ellipse cx="8.9" cy="7.8" rx="1.2" ry="0.6" fill="' + color + '"/>')
        # Terra
        parts.append('<path d="M -12 8 Q -8 7.5 -4 8 Q 0 8.5 4 8 Q 8 7.5 12 8 L 12 9.5 L -12 9.5 Z" fill="' + color + '"/>')
        # Pettorali (opacità ridotta)
        parts.append('<ellipse cx="-1.5" cy="-3.5" rx="1.1" ry="1.5" fill="' + color + '" opacity="0.32"/>')
        parts.append('<ellipse cx="1.5" cy="-3.5" rx="1.1" ry="1.5" fill="' + color + '" opacity="0.32"/>')
        # Linea mediana addominali
        parts.append('<line x1="0" y1="-4.5" x2="0" y2="5.5" stroke="' + color + '" stroke-width="0.22" opacity="0.4"/>')
        parts.append('<line x1="-1" y1="-0.8" x2="1" y2="-0.8" stroke="' + color + '" stroke-width="0.22" opacity="0.4"/>')
        parts.append('<line x1="-1" y1="0.9" x2="1" y2="0.9" stroke="' + color + '" stroke-width="0.22" opacity="0.4"/>')
        parts.append('<line x1="-1" y1="2.9" x2="1" y2="2.9" stroke="' + color + '" stroke-width="0.22" opacity="0.4"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "mammut":
        # Mammut di Peccioli: elefante preistorico con zanne e proboscide
        parts = []
        parts.append('<g transform="translate(100 100)">')
        # Corpo massiccio accovacciato
        parts.append('<ellipse cx="-1.2" cy="3.6" rx="6.7" ry="4.3" fill="' + color + '"/>')
        # Gambe anteriore e posteriore
        parts.append('<rect x="-6.7" y="4.8" width="2.6" height="4.3" rx="0.5" fill="' + color + '"/>')
        parts.append('<rect x="3.1" y="4.8" width="2.6" height="4.3" rx="0.5" fill="' + color + '"/>')
        # Testa grande
        parts.append('<ellipse cx="2.9" cy="-1.9" rx="3.6" ry="3.4" fill="' + color + '"/>')
        # Orecchio floscio
        parts.append('<ellipse cx="0.5" cy="-1.2" rx="1.7" ry="1.9" transform="rotate(-15 0.5 -1.2)" fill="' + color + '"/>')
        # Proboscide alzata e curva
        parts.append('<path d="M 5.3 -2.9 Q 6.7 -4.8 7.2 -6.7 Q 7.7 -8.6 6.2 -9.1 Q 5.3 -8.6 5.5 -7.2 Q 5.5 -5.3 4.8 -3.6 Z" fill="' + color + '"/>')
        # Zanna anteriore grande curva
        parts.append('<path d="M 6 -1 Q 9.1 -2 10.1 -5.3 Q 10.3 -6.7 9.6 -6.7 Q 8.6 -5.3 8.1 -3.4 Q 7.2 -2 6 -1 Z" fill="' + color + '"/>')
        # Seconda zanna dietro
        parts.append('<path d="M 4.3 -0.05 Q 6.7 -0.5 7.2 -2.4 Q 7.2 -3.4 6.7 -3.4 Q 5.8 -2.4 4.3 -0.05 Z" fill="' + color + '"/>')
        # Coda
        parts.append('<path d="M -7.7 2.4 Q -9.6 3.1 -10.1 5.5" fill="none" stroke="' + color + '" stroke-width="0.7" stroke-linecap="round"/>')
        parts.append('</g>')
        return "".join(parts)

    # NEW ORLEANS ==================================================
    if sym_id == "trumpet":
        # Tromba originale del prototipo (quella che ti piaceva)
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<rect x="-11" y="-1.5" width="2.5" height="3" fill="' + color + '"/>')
        parts.append('<rect x="-8.5" y="-1.5" width="11" height="3" fill="' + color + '"/>')
        parts.append('<rect x="-4" y="-3.5" width="1.5" height="2" fill="' + color + '"/>')
        parts.append('<rect x="-1.5" y="-3.5" width="1.5" height="2" fill="' + color + '"/>')
        parts.append('<rect x="1" y="-3.5" width="1.5" height="2" fill="' + color + '"/>')
        parts.append('<path d="M 2.5 -1.5 L 10 -5 L 10 5 L 2.5 1.5 Z" fill="' + color + '"/>')
        parts.append('<ellipse cx="10" cy="0" rx="1" ry="5" fill="white"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "mask":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M -8 -5 Q -11 -10 -9 -12 Q -7 -10 -7 -6" fill="' + color + '" opacity="0.7"/>')
        parts.append('<path d="M 8 -5 Q 11 -10 9 -12 Q 7 -10 7 -6" fill="' + color + '" opacity="0.7"/>')
        parts.append('<path d="M -10 -2 Q -10 -6 -6 -6 L -1 -5 Q 0 -3 1 -5 L 6 -6 Q 10 -6 10 -2 Q 10 4 6 5 Q 2 5 0 2 Q -2 5 -6 5 Q -10 4 -10 -2 Z" fill="' + color + '"/>')
        parts.append('<ellipse cx="-5" cy="-1" rx="2.5" ry="2" fill="white"/>')
        parts.append('<ellipse cx="5" cy="-1" rx="2.5" ry="2" fill="white"/>')
        parts.append('<circle cx="0" cy="3" r="0.8" fill="white"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "fleur":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M 0 -10 Q -2.5 -5 -1.5 -1 Q -2.5 3 0 8 Q 2.5 3 1.5 -1 Q 2.5 -5 0 -10 Z" fill="' + color + '"/>')
        parts.append('<path d="M -1.5 -2 Q -9 -3 -9 3 Q -6 6 -2 3 Q -1 1 -1.5 -2 Z" fill="' + color + '"/>')
        parts.append('<path d="M 1.5 -2 Q 9 -3 9 3 Q 6 6 2 3 Q 1 1 1.5 -2 Z" fill="' + color + '"/>')
        parts.append('<rect x="-7" y="1" width="14" height="2.5" fill="' + color + '"/>')
        parts.append('<circle cx="0" cy="-10" r="1.3" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "riverboat":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M -11 9 Q -8 7 -5 9 Q -2 7 1 9 Q 4 7 7 9 Q 10 7 11 9" fill="none" stroke="' + color + '" stroke-width="1" opacity="0.5"/>')
        parts.append('<path d="M -11 5 L 11 5 L 9 8 L -9 8 Z" fill="' + color + '"/>')
        parts.append('<rect x="-9" y="0" width="18" height="5" fill="' + color + '"/>')
        parts.append('<rect x="-6" y="-3" width="12" height="3" fill="' + color + '"/>')
        parts.append('<rect x="-3.5" y="-9" width="2" height="6" fill="' + color + '"/>')
        parts.append('<rect x="1.5" y="-9" width="2" height="6" fill="' + color + '"/>')
        parts.append('<circle cx="-9" cy="3" r="2.5" fill="none" stroke="' + color + '" stroke-width="0.8"/>')
        parts.append('<line x1="-9" y1="0.5" x2="-9" y2="5.5" stroke="' + color + '" stroke-width="0.6"/>')
        parts.append('<line x1="-11.5" y1="3" x2="-6.5" y2="3" stroke="' + color + '" stroke-width="0.6"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "balcony":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<rect x="-10" y="-5" width="20" height="1.5" fill="' + color + '"/>')
        parts.append('<rect x="-10" y="5" width="20" height="1.5" fill="' + color + '"/>')
        parts.append('<circle cx="-6" cy="0" r="2.5" fill="none" stroke="' + color + '" stroke-width="1"/>')
        parts.append('<circle cx="0" cy="0" r="2.5" fill="none" stroke="' + color + '" stroke-width="1"/>')
        parts.append('<circle cx="6" cy="0" r="2.5" fill="none" stroke="' + color + '" stroke-width="1"/>')
        parts.append('<line x1="-9" y1="-3.5" x2="-9" y2="5" stroke="' + color + '" stroke-width="1"/>')
        parts.append('<line x1="-3" y1="-3.5" x2="-3" y2="5" stroke="' + color + '" stroke-width="1"/>')
        parts.append('<line x1="3" y1="-3.5" x2="3" y2="5" stroke="' + color + '" stroke-width="1"/>')
        parts.append('<line x1="9" y1="-3.5" x2="9" y2="5" stroke="' + color + '" stroke-width="1"/>')
        parts.append('</g>')
        return "".join(parts)

    # TEMI =====================================================
    if sym_id == "note":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<ellipse cx="-5" cy="6" rx="3" ry="2.3" fill="' + color + '" transform="rotate(-20 -5 6)"/>')
        parts.append('<ellipse cx="4" cy="7" rx="3" ry="2.3" fill="' + color + '" transform="rotate(-20 4 7)"/>')
        parts.append('<rect x="-3" y="-8" width="1.5" height="14" fill="' + color + '"/>')
        parts.append('<rect x="6" y="-7" width="1.5" height="14" fill="' + color + '"/>')
        parts.append('<path d="M -3 -8 L 7.5 -7 L 7.5 -4.5 L -3 -5.5 Z" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "wave":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M -10 -4 Q -5 -8 0 -4 Q 5 0 10 -4" fill="none" stroke="' + color + '" stroke-width="1.8" stroke-linecap="round"/>')
        parts.append('<path d="M -10 1 Q -5 -3 0 1 Q 5 5 10 1" fill="none" stroke="' + color + '" stroke-width="1.8" stroke-linecap="round"/>')
        parts.append('<path d="M -10 6 Q -5 2 0 6 Q 5 10 10 6" fill="none" stroke="' + color + '" stroke-width="1.8" stroke-linecap="round"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "people":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<circle cx="-6.5" cy="-4" r="2" fill="' + color + '"/>')
        parts.append('<path d="M -9 0 Q -6.5 -2 -4 0 L -3.5 6 L -9.5 6 Z" fill="' + color + '"/>')
        parts.append('<circle cx="0" cy="-5" r="2.3" fill="' + color + '"/>')
        parts.append('<path d="M -3 -1 Q 0 -3 3 -1 L 3.5 7 L -3.5 7 Z" fill="' + color + '"/>')
        parts.append('<circle cx="6.5" cy="-4" r="2" fill="' + color + '"/>')
        parts.append('<path d="M 4 0 Q 6.5 -2 9 0 L 9.5 6 L 3.5 6 Z" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "book":
        # Libro aperto visto frontalmente - rettangoli dritti
        parts = []
        parts.append('<g transform="translate(100 100)">')
        # Pagina sinistra
        parts.append('<rect x="-11" y="-8" width="10.5" height="16" fill="' + color + '"/>')
        # Pagina destra
        parts.append('<rect x="0.5" y="-8" width="10.5" height="16" fill="' + color + '"/>')
        # Rilegatura centrale (piu' scura)
        parts.append('<rect x="-0.8" y="-8" width="1.6" height="16" fill="' + color + '" opacity="0.5"/>')
        # Linee di testo pagina sinistra
        parts.append('<rect x="-9.5" y="-5" width="7.5" height="0.6" fill="white"/>')
        parts.append('<rect x="-9.5" y="-2.8" width="7.5" height="0.6" fill="white"/>')
        parts.append('<rect x="-9.5" y="-0.6" width="7.5" height="0.6" fill="white"/>')
        parts.append('<rect x="-9.5" y="1.6" width="5" height="0.6" fill="white"/>')
        parts.append('<rect x="-9.5" y="3.8" width="7.5" height="0.6" fill="white"/>')
        # Linee di testo pagina destra
        parts.append('<rect x="2" y="-5" width="7.5" height="0.6" fill="white"/>')
        parts.append('<rect x="2" y="-2.8" width="7.5" height="0.6" fill="white"/>')
        parts.append('<rect x="2" y="-0.6" width="7.5" height="0.6" fill="white"/>')
        parts.append('<rect x="2" y="1.6" width="6" height="0.6" fill="white"/>')
        parts.append('<rect x="2" y="3.8" width="7.5" height="0.6" fill="white"/>')
        parts.append('</g>')
        return "".join(parts)

    # ASTRATTI =====================================================
    if sym_id == "star":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<polygon points="0,-10 3,-3 10,-3 4.5,1.5 6.5,9 0,5 -6.5,9 -4.5,1.5 -10,-3 -3,-3" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "heart":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M 0 9 C -11 0 -11 -9 -5 -9 C -2 -9 0 -6 0 -4 C 0 -6 2 -9 5 -9 C 11 -9 11 0 0 9 Z" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "eye_inside":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M -10 0 Q 0 -7 10 0 Q 0 7 -10 0 Z" fill="none" stroke="' + color + '" stroke-width="1.8"/>')
        parts.append('<circle cx="0" cy="0" r="4" fill="' + color + '"/>')
        parts.append('<circle cx="0" cy="0" r="1.8" fill="white"/>')
        parts.append('<circle cx="0" cy="0" r="0.7" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "lightning":
        # Saetta classica a zigzag con spigoli netti
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<polygon points="1,-12 -4,0 0,0 -2,12 6,-2 2,-2 5,-12" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    return ""


def render_lashes(shape, style, color):
    if style == "none":
        return ""
    if shape == "round":
        top_y = 40
        xs = [50, 65, 80, 100, 120, 135, 150]
    elif shape == "almond":
        top_y = 52
        xs = [50, 70, 90, 100, 110, 130, 150]
    elif shape == "wide":
        top_y = 42
        xs = [45, 65, 85, 100, 115, 135, 155]
    else:
        top_y = 70
        xs = [50, 70, 90, 100, 110, 130, 150]

    if style == "long":
        length = 20
        thick = 2.5
    elif style == "short":
        length = 8
        thick = 2.0
    elif style == "thick":
        length = 14
        thick = 3.5
    else:
        length = 13
        thick = 2.2

    out = []
    for x in xs:
        tilt = (x - 100) * 0.25
        x2 = x + tilt
        y2 = top_y - length
        out.append('<line x1="' + str(x) + '" y1="' + str(top_y) + '" x2="' + str(x2) + '" y2="' + str(y2) + '" stroke="' + color + '" stroke-width="' + str(thick) + '" stroke-linecap="round"/>')
    return "".join(out)


def render_background(bg_id):
    bg = next((b for b in BACKGROUNDS if b["id"] == bg_id), BACKGROUNDS[0])
    out = ['<rect width="200" height="200" fill="' + bg["color"] + '"/>']

    if bg_id == "nola_jazz":
        out.append('<rect width="200" height="200" fill="#2a0a3a"/>')
        out.append('<g opacity="0.25" fill="' + BRAND_YELLOW + '">')
        out.append('<ellipse cx="30" cy="45" rx="5" ry="3.5" transform="rotate(-20 30 45)"/>')
        out.append('<rect x="33" y="25" width="1.5" height="22"/>')
        out.append('<ellipse cx="170" cy="60" rx="5" ry="3.5" transform="rotate(-20 170 60)"/>')
        out.append('<rect x="173" y="40" width="1.5" height="22"/>')
        out.append('<ellipse cx="40" cy="160" rx="5" ry="3.5" transform="rotate(-20 40 160)"/>')
        out.append('<rect x="43" y="140" width="1.5" height="22"/>')
        out.append('<ellipse cx="160" cy="170" rx="5" ry="3.5" transform="rotate(-20 160 170)"/>')
        out.append('<rect x="163" y="150" width="1.5" height="22"/>')
        out.append('</g>')

    elif bg_id == "peccioli_hills":
        out.append('<rect y="0" width="200" height="110" fill="#b8dcf0"/>')
        out.append('<circle cx="155" cy="45" r="14" fill="' + BRAND_YELLOW + '" opacity="0.9"/>')
        out.append('<ellipse cx="50" cy="35" rx="15" ry="5" fill="white" opacity="0.75"/>')
        out.append('<ellipse cx="90" cy="55" rx="12" ry="4" fill="white" opacity="0.65"/>')
        out.append('<path d="M 0 130 Q 50 100 100 115 Q 150 95 200 120 L 200 200 L 0 200 Z" fill="#4a9960" opacity="0.65"/>')
        out.append('<path d="M 0 155 Q 40 130 90 140 Q 140 125 200 145 L 200 200 L 0 200 Z" fill="#2e7a42"/>')
        out.append('<ellipse cx="40" cy="138" rx="3" ry="10" fill="#1a5028"/>')
        out.append('<ellipse cx="130" cy="130" rx="3" ry="10" fill="#1a5028"/>')
        out.append('<ellipse cx="165" cy="140" rx="3" ry="10" fill="#1a5028"/>')
        out.append('<path d="M 0 180 Q 100 170 200 182 L 200 200 L 0 200 Z" fill="#1a7a4a"/>')

    elif bg_id == "ghizzano":
        # Cielo chiaro
        out.append('<defs><linearGradient id="sky-ghiz" x1="0" x2="0" y1="0" y2="1">')
        out.append('<stop offset="0%" stop-color="#b8c8d8"/><stop offset="100%" stop-color="#d8ddd5"/></linearGradient>')
        out.append('<linearGradient id="street-ghiz" x1="0" x2="0" y1="0" y2="1">')
        out.append('<stop offset="0%" stop-color="#b8b0a0"/><stop offset="100%" stop-color="#d0cabc"/></linearGradient></defs>')
        out.append('<rect width="200" height="67" fill="url(#sky-ghiz)"/>')
        # Strada in prospettiva
        out.append('<polygon points="0,200 200,200 125,67 75,67" fill="url(#street-ghiz)"/>')
        out.append('<g stroke="#8a8070" stroke-width="0.5" opacity="0.4">')
        out.append('<line x1="50" y1="150" x2="87" y2="75"/>')
        out.append('<line x1="150" y1="150" x2="113" y2="75"/>')
        out.append('<line x1="25" y1="183" x2="80" y2="70"/>')
        out.append('<line x1="175" y1="183" x2="120" y2="70"/>')
        out.append('</g>')
        # Casa fucsia sinistra
        out.append('<polygon points="0,67 75,67 75,200 0,200" fill="#c8226a"/>')
        out.append('<rect x="13" y="92" width="17" height="20" fill="#f4d03f" stroke="#2a1010" stroke-width="0.8"/>')
        out.append('<rect x="43" y="117" width="24" height="67" fill="#8a1040" stroke="#2a1010" stroke-width="0.8"/>')
        out.append('<rect x="50" y="125" width="10" height="13" fill="#f4d03f"/>')
        out.append('<rect x="0" y="67" width="75" height="3" fill="#8a1040"/>')
        # Casa verde destra
        out.append('<polygon points="125,67 200,67 200,200 125,200" fill="#5ab848"/>')
        out.append('<rect x="158" y="117" width="30" height="75" fill="#4a2818" stroke="#2a1008" stroke-width="0.8"/>')
        out.append('<rect x="162" y="120" width="23" height="23" fill="none" stroke="#2a1008" stroke-width="0.6"/>')
        out.append('<rect x="162" y="147" width="23" height="23" fill="none" stroke="#2a1008" stroke-width="0.6"/>')
        out.append('<rect x="130" y="87" width="20" height="17" fill="#c82828" stroke="#2a1010" stroke-width="0.8"/>')
        out.append('<rect x="125" y="67" width="75" height="3" fill="#3a8028"/>')
        # Casa lime centrale
        out.append('<polygon points="87,77 113,77 113,150 87,150" fill="#a8d430"/>')
        out.append('<rect x="90" y="87" width="7" height="8" fill="#3a2418"/>')
        out.append('<rect x="100" y="87" width="7" height="8" fill="#3a2418"/>')
        out.append('<rect x="90" y="108" width="7" height="8" fill="#3a2418"/>')
        out.append('<rect x="100" y="108" width="7" height="8" fill="#3a2418"/>')
        out.append('<rect x="93" y="130" width="14" height="20" fill="#6a4020"/>')
        out.append('<polygon points="87,77 113,77 100,68" fill="#8aa028"/>')
        # Casa terracotta
        out.append('<polygon points="67,70 87,70 87,142 67,142" fill="#a04830"/>')
        out.append('<rect x="72" y="80" width="7" height="8" fill="#2a1008"/>')
        out.append('<rect x="80" y="80" width="4" height="8" fill="#2a1008"/>')
        out.append('<rect x="72" y="100" width="7" height="8" fill="#2a1008"/>')
        # Casa ocra
        out.append('<polygon points="92,67 108,67 108,80 92,80" fill="#d49040"/>')
        # Lampione parete
        out.append('<circle cx="33" cy="83" r="3" fill="#4a3020"/>')
        out.append('<rect x="30" y="83" width="7" height="3" fill="#ffd088"/>')
        # Vasi fiori destra
        out.append('<rect x="130" y="180" width="8" height="10" fill="#8a5030"/>')
        out.append('<circle cx="134" cy="175" r="5" fill="#3a8028"/>')
        out.append('<rect x="142" y="183" width="6" height="7" fill="#8a5030"/>')
        out.append('<circle cx="145" cy="180" r="4" fill="#d02020"/>')
        # Vasi fiori sinistra
        out.append('<rect x="53" y="180" width="8" height="10" fill="#8a5030"/>')
        out.append('<circle cx="57" cy="175" r="5" fill="#d04040"/>')
        # Lampione pendente
        out.append('<line x1="100" y1="70" x2="100" y2="80" stroke="#2a1a10" stroke-width="0.7"/>')
        out.append('<circle cx="100" cy="83" r="2" fill="#ffd088" opacity="0.9"/>')

    elif bg_id == "muro_occhi":
        # Muro di pietra
        out.append('<defs><pattern id="stone-wall" x="0" y="0" width="25" height="13" patternUnits="userSpaceOnUse">')
        out.append('<rect width="25" height="13" fill="#8a7a6a"/>')
        out.append('<rect x="0" y="0" width="10" height="6" fill="#9a8a7a" stroke="#6a5a4a" stroke-width="0.4"/>')
        out.append('<rect x="12" y="0" width="13" height="6" fill="#a89888" stroke="#6a5a4a" stroke-width="0.4"/>')
        out.append('<rect x="0" y="7" width="15" height="6" fill="#948474" stroke="#6a5a4a" stroke-width="0.4"/>')
        out.append('<rect x="17" y="7" width="8" height="6" fill="#a49484" stroke="#6a5a4a" stroke-width="0.4"/>')
        out.append('</pattern></defs>')
        out.append('<rect width="200" height="200" fill="url(#stone-wall)"/>')
        # Occhi disposti irregolarmente (coordinate scalate x 1.67)
        eye_positions = [
            (25, 25, -3, "#4a7a3a"), (70, 22, 2, "#6b5d3a"), (120, 27, -2, "#3a6ba5"), (167, 23, 3, "#8a5a3a"),
            (47, 53, 1, "#4a7a3a"), (93, 50, -3, "#3a6ba5"), (145, 57, 2, "#5a3a6a"),
            (30, 92, 2, "#6b5d3a"), (158, 97, -2, "#4a7a3a"),
            (30, 133, -2, "#3a6ba5"), (75, 142, 3, "#8a5a3a"), (125, 137, -1, "#5a3a6a"), (172, 143, 2, "#4a7a3a"),
            (50, 175, 1, "#6b5d3a"), (103, 178, -3, "#3a6ba5"), (153, 180, 2, "#8a5a3a"),
        ]
        for ex, ey, rot, iris_col in eye_positions:
            out.append('<g transform="translate(' + str(ex) + ',' + str(ey) + ') rotate(' + str(rot) + ')">')
            out.append('<rect x="-17" y="-8" width="33" height="17" fill="#e8d4b0" stroke="#6a5a3a" stroke-width="0.5"/>')
            out.append('<ellipse cx="0" cy="0" rx="8" ry="4" fill="white"/>')
            out.append('<circle cx="0" cy="0" r="3.3" fill="' + iris_col + '"/>')
            out.append('<circle cx="0" cy="0" r="1.3" fill="#1a1a1a"/>')
            out.append('<path d="M -8 -4 Q 0 -6 8 -4" fill="none" stroke="#3a2a1a" stroke-width="0.6"/>')
            out.append('</g>')
        # Finestra centrale nera con inferriata
        out.append('<rect x="80" y="80" width="40" height="40" fill="#1a1a1a" stroke="#3a2a1a" stroke-width="1.5"/>')
        out.append('<line x1="90" y1="80" x2="90" y2="120" stroke="#4a4a4a" stroke-width="1.5"/>')
        out.append('<line x1="100" y1="80" x2="100" y2="120" stroke="#4a4a4a" stroke-width="1.5"/>')
        out.append('<line x1="110" y1="80" x2="110" y2="120" stroke="#4a4a4a" stroke-width="1.5"/>')
        out.append('<line x1="80" y1="100" x2="120" y2="100" stroke="#4a4a4a" stroke-width="1.2"/>')
        out.append('<circle cx="100" cy="117" r="3" fill="#5a7a30"/>')

    elif bg_id == "macca":
        # Cielo tramonto
        out.append('<defs><linearGradient id="sky-macca" x1="0" x2="0" y1="0" y2="1">')
        out.append('<stop offset="0%" stop-color="#3a4a7a"/>')
        out.append('<stop offset="30%" stop-color="#7a5a7a"/>')
        out.append('<stop offset="65%" stop-color="#d88a7a"/>')
        out.append('<stop offset="90%" stop-color="#e8b080"/>')
        out.append('<stop offset="100%" stop-color="#f0c898"/></linearGradient>')
        out.append('<linearGradient id="valley-macca" x1="0" x2="0" y1="0" y2="1">')
        out.append('<stop offset="0%" stop-color="#2a3a30"/><stop offset="100%" stop-color="#0a1818"/></linearGradient></defs>')
        out.append('<rect width="200" height="120" fill="url(#sky-macca)"/>')
        out.append('<rect y="120" width="200" height="80" fill="url(#valley-macca)"/>')
        out.append('<path d="M 0 130 Q 50 123 100 127 T 200 125 L 200 142 L 0 142 Z" fill="#1a2a28" opacity="0.9"/>')
        # Borgo di 5 case attaccate al museo
        # Casa 1 con campanile
        out.append('<rect x="0" y="50" width="23" height="75" fill="#d88060"/>')
        out.append('<rect x="5" y="33" width="8" height="20" fill="#c07048"/>')
        out.append('<polygon points="5,33 13,33 9,23" fill="#a05838"/>')
        out.append('<rect x="7" y="40" width="3" height="5" fill="#1a1a1a"/>')
        # Casa 2
        out.append('<rect x="23" y="58" width="20" height="67" fill="#c87058"/>')
        out.append('<rect x="28" y="70" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="35" y="70" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="28" y="87" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="35" y="87" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="28" y="103" width="5" height="7" fill="#ffd088"/>')
        # Casa 3 (ocra)
        out.append('<rect x="43" y="53" width="23" height="72" fill="#d49860"/>')
        out.append('<rect x="48" y="67" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="57" y="67" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="48" y="83" width="5" height="7" fill="#ffd088"/>')
        out.append('<rect x="57" y="83" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="48" y="100" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="57" y="100" width="5" height="7" fill="#ffd088"/>')
        out.append('<polygon points="43,53 66,53 55,45" fill="#8a4a30"/>')
        # Casa 4
        out.append('<rect x="66" y="60" width="20" height="65" fill="#b86848"/>')
        out.append('<rect x="72" y="70" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="78" y="70" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="72" y="87" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="78" y="87" width="5" height="7" fill="#ffd088"/>')
        # Casa 5
        out.append('<rect x="86" y="55" width="23" height="70" fill="#c88870"/>')
        out.append('<rect x="91" y="67" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="100" y="67" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="91" y="87" width="5" height="7" fill="#ffd088"/>')
        out.append('<rect x="100" y="87" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="91" y="103" width="5" height="7" fill="#2a1a18"/>')
        out.append('<rect x="100" y="103" width="5" height="7" fill="#2a1a18"/>')
        out.append('<polygon points="86,55 110,55 98,47" fill="#7a4028"/>')
        # Edificio museo MACCA
        out.append('<rect x="110" y="63" width="53" height="62" fill="#e8dac0"/>')
        out.append('<rect x="107" y="60" width="60" height="5" fill="#d8c8a8"/>')
        out.append('<g fill="#3a2a20" opacity="0.85">')
        out.append('<rect x="113" y="70" width="5" height="50"/>')
        out.append('<rect x="120" y="70" width="5" height="50"/>')
        out.append('<rect x="127" y="70" width="5" height="50"/>')
        out.append('<rect x="134" y="70" width="5" height="50"/>')
        out.append('<rect x="141" y="70" width="5" height="50"/>')
        out.append('<rect x="148" y="70" width="5" height="50"/>')
        out.append('<rect x="155" y="70" width="5" height="50"/>')
        out.append('</g>')
        out.append('<rect x="110" y="70" width="53" height="50" fill="#ffd088" opacity="0.35"/>')
        # Terrazza grande a destra
        out.append('<rect x="147" y="87" width="50" height="13" fill="#4a3a28"/>')
        out.append('<rect x="147" y="97" width="50" height="5" fill="#2a1a10"/>')
        out.append('<rect x="147" y="73" width="50" height="14" fill="none" stroke="#2a1a10" stroke-width="1"/>')
        out.append('<g stroke="#2a1a10" stroke-width="0.8">')
        out.append('<line x1="153" y1="73" x2="153" y2="87"/>')
        out.append('<line x1="162" y1="73" x2="162" y2="87"/>')
        out.append('<line x1="170" y1="73" x2="170" y2="87"/>')
        out.append('<line x1="178" y1="73" x2="178" y2="87"/>')
        out.append('<line x1="187" y1="73" x2="187" y2="87"/>')
        out.append('</g>')
        # Persone sulla terrazza
        out.append('<g fill="#1a1a1a">')
        out.append('<rect x="157" y="63" width="3" height="10"/><circle cx="158.5" cy="61" r="2"/>')
        out.append('<rect x="166" y="63" width="3" height="10"/><circle cx="167.5" cy="61" r="2"/>')
        out.append('<rect x="177" y="65" width="3" height="8"/><circle cx="178.5" cy="63" r="1.7"/>')
        out.append('<rect x="182" y="65" width="3" height="8"/><circle cx="183.5" cy="63" r="1.7"/>')
        out.append('<rect x="187" y="65" width="3" height="8"/><circle cx="188.5" cy="63" r="1.7"/>')
        out.append('</g>')
        # Luci terrazza
        out.append('<circle cx="153" cy="83" r="2" fill="#ffd088" opacity="0.95"/>')
        out.append('<circle cx="170" cy="83" r="2" fill="#ffd088" opacity="0.95"/>')
        out.append('<circle cx="187" cy="83" r="2" fill="#ffd088" opacity="0.95"/>')
        # Colonne sotto terrazza
        out.append('<g fill="#2a1a10">')
        out.append('<rect x="158" y="100" width="3" height="30"/>')
        out.append('<rect x="175" y="100" width="3" height="33"/>')
        out.append('<rect x="190" y="100" width="3" height="37"/>')
        out.append('</g>')
        # Alberi primo piano
        out.append('<g fill="#0a1410" opacity="0.95">')
        out.append('<circle cx="63" cy="170" r="12"/>')
        out.append('<circle cx="80" cy="175" r="10"/>')
        out.append('<circle cx="108" cy="178" r="8"/>')
        out.append('<circle cx="133" cy="175" r="10"/>')
        out.append('</g>')

    elif bg_id == "peccioli_tower":
        # Cielo B/N
        out.append('<defs><linearGradient id="sky-bell" x1="0" x2="0" y1="0" y2="1">')
        out.append('<stop offset="0%" stop-color="#c8c8c8"/><stop offset="50%" stop-color="#dcdcdc"/><stop offset="100%" stop-color="#f0f0f0"/></linearGradient>')
        out.append('<linearGradient id="stone-tower" x1="0" x2="1" y1="0" y2="0">')
        out.append('<stop offset="0%" stop-color="#8a8278"/><stop offset="50%" stop-color="#b0a89c"/><stop offset="100%" stop-color="#7a7268"/></linearGradient>')
        out.append('<linearGradient id="roof-tower" x1="0" x2="1" y1="0" y2="0">')
        out.append('<stop offset="0%" stop-color="#6a6258"/><stop offset="50%" stop-color="#8a8278"/><stop offset="100%" stop-color="#5a524a"/></linearGradient></defs>')
        out.append('<rect width="200" height="200" fill="url(#sky-bell)"/>')
        # Nuvole
        out.append('<ellipse cx="33" cy="92" rx="27" ry="7" fill="#ffffff" opacity="0.85"/>')
        out.append('<ellipse cx="47" cy="97" rx="17" ry="5" fill="#ffffff" opacity="0.7"/>')
        out.append('<ellipse cx="17" cy="117" rx="17" ry="5" fill="#ffffff" opacity="0.55"/>')
        # Base quadrata con blocchi
        out.append('<rect x="125" y="142" width="37" height="58" fill="url(#stone-tower)"/>')
        out.append('<g stroke="#5a524a" stroke-width="0.5" opacity="0.6">')
        out.append('<line x1="125" y1="158" x2="162" y2="158"/>')
        out.append('<line x1="125" y1="175" x2="162" y2="175"/>')
        out.append('<line x1="125" y1="192" x2="162" y2="192"/>')
        out.append('<line x1="137" y1="142" x2="137" y2="158"/>')
        out.append('<line x1="148" y1="142" x2="148" y2="158"/>')
        out.append('<line x1="132" y1="158" x2="132" y2="175"/>')
        out.append('<line x1="142" y1="158" x2="142" y2="175"/>')
        out.append('<line x1="155" y1="158" x2="155" y2="175"/>')
        out.append('<line x1="130" y1="175" x2="130" y2="192"/>')
        out.append('<line x1="147" y1="175" x2="147" y2="192"/>')
        out.append('<line x1="158" y1="175" x2="158" y2="192"/>')
        out.append('</g>')
        # Monofora con vetrata verde
        out.append('<path d="M 137 167 L 137 157 Q 137 152 143 152 Q 150 152 150 157 L 150 167 Z" fill="#1a1a1a"/>')
        out.append('<rect x="139.5" y="157" width="8" height="10" fill="#2a7060" opacity="0.75"/>')
        out.append('<line x1="143" y1="157" x2="143" y2="167" stroke="#3a2a20" stroke-width="0.7"/>')
        # Cornice
        out.append('<rect x="120" y="137" width="47" height="5" fill="#5a524a"/>')
        out.append('<rect x="122" y="133" width="43" height="3" fill="#6a6258"/>')
        # Primo ordine bifora
        out.append('<rect x="125" y="100" width="37" height="33" fill="url(#stone-tower)"/>')
        out.append('<path d="M 132 130 L 132 117 Q 132 110 137 110 L 137 130 Z" fill="#1a1a1a"/>')
        out.append('<path d="M 150 130 L 150 117 Q 150 110 155 110 L 155 130 Z" fill="#1a1a1a"/>')
        out.append('<rect x="142" y="110" width="3" height="20" fill="#5a524a"/>')
        out.append('<path d="M 137 110 Q 143 107 150 110" fill="none" stroke="#5a524a" stroke-width="0.7"/>')
        out.append('<rect x="140.8" y="108" width="5" height="2" fill="#6a6258"/>')
        out.append('<rect x="133" y="120" width="3" height="10" fill="#2a7060" opacity="0.75"/>')
        out.append('<rect x="150" y="120" width="3" height="10" fill="#2a7060" opacity="0.75"/>')
        # Cornice
        out.append('<rect x="120" y="97" width="47" height="3" fill="#5a524a"/>')
        out.append('<rect x="122" y="93" width="43" height="3" fill="#6a6258"/>')
        # Secondo ordine bifora
        out.append('<rect x="128" y="67" width="30" height="27" fill="url(#stone-tower)"/>')
        out.append('<path d="M 133 90 L 133 77 Q 133 72 138 72 L 138 90 Z" fill="#1a1a1a"/>')
        out.append('<path d="M 148 90 L 148 77 Q 148 72 153 72 L 153 90 Z" fill="#1a1a1a"/>')
        out.append('<rect x="142" y="72" width="2" height="18" fill="#5a524a"/>')
        out.append('<path d="M 138 72 Q 143 69 148 72" fill="none" stroke="#5a524a" stroke-width="0.5"/>')
        # Cornice prima del tamburo
        out.append('<rect x="123" y="63" width="40" height="3" fill="#5a524a"/>')
        out.append('<rect x="125" y="60" width="36" height="3" fill="#6a6258"/>')
        out.append('<rect x="127" y="57" width="32" height="3" fill="#7a7268"/>')
        # Tamburo ottagonale
        out.append('<polygon points="130,57 157,57 155,45 132,45" fill="url(#stone-tower)"/>')
        out.append('<g fill="#3a3028" opacity="0.8">')
        out.append('<path d="M 133 53 L 133 49 Q 133 48 136 48 Q 139 48 139 49 L 139 53 Z"/>')
        out.append('<path d="M 140 53 L 140 49 Q 140 48 143 48 Q 146 48 146 49 L 146 53 Z"/>')
        out.append('<path d="M 147 53 L 147 49 Q 147 48 150 48 Q 153 48 153 49 L 153 53 Z"/>')
        out.append('</g>')
        out.append('<rect x="130" y="41" width="3" height="4" fill="#6a6258"/>')
        out.append('<rect x="137" y="41" width="3" height="4" fill="#6a6258"/>')
        out.append('<rect x="144" y="41" width="3" height="4" fill="#6a6258"/>')
        out.append('<rect x="151" y="41" width="3" height="4" fill="#6a6258"/>')
        # Tetto a pagoda
        out.append('<polygon points="130,41 157,41 143,8" fill="url(#roof-tower)"/>')
        out.append('<line x1="143" y1="8" x2="143" y2="41" stroke="#3a3028" stroke-width="0.8" opacity="0.6"/>')
        out.append('<line x1="137" y1="25" x2="133" y2="41" stroke="#3a3028" stroke-width="0.5" opacity="0.5"/>')
        out.append('<line x1="150" y1="25" x2="154" y2="41" stroke="#3a3028" stroke-width="0.5" opacity="0.5"/>')
        out.append('<g stroke="#3a3028" stroke-width="0.4" opacity="0.5">')
        out.append('<line x1="135" y1="33" x2="152" y2="33"/>')
        out.append('<line x1="137" y1="28" x2="150" y2="28"/>')
        out.append('<line x1="139" y1="22" x2="147" y2="22"/>')
        out.append('<line x1="140" y1="17" x2="146" y2="17"/>')
        out.append('</g>')
        # Pennacchio + banderuola
        out.append('<rect x="142" y="3" width="2" height="7" fill="#3a3028"/>')
        out.append('<circle cx="143" cy="5" r="1.7" fill="#5a524a"/>')
        out.append('<polygon points="143,2 148,3 143,5" fill="#3a3028"/>')
        # Rondini
        out.append('<g fill="#1a1a1a">')
        out.append('<path d="M 30 63 L 38 56 L 47 63 L 42 61 L 38 62 L 35 61 Z"/>')
        out.append('<path d="M 50 53 L 55 50 L 60 53 L 55 52 Z"/>')
        out.append('<path d="M 67 45 L 72 42 L 77 45 L 72 44 Z"/>')
        out.append('<path d="M 83 38 L 87 36 L 92 38 L 87 37 Z"/>')
        out.append('<path d="M 20 80 L 27 75 L 33 80 L 27 78 Z"/>')
        out.append('<path d="M 40 70 L 45 67 L 50 70 L 45 69 Z"/>')
        out.append('<path d="M 60 63 L 65 60 L 70 63 L 65 62 Z"/>')
        out.append('<path d="M 8 97 L 15 92 L 22 97 L 15 95 Z"/>')
        out.append('<path d="M 33 93 L 40 89 L 47 93 L 40 91 Z"/>')
        out.append('</g>')

    elif bg_id == "french_quarter":
        # Cielo
        out.append('<defs><linearGradient id="sky-fq" x1="0" x2="0" y1="0" y2="1">')
        out.append('<stop offset="0%" stop-color="#87CEEB"/><stop offset="100%" stop-color="#b5d8e8"/></linearGradient>')
        out.append('<pattern id="ironwork" x="0" y="0" width="13" height="13" patternUnits="userSpaceOnUse">')
        out.append('<circle cx="6.5" cy="6.5" r="2.5" fill="none" stroke="#1a1a1a" stroke-width="0.8"/>')
        out.append('<line x1="0" y1="6.5" x2="13" y2="6.5" stroke="#1a1a1a" stroke-width="0.5"/>')
        out.append('<line x1="6.5" y1="0" x2="6.5" y2="13" stroke="#1a1a1a" stroke-width="0.5"/>')
        out.append('</pattern></defs>')
        out.append('<rect width="200" height="33" fill="url(#sky-fq)"/>')
        # Edificio rosso mattone
        out.append('<rect x="0" y="30" width="200" height="170" fill="#a85a3a"/>')
        # 1° piano finestre
        out.append('<g fill="#3a2418">')
        out.append('<rect x="13" y="47" width="23" height="40"/>')
        out.append('<rect x="50" y="47" width="23" height="40"/>')
        out.append('<rect x="87" y="47" width="23" height="40"/>')
        out.append('<rect x="123" y="47" width="23" height="40"/>')
        out.append('<rect x="160" y="47" width="23" height="40"/>')
        out.append('</g>')
        # Balcone 1° piano
        out.append('<rect x="0" y="90" width="200" height="13" fill="url(#ironwork)" opacity="0.8"/>')
        out.append('<rect x="0" y="88" width="200" height="2" fill="#1a1a1a"/>')
        out.append('<rect x="0" y="103" width="200" height="2" fill="#1a1a1a"/>')
        # 2° piano finestre
        out.append('<g fill="#3a2418">')
        out.append('<rect x="13" y="113" width="23" height="40"/>')
        out.append('<rect x="50" y="113" width="23" height="40"/>')
        out.append('<rect x="87" y="113" width="23" height="40"/>')
        out.append('<rect x="123" y="113" width="23" height="40"/>')
        out.append('<rect x="160" y="113" width="23" height="40"/>')
        out.append('</g>')
        # Balcone 2° piano
        out.append('<rect x="0" y="157" width="200" height="13" fill="url(#ironwork)" opacity="0.8"/>')
        out.append('<rect x="0" y="155" width="200" height="2" fill="#1a1a1a"/>')
        out.append('<rect x="0" y="170" width="200" height="2" fill="#1a1a1a"/>')
        # Piante appese
        out.append('<g fill="#4a7a2a">')
        out.append('<circle cx="23" cy="100" r="6"/>')
        out.append('<circle cx="62" cy="100" r="6"/>')
        out.append('<circle cx="98" cy="100" r="6"/>')
        out.append('<circle cx="135" cy="100" r="6"/>')
        out.append('<circle cx="172" cy="100" r="6"/>')
        out.append('<circle cx="23" cy="167" r="6"/>')
        out.append('<circle cx="62" cy="167" r="6"/>')
        out.append('<circle cx="98" cy="167" r="6"/>')
        out.append('<circle cx="135" cy="167" r="6"/>')
        out.append('<circle cx="172" cy="167" r="6"/>')
        out.append('</g>')
        # Marciapiede
        out.append('<rect x="0" y="177" width="200" height="23" fill="#9a9a9a"/>')

    elif bg_id == "sunset_mississippi":
        # Cielo tramonto
        out.append('<defs><linearGradient id="sunset-nola" x1="0" x2="0" y1="0" y2="1">')
        out.append('<stop offset="0%" stop-color="#ff9a8b"/>')
        out.append('<stop offset="40%" stop-color="#ffb199"/>')
        out.append('<stop offset="70%" stop-color="#ffc9a9"/>')
        out.append('<stop offset="100%" stop-color="#d4a8c5"/></linearGradient>')
        out.append('<linearGradient id="river-nola" x1="0" x2="0" y1="0" y2="1">')
        out.append('<stop offset="0%" stop-color="#7a92a8"/><stop offset="100%" stop-color="#5a7088"/></linearGradient></defs>')
        out.append('<rect width="200" height="100" fill="url(#sunset-nola)"/>')
        # Nuvole rosate
        out.append('<ellipse cx="42" cy="30" rx="20" ry="5" fill="#ffd4c4" opacity="0.7"/>')
        out.append('<ellipse cx="133" cy="20" rx="25" ry="4" fill="#ffd4c4" opacity="0.7"/>')
        out.append('<ellipse cx="167" cy="42" rx="17" ry="4" fill="#f5b8a8" opacity="0.6"/>')
        # Skyline
        out.append('<g fill="#4a5a6a">')
        out.append('<rect x="17" y="70" width="13" height="33"/>')
        out.append('<rect x="33" y="58" width="17" height="45"/>')
        out.append('<rect x="53" y="50" width="13" height="53"/>')
        out.append('<rect x="70" y="63" width="10" height="40"/>')
        out.append('<rect x="83" y="42" width="17" height="61"/>')
        out.append('<rect x="103" y="53" width="12" height="50"/>')
        out.append('<rect x="117" y="47" width="15" height="56"/>')
        out.append('<rect x="135" y="60" width="12" height="43"/>')
        out.append('<rect x="150" y="67" width="13" height="36"/>')
        out.append('<rect x="167" y="55" width="12" height="48"/>')
        out.append('</g>')
        # Luci
        out.append('<g fill="#ffdc70">')
        out.append('<rect x="20" y="80" width="2" height="2"/>')
        out.append('<rect x="37" y="70" width="2" height="2"/>')
        out.append('<rect x="57" y="63" width="2" height="2"/>')
        out.append('<rect x="87" y="53" width="2" height="2"/>')
        out.append('<rect x="93" y="63" width="2" height="2"/>')
        out.append('<rect x="120" y="58" width="2" height="2"/>')
        out.append('<rect x="127" y="70" width="2" height="2"/>')
        out.append('<rect x="153" y="73" width="2" height="2"/>')
        out.append('</g>')
        # Lungofiume + fiume
        out.append('<rect y="103" width="200" height="8" fill="#3a4a5a"/>')
        out.append('<rect y="111" width="200" height="58" fill="url(#river-nola)"/>')
        # Battello
        out.append('<rect x="117" y="125" width="37" height="13" fill="white"/>')
        out.append('<rect x="120" y="120" width="30" height="5" fill="white"/>')
        out.append('<rect x="130" y="113" width="3" height="7" fill="#a84030"/>')
        out.append('<rect x="140" y="113" width="3" height="7" fill="#a84030"/>')
        out.append('<rect x="117" y="138" width="37" height="3" fill="#a84030"/>')
        # Riflessi
        out.append('<g fill="#3a4a5a" opacity="0.35">')
        out.append('<rect x="33" y="111" width="17" height="20"/>')
        out.append('<rect x="53" y="111" width="13" height="23"/>')
        out.append('<rect x="83" y="111" width="17" height="27"/>')
        out.append('<rect x="117" y="111" width="15" height="23"/>')
        out.append('</g>')
        # Prato primo piano
        out.append('<rect y="169" width="200" height="31" fill="#5a6a50"/>')

    elif bg_id == "mardigras":
        # Cielo
        out.append('<defs><linearGradient id="sky-mardi" x1="0" x2="0" y1="0" y2="1">')
        out.append('<stop offset="0%" stop-color="#4ba5c5"/><stop offset="100%" stop-color="#a8d5e8"/></linearGradient></defs>')
        out.append('<rect width="200" height="92" fill="url(#sky-mardi)"/>')
        # Carro bianco
        out.append('<rect x="17" y="125" width="167" height="42" fill="#f0f0f0"/>')
        # Decorazioni carro
        out.append('<path d="M 17 125 L 25 133 L 33 125 L 42 133 L 50 125 L 58 133 L 67 125 L 75 133 L 83 125 L 92 133 L 100 125 L 108 133 L 117 125 L 125 133 L 133 125 L 142 133 L 150 125 L 158 133 L 167 125 L 175 133 L 183 125 L 183 130 L 17 130 Z" fill="#d4a017"/>')
        # Piume rosa sinistra
        out.append('<path d="M 37 125 Q 25 92 20 63 Q 17 42 25 30 Q 33 42 37 63 Q 40 92 42 125 Z" fill="#ff4d8a" opacity="0.85"/>')
        out.append('<path d="M 50 125 Q 42 87 37 53 Q 33 33 43 25 Q 53 37 53 58 Q 53 92 55 125 Z" fill="#ff6ba0" opacity="0.85"/>')
        out.append('<path d="M 63 125 Q 58 92 58 63 Q 60 42 70 37 Q 73 50 70 67 Q 68 92 67 125 Z" fill="#ff85b0" opacity="0.8"/>')
        # Figura regale centrale (re)
        out.append('<path d="M 92 125 L 92 100 L 83 92 L 100 80 L 117 92 L 108 100 L 108 125 Z" fill="#a84030"/>')
        out.append('<circle cx="100" cy="80" r="8" fill="#e8b79a"/>')
        out.append('<polygon points="92,73 100,63 108,73 105,80 95,80" fill="#d4a017"/>')
        # Piume bianche destra
        out.append('<path d="M 133 125 Q 125 92 120 58 Q 117 33 127 25 Q 137 37 137 63 Q 137 92 138 125 Z" fill="#ffffff" opacity="0.9"/>')
        out.append('<path d="M 150 125 Q 142 92 140 63 Q 140 37 150 30 Q 158 42 157 67 Q 153 92 153 125 Z" fill="#ffffff" opacity="0.85"/>')
        out.append('<path d="M 167 125 Q 160 92 160 63 Q 162 42 170 37 Q 175 50 172 70 Q 168 97 167 125 Z" fill="#e8e8f0" opacity="0.85"/>')
        # Figura regale bianca (regina)
        out.append('<path d="M 142 125 L 142 103 L 133 97 L 147 87 L 160 97 L 152 103 L 152 125 Z" fill="#e8e0f0"/>')
        out.append('<circle cx="147" cy="87" r="7" fill="#e8b79a"/>')
        out.append('<polygon points="140,82 147,73 153,82 152,87 142,87" fill="#d4a017"/>')
        # Coriandoli
        out.append('<g>')
        out.append('<rect x="25" y="42" width="3" height="5" fill="#ffde59" transform="rotate(20 27 44)"/>')
        out.append('<rect x="67" y="30" width="3" height="5" fill="#7a3d9a" transform="rotate(-15 68 32)"/>')
        out.append('<rect x="108" y="47" width="3" height="5" fill="#3d9a45" transform="rotate(30 110 49)"/>')
        out.append('<rect x="158" y="33" width="3" height="5" fill="#ffde59" transform="rotate(45 160 35)"/>')
        out.append('<rect x="83" y="17" width="3" height="5" fill="#7a3d9a" transform="rotate(-25 85 19)"/>')
        out.append('<rect x="42" y="67" width="3" height="5" fill="#3d9a45" transform="rotate(60 44 69)"/>')
        out.append('<rect x="133" y="70" width="3" height="5" fill="#ffde59" transform="rotate(-40 135 72)"/>')
        out.append('</g>')
        # Strada
        out.append('<rect y="167" width="200" height="33" fill="#888"/>')

    return "".join(out)


@st.cache_data(show_spinner=False)
def build_eye_svg(params_tuple, size=240):
    params = dict(params_tuple)
    eye_d = eye_path(params["shape"])

    if params["shape"] == "narrow":
        iris_radius = 22
    elif params["shape"] == "wide":
        iris_radius = 28
    else:
        iris_radius = 26

    stroke_color = params.get("border_color", "#ffffff")

    if params["bg"] == "white-solid":
        sclera_color = "#f4f1e8"
    else:
        sclera_color = "white"

    sym_color = params.get("symbol_color", "#130089")
    lash_color = params.get("lashes_color", "#1a1a1a")

    content = params["shape"] + params["iris"] + params["symbol"] + sym_color + params["bg"] + params["lashes"] + lash_color + stroke_color
    clip_id = "eye-clip-" + hashlib.md5(content.encode()).hexdigest()[:8]

    pupil_radius = iris_radius * 0.65

    parts = []
    parts.append('<svg viewBox="0 0 200 200" width="' + str(size) + '" height="' + str(size) + '" xmlns="http://www.w3.org/2000/svg">')
    parts.append('<defs><clipPath id="' + clip_id + '"><path d="' + eye_d + '"/></clipPath></defs>')
    parts.append(render_background(params["bg"]))
    parts.append('<path d="' + eye_d + '" fill="' + sclera_color + '" stroke="' + stroke_color + '" stroke-width="3"/>')
    parts.append('<g clip-path="url(#' + clip_id + ')">')
    parts.append('<circle cx="100" cy="100" r="' + str(iris_radius) + '" fill="' + params["iris"] + '"/>')
    parts.append('<circle cx="100" cy="100" r="' + str(pupil_radius) + '" fill="white"/>')
    scale_factor = pupil_radius / 12
    parts.append('<g transform="translate(100 100) scale(' + str(scale_factor) + ') translate(-100 -100)">')
    parts.append(render_symbol(params["symbol"], sym_color))
    parts.append('</g>')
    parts.append('</g>')
    parts.append(render_lashes(params["shape"], params["lashes"], lash_color))
    parts.append('</svg>')
    return "".join(parts)


def eye_svg(avatar_dict, size=240):
    keys = ["shape", "iris", "symbol", "symbol_color", "lashes", "lashes_color", "bg", "border_color"]
    tup = tuple((k, avatar_dict.get(k, DEFAULT_AVATAR[k])) for k in keys)
    return build_eye_svg(tup, size)


# ==================== CSS ====================
css_lines = []
css_lines.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
css_lines.append('<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lobster+Two:ital,wght@1,700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">')
css_lines.append('<style>')
css_lines.append('html, body, [class*="css"] { font-family: Inter, sans-serif; }')
css_lines.append('.block-container { max-width: 1100px; padding-top: 1.5rem; }')
css_lines.append('#MainMenu, header[data-testid="stHeader"], footer { display: none !important; }')
css_lines.append('.stButton>button { background: ' + BRAND_BLUE + ' !important; color: white !important; border: none !important; border-radius: 10px !important; font-weight: 600 !important; }')
css_lines.append('.stButton>button:hover { background: ' + BRAND_BLUE_DARK + ' !important; color: ' + BRAND_YELLOW + ' !important; }')
css_lines.append('.proto-banner { background: ' + BRAND_YELLOW_LIGHT + '; border-left: 4px solid ' + BRAND_YELLOW + '; border-radius: 0 10px 10px 0; padding: 0.7rem 1rem; margin-bottom: 1.5rem; font-size: 0.85rem; color: #8b6914; }')
css_lines.append('.login-hero { background: ' + BRAND_BLUE + '; border-radius: 24px; padding: 3rem 2rem 2rem; text-align: center; margin-bottom: 1.5rem; }')
css_lines.append('.login-hero-title { font-family: "Playfair Display", serif; color: white; font-size: 2rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.02em; }')
css_lines.append('.login-hero-sub { font-family: "Lobster Two", cursive; font-style: italic; font-weight: 700; color: ' + BRAND_YELLOW + '; font-size: 1.3rem; margin-top: 0.2rem; }')
css_lines.append('.login-hero-year { display: inline-block; margin-top: 1rem; padding: 0.3rem 0.9rem; font-size: 0.7rem; letter-spacing: 0.3em; color: rgba(255,255,255,0.7); border: 1px solid rgba(255,222,89,0.5); border-radius: 999px; }')
css_lines.append('.user-chip { display: flex; align-items: center; gap: 0.8rem; background: ' + BRAND_BLUE_LIGHT + '; border-radius: 999px; padding: 0.4rem 1rem 0.4rem 0.4rem; width: fit-content; margin-bottom: 1rem; }')
css_lines.append('.chip-name { font-weight: 700; color: ' + BRAND_BLUE + '; }')
css_lines.append('.section-title-home { font-family: "Playfair Display", serif; color: ' + BRAND_BLUE + '; font-size: 1.6rem; font-weight: 800; margin: 1rem 0 0.3rem; }')
css_lines.append('.section-sub-home { font-family: "Lobster Two", cursive; font-style: italic; font-weight: 700; color: ' + BRAND_YELLOW + '; font-size: 1.05rem; margin-bottom: 1rem; }')
css_lines.append('.eye-card { background: white; border: 1px solid rgba(19,0,137,0.08); border-radius: 18px; padding: 1rem; text-align: center; box-shadow: 0 4px 16px rgba(19,0,137,0.06); }')
css_lines.append('.eye-card-name { font-family: "Playfair Display", serif; font-weight: 800; color: ' + BRAND_BLUE + '; font-size: 0.95rem; margin-top: 0.5rem; }')
css_lines.append('</style>')

st.markdown("\n".join(css_lines), unsafe_allow_html=True)


# ==================== STATE ====================
if "username" not in st.session_state:
    st.session_state.username = None
if "view" not in st.session_state:
    st.session_state.view = "home"


st.markdown('<div class="proto-banner">Prototipo v9 - simboli ridisegnati, colline/luna rimossi.</div>', unsafe_allow_html=True)


db = load_db()


# ==================== LOGIN ====================
if st.session_state.username is None:
    login_hero = '<div class="login-hero"><div class="login-hero-title">Peccioli Eyes</div><div class="login-hero-sub">to New Orleans</div><div class="login-hero-year">2026</div><p style="color:rgba(255,255,255,0.85);margin-top:1.5rem;font-size:0.95rem;max-width:420px;margin-left:auto;margin-right:auto;line-height:1.6;">Crea il tuo sguardo personale. Scegli un nome e una password che ricorderai.</p></div>'
    st.markdown(login_hero, unsafe_allow_html=True)

    tab_login, tab_new = st.tabs(["Ho gia un profilo", "Creane uno nuovo"])

    with tab_login:
        c1, c2 = st.columns(2)
        with c1:
            login_user = st.text_input("Nome", key="login_user", placeholder="Il tuo nome")
        with c2:
            login_pwd = st.text_input("Password", type="password", key="login_pwd", placeholder="La tua password")
        if st.button("Entra", key="btn_login", use_container_width=True):
            u = (login_user or "").strip().lower()
            if not u:
                st.error("Inserisci il tuo nome")
            elif u not in db:
                st.error("Non esiste un profilo con il nome '" + str(login_user) + "'.")
            elif db[u].get("password") != login_pwd:
                st.error("Password sbagliata.")
            else:
                st.session_state.username = u
                for k in list(st.session_state.keys()):
                    if k.startswith("w_") or k.startswith("__"):
                        del st.session_state[k]
                st.rerun()

    with tab_new:
        c1, c2 = st.columns(2)
        with c1:
            new_user = st.text_input("Scegli un nome", key="new_user", placeholder="Es. marco...")
        with c2:
            new_pwd = st.text_input("Inventa una password", type="password", key="new_pwd")
        st.caption("Il nome sara visibile agli altri nella galleria.")
        if st.button("Crea il mio profilo", key="btn_new", use_container_width=True):
            u = (new_user or "").strip().lower()
            if not u:
                st.error("Scegli un nome")
            elif len(u) < 2:
                st.error("Il nome deve avere almeno 2 caratteri")
            elif not new_pwd or len(new_pwd) < 3:
                st.error("La password deve avere almeno 3 caratteri")
            elif u in db:
                st.error("Un profilo con questo nome esiste gia.")
            else:
                db[u] = {
                    "display_name": new_user.strip(),
                    "password": new_pwd,
                    "avatar": DEFAULT_AVATAR.copy(),
                    "created_at": datetime.now().isoformat(timespec="seconds"),
                    "visible_in_gallery": True,
                }
                save_db(db)
                st.session_state.username = u
                st.session_state.view = "editor"
                for k in list(st.session_state.keys()):
                    if k.startswith("w_") or k.startswith("__"):
                        del st.session_state[k]
                st.success("Profilo creato!")
                st.rerun()

    st.stop()


# ==================== LOGGATO ====================
user = db[st.session_state.username]
avatar = user["avatar"]
if "brow" in avatar:
    del avatar["brow"]
if "symbol_color" not in avatar:
    avatar["symbol_color"] = "#130089"
if "lashes_color" not in avatar:
    avatar["lashes_color"] = "#1a1a1a"
if "border_color" not in avatar:
    avatar["border_color"] = "#ffffff"
# Migrazioni legacy: rimappa simboli vecchi/rimossi
if avatar.get("symbol") == "torre_peccioli":
    avatar["symbol"] = "campanile_peccioli"
if avatar.get("symbol") in ("collina", "moon"):
    avatar["symbol"] = "trumpet"
# Migrazioni legacy: rimappa sfondi rimossi
if avatar.get("bg") == "stars":
    avatar["bg"] = "nola_jazz"
if avatar.get("bg") == "nola_skyline":
    avatar["bg"] = "sunset_mississippi"

display_name = user["display_name"]


col_chip, col_nav = st.columns([2, 3])
with col_chip:
    chip_svg = eye_svg(avatar, size=40)
    st.markdown('<div class="user-chip">' + chip_svg + '<span class="chip-name">Ciao, ' + display_name + '</span></div>', unsafe_allow_html=True)

with col_nav:
    nav_cols = st.columns(4)
    with nav_cols[0]:
        if st.button("Home", key="nav_home", use_container_width=True):
            st.session_state.view = "home"
            st.rerun()
    with nav_cols[1]:
        if st.button("Sguardo", key="nav_editor", use_container_width=True):
            st.session_state.view = "editor"
            st.rerun()
    with nav_cols[2]:
        if st.button("Galleria", key="nav_gallery", use_container_width=True):
            st.session_state.view = "gallery"
            st.rerun()
    with nav_cols[3]:
        if st.button("Esci", key="nav_logout", use_container_width=True):
            st.session_state.username = None
            st.session_state.view = "home"
            for k in list(st.session_state.keys()):
                if k.startswith("w_") or k.startswith("__"):
                    del st.session_state[k]
            st.rerun()

st.markdown("---")


# ==================== HOME ====================
if st.session_state.view == "home":
    c1, c2 = st.columns([1, 1.2])
    with c1:
        big_svg = eye_svg(avatar, size=280)
        home_card = '<div style="background:' + BRAND_BLUE_LIGHT + ';border-radius:24px;padding:1.5rem;text-align:center;">' + big_svg + '<div style="margin-top:0.8rem;font-family:\'Lobster Two\',cursive;font-style:italic;font-size:1.3rem;color:' + BRAND_BLUE + ';">Il tuo sguardo</div></div>'
        st.markdown(home_card, unsafe_allow_html=True)
    with c2:
        home_text = '<div class="section-title-home">Ciao, ' + display_name + '</div><div class="section-sub-home">Benvenuto nel tuo portale</div><p style="color:#3a4a5c;line-height:1.7;font-size:0.95rem;">Questo e il tuo spazio personale dentro <strong>Peccioli Eyes</strong>. Il tuo sguardo e unico e ti rappresenta nel viaggio verso New Orleans.</p>'
        st.markdown(home_text, unsafe_allow_html=True)

        total_users = len(db)
        stats_card = '<div style="background:white;border:1px solid rgba(19,0,137,0.1);border-radius:16px;padding:1rem 1.2rem;margin-top:1rem;"><div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:' + BRAND_BLUE + ';font-weight:700;opacity:0.7;">Sguardi creati finora</div><div style="font-family:\'Playfair Display\',serif;font-size:2rem;font-weight:800;color:' + BRAND_BLUE + ';">' + str(total_users) + '</div></div>'
        st.markdown(stats_card, unsafe_allow_html=True)


# ==================== EDITOR ====================
elif st.session_state.view == "editor":
    st.markdown('<div class="section-title-home">Crea il tuo sguardo</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub-home">Ogni dettaglio racconta chi sei</div>', unsafe_allow_html=True)

    for key, default in [("w_shape", avatar["shape"]), ("w_iris", avatar["iris"]),
                          ("w_symbol", avatar["symbol"]),
                          ("w_symbol_color", avatar.get("symbol_color", "#130089")),
                          ("w_lashes", avatar["lashes"]),
                          ("w_lashes_color", avatar.get("lashes_color", "#1a1a1a")),
                          ("w_bg", avatar["bg"]),
                          ("w_border_color", avatar.get("border_color", "#ffffff"))]:
        if key not in st.session_state:
            st.session_state[key] = default

    if "w_symbol_cat" not in st.session_state:
        current_sym_obj = next((s for s in SYMBOLS if s["id"] == st.session_state.w_symbol), SYMBOLS[0])
        st.session_state.w_symbol_cat = current_sym_obj["category"]

    live_avatar = {
        "shape": st.session_state.w_shape,
        "iris": st.session_state.w_iris,
        "symbol": st.session_state.w_symbol,
        "symbol_color": st.session_state.w_symbol_color,
        "lashes": st.session_state.w_lashes,
        "lashes_color": st.session_state.w_lashes_color,
        "bg": st.session_state.w_bg,
        "border_color": st.session_state.w_border_color,
    }

    c_preview, c_controls = st.columns([1, 1.3])

    with c_preview:
        preview_svg = eye_svg(live_avatar, size=300)
        preview_card = '<div style="background:' + BRAND_BLUE_LIGHT + ';border-radius:20px;padding:1.5rem;text-align:center;">' + preview_svg + '<div style="margin-top:0.8rem;font-size:0.85rem;color:' + BRAND_BLUE + ';font-weight:500;">Anteprima dal vivo</div></div>'
        st.markdown(preview_card, unsafe_allow_html=True)

        if st.button("Sguardo casuale", use_container_width=True, key="randomize"):
            st.session_state.w_shape = random.choice(SHAPES)["id"]
            st.session_state.w_iris = random.choice([c[1] for c in COLORS if c[1] != "#ffffff"])
            rand_sym = random.choice(SYMBOLS)
            st.session_state.w_symbol = rand_sym["id"]
            st.session_state.w_symbol_cat = rand_sym["category"]
            st.session_state.w_symbol_color = random.choice([c[1] for c in COLORS])
            st.session_state.w_lashes = random.choice(LASHES)["id"]
            st.session_state.w_lashes_color = random.choice([c[1] for c in COLORS])
            st.session_state.w_bg = random.choice(BACKGROUNDS)["id"]
            st.session_state.w_border_color = random.choice([c[1] for c in COLORS])
            st.rerun()

        st.caption("Clicca su **Salva** per rendere permanenti le scelte.")

    with c_controls:
        st.markdown("**Forma dell'occhio**")
        shape_labels = [s["label"] for s in SHAPES]
        shape_ids = [s["id"] for s in SHAPES]
        current_shape_idx = shape_ids.index(st.session_state.w_shape) if st.session_state.w_shape in shape_ids else 0
        new_shape_label = st.radio("Forma", shape_labels, index=current_shape_idx, horizontal=True, label_visibility="collapsed", key="__rd_shape")
        _new_shape = shape_ids[shape_labels.index(new_shape_label)]
        if _new_shape != st.session_state.w_shape:
            st.session_state.w_shape = _new_shape
            st.rerun()

        st.markdown("**Colore bordo dell'occhio**")
        color_labels = [c[0] for c in COLORS]
        color_values = [c[1] for c in COLORS]
        current_border_idx = color_values.index(st.session_state.w_border_color) if st.session_state.w_border_color in color_values else 11
        new_border_label = st.selectbox("Bordo", color_labels, index=current_border_idx, label_visibility="collapsed", key="__sb_border")
        _new_border = color_values[color_labels.index(new_border_label)]
        if _new_border != st.session_state.w_border_color:
            st.session_state.w_border_color = _new_border
            st.rerun()

        st.markdown("**Colore iride**")
        current_iris_idx = color_values.index(st.session_state.w_iris) if st.session_state.w_iris in color_values else 0
        new_iris_label = st.selectbox("Iride", color_labels, index=current_iris_idx, label_visibility="collapsed", key="__sb_iris")
        _new_iris = color_values[color_labels.index(new_iris_label)]
        if _new_iris != st.session_state.w_iris:
            st.session_state.w_iris = _new_iris
            st.rerun()

        st.markdown("**Simbolo nella pupilla**")
        cat_labels = [c[1] for c in SYMBOL_CATEGORIES]
        cat_ids = [c[0] for c in SYMBOL_CATEGORIES]
        current_cat_idx = cat_ids.index(st.session_state.w_symbol_cat) if st.session_state.w_symbol_cat in cat_ids else 0
        selected_cat_label = st.radio("Categoria", cat_labels, index=current_cat_idx, horizontal=True, label_visibility="collapsed", key="__rd_cat")
        _new_cat = cat_ids[cat_labels.index(selected_cat_label)]
        if _new_cat != st.session_state.w_symbol_cat:
            st.session_state.w_symbol_cat = _new_cat
            cat_syms = [s for s in SYMBOLS if s["category"] == _new_cat]
            if cat_syms:
                st.session_state.w_symbol = cat_syms[0]["id"]
            st.rerun()

        cat_symbols = [s for s in SYMBOLS if s["category"] == st.session_state.w_symbol_cat]
        sym_labels = [s["label"] for s in cat_symbols]
        sym_ids = [s["id"] for s in cat_symbols]
        if st.session_state.w_symbol not in sym_ids:
            st.session_state.w_symbol = sym_ids[0]
        current_sym_idx = sym_ids.index(st.session_state.w_symbol)
        new_sym_label = st.radio("Simbolo", sym_labels, index=current_sym_idx, label_visibility="collapsed", key="__rd_sym_" + st.session_state.w_symbol_cat)
        _new_sym = sym_ids[sym_labels.index(new_sym_label)]
        if _new_sym != st.session_state.w_symbol:
            st.session_state.w_symbol = _new_sym
            st.rerun()

        st.markdown("**Colore del simbolo**")
        current_symcol_idx = color_values.index(st.session_state.w_symbol_color) if st.session_state.w_symbol_color in color_values else 1
        new_symcol_label = st.selectbox("Colore simbolo", color_labels, index=current_symcol_idx, label_visibility="collapsed", key="__sb_symcol")
        _new_symcol = color_values[color_labels.index(new_symcol_label)]
        if _new_symcol != st.session_state.w_symbol_color:
            st.session_state.w_symbol_color = _new_symcol
            st.rerun()

        st.markdown("**Ciglia**")
        lash_labels = [l["label"] for l in LASHES]
        lash_ids = [l["id"] for l in LASHES]
        current_lash_idx = lash_ids.index(st.session_state.w_lashes) if st.session_state.w_lashes in lash_ids else 0
        new_lash_label = st.radio("Stile ciglia", lash_labels, index=current_lash_idx, horizontal=True, label_visibility="collapsed", key="__rd_lashes")
        _new_lash = lash_ids[lash_labels.index(new_lash_label)]
        if _new_lash != st.session_state.w_lashes:
            st.session_state.w_lashes = _new_lash
            st.rerun()

        st.markdown("**Colore delle ciglia**")
        current_lashcol_idx = color_values.index(st.session_state.w_lashes_color) if st.session_state.w_lashes_color in color_values else 10
        new_lashcol_label = st.selectbox("Colore ciglia", color_labels, index=current_lashcol_idx, label_visibility="collapsed", key="__sb_lashcol")
        _new_lashcol = color_values[color_labels.index(new_lashcol_label)]
        if _new_lashcol != st.session_state.w_lashes_color:
            st.session_state.w_lashes_color = _new_lashcol
            st.rerun()

        st.markdown("**Sfondo**")
        bg_labels = [b["label"] for b in BACKGROUNDS]
        bg_ids = [b["id"] for b in BACKGROUNDS]
        current_bg_idx = bg_ids.index(st.session_state.w_bg) if st.session_state.w_bg in bg_ids else 0
        new_bg_label = st.selectbox("Sfondo", bg_labels, index=current_bg_idx, label_visibility="collapsed", key="__sb_bg")
        _new_bg = bg_ids[bg_labels.index(new_bg_label)]
        if _new_bg != st.session_state.w_bg:
            st.session_state.w_bg = _new_bg
            st.rerun()

        st.markdown("---")
        st.markdown("**Privacy**")
        visible = st.checkbox("Mostra il mio sguardo nella galleria pubblica", value=user.get("visible_in_gallery", True), key="sel_visible")

        col_save, col_reset = st.columns([2, 1])
        with col_save:
            if st.button("Salva il mio sguardo", use_container_width=True, type="primary", key="btn_save_avatar"):
                db[st.session_state.username]["avatar"] = {
                    "shape": st.session_state.w_shape,
                    "iris": st.session_state.w_iris,
                    "symbol": st.session_state.w_symbol,
                    "symbol_color": st.session_state.w_symbol_color,
                    "lashes": st.session_state.w_lashes,
                    "lashes_color": st.session_state.w_lashes_color,
                    "bg": st.session_state.w_bg,
                    "border_color": st.session_state.w_border_color,
                }
                db[st.session_state.username]["visible_in_gallery"] = visible
                save_db(db)
                st.success("Sguardo salvato!")
                st.rerun()
        with col_reset:
            if st.button("Annulla", use_container_width=True, key="btn_reset_avatar"):
                for k in ["w_shape", "w_iris", "w_symbol_cat", "w_symbol", "w_symbol_color", "w_lashes", "w_lashes_color", "w_bg", "w_border_color"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()


# ==================== GALLERIA ====================
elif st.session_state.view == "gallery":
    st.markdown('<div class="section-title-home">Gli sguardi di Peccioli</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub-home">Ogni ragazzo, un occhio</div>', unsafe_allow_html=True)

    visible_users = [(uname, u) for uname, u in db.items() if u.get("visible_in_gallery", True)]
    st.caption(str(len(visible_users)) + " sguardi in galleria - " + str(len(db)) + " profili totali")

    if not visible_users:
        st.info("Ancora nessuno sguardo pubblico in galleria.")
    else:
        cols_per_row = 4
        for i in range(0, len(visible_users), cols_per_row):
            row = visible_users[i:i + cols_per_row]
            cols = st.columns(cols_per_row)
            for col, (uname, u) in zip(cols, row):
                with col:
                    svg = eye_svg(u["avatar"], size=140)
                    is_me = uname == st.session_state.username
                    if is_me:
                        border_color = BRAND_YELLOW
                        border_width = "3px"
                        me_badge = '<div style="display:inline-block;background:' + BRAND_YELLOW + ';color:' + BRAND_BLUE + ';font-size:0.65rem;font-weight:700;padding:0.1rem 0.5rem;border-radius:999px;margin-top:0.3rem;">SEI TU</div>'
                    else:
                        border_color = "rgba(19,0,137,0.08)"
                        border_width = "1px"
                        me_badge = ""
                    card = '<div class="eye-card" style="border:' + border_width + ' solid ' + border_color + ';">' + svg + '<div class="eye-card-name">' + u["display_name"] + '</div>' + me_badge + '</div>'
                    st.markdown(card, unsafe_allow_html=True)

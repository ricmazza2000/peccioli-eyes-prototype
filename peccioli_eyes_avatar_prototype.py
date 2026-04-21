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

SYMBOLS = [
    {"id": "campanile_peccioli", "label": "Campanile di Peccioli", "category": "peccioli"},
    {"id": "cipresso", "label": "Cipresso toscano", "category": "peccioli"},
    {"id": "collina", "label": "Colline", "category": "peccioli"},
    {"id": "uliva", "label": "Olivo", "category": "peccioli"},

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
    {"id": "moon", "label": "Luna", "category": "astratti"},
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
    {"id": "stars", "label": "Cielo stellato", "color": BRAND_BLUE_DARK},
    {"id": "nola_skyline", "label": "Skyline New Orleans", "color": "#1a2f6c"},
    {"id": "nola_jazz", "label": "Jazz notturno", "color": "#2a0a3a"},
    {"id": "peccioli_hills", "label": "Colline Peccioli", "color": "#2ea36a"},
    {"id": "peccioli_tower", "label": "Campanile di Peccioli", "color": "#f5d896"},
    {"id": "sunset_mississippi", "label": "Tramonto Mississippi", "color": "#c84a1e"},
    {"id": "mardigras", "label": "Mardi Gras", "color": "#4a1a5a"},
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
    """Simboli dentro la pupilla bianca. Disegnati a dimensione "nativa" (raggio ~10)."""

    # PECCIOLI ==================================================
    if sym_id == "campanile_peccioli":
        # Campanile di Peccioli: torre slanciata ottagonale con ordini di bifore sovrapposti
        # e copertura conica a punta (come nella foto reale)
        parts = []
        parts.append('<g transform="translate(100 100)">')
        # Base più larga (plinto)
        parts.append('<rect x="-5" y="9" width="10" height="2" fill="' + color + '"/>')
        # Corpo principale slanciato (leggermente rastremato verso l'alto)
        parts.append('<polygon points="-4.5,9 4.5,9 4,2 -4,2" fill="' + color + '"/>')
        # Divisorio tra primo ordine
        parts.append('<rect x="-4.3" y="1" width="8.6" height="1" fill="white"/>')
        # Secondo ordine (bifora - due finestre ad arco)
        parts.append('<polygon points="-4,0 4,0 3.5,-5 -3.5,-5" fill="' + color + '"/>')
        # Bifora nel secondo ordine (due aperture)
        parts.append('<path d="M -2.5 -1 L -2.5 -3.5 Q -1.5 -4.5 -0.5 -3.5 L -0.5 -1 Z" fill="white"/>')
        parts.append('<path d="M 0.5 -1 L 0.5 -3.5 Q 1.5 -4.5 2.5 -3.5 L 2.5 -1 Z" fill="white"/>')
        # Divisorio
        parts.append('<rect x="-3.8" y="-6" width="7.6" height="1" fill="white"/>')
        # Terzo ordine (trifora stilizzata con 3 aperture piccole)
        parts.append('<polygon points="-3.5,-7 3.5,-7 3,-11 -3,-11" fill="' + color + '"/>')
        parts.append('<rect x="-2.5" y="-9.5" width="1.2" height="2" fill="white"/>')
        parts.append('<rect x="-0.6" y="-10" width="1.2" height="2.5" fill="white"/>')
        parts.append('<rect x="1.3" y="-9.5" width="1.2" height="2" fill="white"/>')
        # Copertura conica a punta (tetto spiovente)
        parts.append('<polygon points="-3,-11 3,-11 0,-16" fill="' + color + '"/>')
        # Cuspide finale
        parts.append('<circle cx="0" cy="-16" r="0.6" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "cipresso":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M 0 -9 Q 3 -6 3 -3 Q 4 0 3 3 Q 4 5 2 7 L -2 7 Q -4 5 -3 3 Q -4 0 -3 -3 Q -3 -6 0 -9 Z" fill="' + color + '"/>')
        parts.append('<rect x="-0.8" y="7" width="1.6" height="3" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "collina":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<circle cx="5" cy="-6" r="2.5" fill="' + color + '"/>')
        parts.append('<path d="M -10 4 Q -5 -2 0 2 Q 4 -3 10 4 Z" fill="' + color + '" opacity="0.5"/>')
        parts.append('<path d="M -11 7 Q -5 1 -1 4 Q 3 0 9 7 Z" fill="' + color + '" opacity="0.75"/>')
        parts.append('<path d="M -12 10 Q -6 5 0 8 Q 6 4 12 10 Z" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "uliva":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M -10 3 Q 0 -1 10 3" fill="none" stroke="' + color + '" stroke-width="1.3" stroke-linecap="round"/>')
        parts.append('<ellipse cx="-6" cy="0" rx="2.8" ry="1.2" fill="' + color + '" transform="rotate(-25 -6 0)"/>')
        parts.append('<ellipse cx="-2" cy="-2" rx="3" ry="1.3" fill="' + color + '" transform="rotate(-15 -2 -2)"/>')
        parts.append('<ellipse cx="2" cy="-2" rx="3" ry="1.3" fill="' + color + '" transform="rotate(15 2 -2)"/>')
        parts.append('<ellipse cx="6" cy="0" rx="2.8" ry="1.2" fill="' + color + '" transform="rotate(25 6 0)"/>')
        parts.append('<circle cx="-3" cy="2" r="1.2" fill="' + color + '"/>')
        parts.append('<circle cx="3" cy="2" r="1.2" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    # NEW ORLEANS ==================================================
    if sym_id == "trumpet":
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
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M -10 -5 L -10 6 L 0 4 L 0 -4 Z" fill="' + color + '"/>')
        parts.append('<path d="M 10 -5 L 10 6 L 0 4 L 0 -4 Z" fill="' + color + '"/>')
        parts.append('<line x1="-8" y1="-2" x2="-2" y2="-2.6" stroke="white" stroke-width="0.6"/>')
        parts.append('<line x1="-8" y1="0" x2="-2" y2="-0.6" stroke="white" stroke-width="0.6"/>')
        parts.append('<line x1="-8" y1="2" x2="-2" y2="1.4" stroke="white" stroke-width="0.6"/>')
        parts.append('<line x1="2" y1="-2.6" x2="8" y2="-2" stroke="white" stroke-width="0.6"/>')
        parts.append('<line x1="2" y1="-0.6" x2="8" y2="0" stroke="white" stroke-width="0.6"/>')
        parts.append('<line x1="2" y1="1.4" x2="8" y2="2" stroke="white" stroke-width="0.6"/>')
        parts.append('<line x1="0" y1="-4" x2="0" y2="4" stroke="' + color + '" stroke-width="0.8"/>')
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

    if sym_id == "moon":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M -2 -9 A 9 9 0 1 0 -2 9 A 6.5 6.5 0 1 1 -2 -9 Z" fill="' + color + '"/>')
        parts.append('<polygon points="6,-4 6.8,-2 9,-2 7.2,-0.7 7.8,1.5 6,0.3 4.2,1.5 4.8,-0.7 3,-2 5.2,-2" fill="' + color + '" opacity="0.8"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "lightning":
        parts = []
        parts.append('<g transform="translate(100 100)">')
        parts.append('<polygon points="-2,-10 5,-2 1,-2 4,10 -5,0 -1,0 -4,-10" fill="' + color + '"/>')
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

    if bg_id == "stars":
        stars = [(30,40),(160,35),(50,160),(170,140),(100,30),(25,110),(175,80),(90,170),(130,60),(60,80),(150,170),(20,70)]
        for sx, sy in stars:
            out.append('<circle cx="' + str(sx) + '" cy="' + str(sy) + '" r="1.3" fill="' + BRAND_YELLOW + '"/>')
        out.append('<circle cx="165" cy="40" r="10" fill="' + BRAND_YELLOW + '" opacity="0.85"/>')

    elif bg_id == "nola_skyline":
        out.append('<rect y="0" width="200" height="130" fill="#1a2f6c"/>')
        out.append('<rect y="130" width="200" height="70" fill="#0a1548"/>')
        out.append('<circle cx="30" cy="30" r="1" fill="white" opacity="0.9"/>')
        out.append('<circle cx="80" cy="20" r="1.2" fill="white" opacity="0.9"/>')
        out.append('<circle cx="150" cy="40" r="1" fill="white" opacity="0.8"/>')
        out.append('<polygon points="0,200 0,150 15,145 25,130 40,135 55,120 70,125 85,105 100,115 115,100 130,110 145,90 160,105 175,95 190,100 200,90 200,200" fill="#05082a"/>')
        out.append('<rect x="25" y="140" width="1.5" height="2" fill="' + BRAND_YELLOW + '"/>')
        out.append('<rect x="70" y="135" width="1.5" height="2" fill="' + BRAND_YELLOW + '"/>')
        out.append('<rect x="115" y="115" width="1.5" height="2" fill="' + BRAND_YELLOW + '"/>')
        out.append('<rect x="135" y="120" width="1.5" height="2" fill="' + BRAND_YELLOW + '"/>')
        out.append('<rect x="165" y="110" width="1.5" height="2" fill="' + BRAND_YELLOW + '"/>')

    elif bg_id == "nola_jazz":
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

    elif bg_id == "peccioli_tower":
        # Sfondo: cielo azzurro chiaro con silhouette del campanile di Peccioli stilizzata
        out.append('<rect y="0" width="200" height="160" fill="#b8dcf0"/>')
        out.append('<rect y="160" width="200" height="40" fill="#d4b888"/>')
        # Campanile silhouette in scala grande
        out.append('<g opacity="0.35" fill="#8b6914">')
        # Corpo slanciato
        out.append('<polygon points="85,160 115,160 112,100 88,100"/>')
        # Secondo ordine
        out.append('<polygon points="86,99 114,99 111,65 89,65"/>')
        # Finestre ad arco scure
        out.append('<path d="M 93 90 L 93 78 Q 96 74 99 78 L 99 90 Z" fill="#6b4d0a"/>')
        out.append('<path d="M 101 90 L 101 78 Q 104 74 107 78 L 107 90 Z" fill="#6b4d0a"/>')
        # Terzo ordine
        out.append('<polygon points="88,64 112,64 110,35 90,35"/>')
        # Tetto conico
        out.append('<polygon points="87,34 113,34 100,10"/>')
        out.append('</g>')
        # Cielo sopra - qualche nuvola
        out.append('<ellipse cx="40" cy="30" rx="12" ry="4" fill="white" opacity="0.6"/>')
        out.append('<ellipse cx="170" cy="45" rx="10" ry="3" fill="white" opacity="0.55"/>')

    elif bg_id == "sunset_mississippi":
        out.append('<rect y="0" width="200" height="80" fill="#ff7e4a"/>')
        out.append('<rect y="80" width="200" height="30" fill="#ffa07a"/>')
        out.append('<circle cx="100" cy="110" r="22" fill="' + BRAND_YELLOW + '" opacity="0.95"/>')
        out.append('<rect y="110" width="200" height="90" fill="#8b4513"/>')
        out.append('<rect y="115" width="200" height="3" fill="' + BRAND_YELLOW + '" opacity="0.4"/>')
        out.append('<rect y="130" width="200" height="2" fill="' + BRAND_YELLOW + '" opacity="0.3"/>')
        out.append('<rect y="145" width="200" height="2" fill="' + BRAND_YELLOW + '" opacity="0.2"/>')
        out.append('<g fill="#2a1a0a">')
        out.append('<rect x="35" y="100" width="25" height="6"/>')
        out.append('<rect x="40" y="95" width="15" height="5"/>')
        out.append('<rect x="44" y="88" width="2" height="8"/>')
        out.append('<rect x="49" y="88" width="2" height="8"/>')
        out.append('</g>')

    elif bg_id == "mardigras":
        out.append('<rect width="200" height="200" fill="#4a1a5a"/>')
        confetti = [
            (25, 30, "#2ea36a"), (60, 50, "#FFDE59"), (140, 25, "#7a3fb8"),
            (170, 60, "#2ea36a"), (30, 90, "#FFDE59"), (90, 110, "#7a3fb8"),
            (160, 100, "#FFDE59"), (40, 140, "#2ea36a"), (110, 160, "#FFDE59"),
            (170, 155, "#2ea36a"), (50, 175, "#7a3fb8"), (135, 180, "#FFDE59"),
        ]
        for cx, cy, col in confetti:
            out.append('<polygon points="' + str(cx) + ',' + str(cy-3) + ' ' + str(cx+3) + ',' + str(cy) + ' ' + str(cx) + ',' + str(cy+3) + ' ' + str(cx-3) + ',' + str(cy) + '" fill="' + col + '" opacity="0.75"/>')
        out.append('<path d="M -10 70 Q 100 55 210 70" fill="none" stroke="#FFDE59" stroke-width="1" opacity="0.5" stroke-dasharray="2,3"/>')
        out.append('<path d="M -10 130 Q 100 115 210 130" fill="none" stroke="#2ea36a" stroke-width="1" opacity="0.5" stroke-dasharray="2,3"/>')

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

    # Il colore bordo occhio ora e' personalizzabile
    stroke_color = params.get("border_color", "#ffffff")

    if params["bg"] == "white-solid":
        sclera_color = "#f4f1e8"
    else:
        sclera_color = "white"

    sym_color = params.get("symbol_color", "#130089")
    lash_color = params.get("lashes_color", "#1a1a1a")

    content = params["shape"] + params["iris"] + params["symbol"] + sym_color + params["bg"] + params["lashes"] + lash_color + stroke_color
    clip_id = "eye-clip-" + hashlib.md5(content.encode()).hexdigest()[:8]

    # Pupilla leggermente piu' piccola (0.65 invece di 0.7)
    pupil_radius = iris_radius * 0.65

    parts = []
    parts.append('<svg viewBox="0 0 200 200" width="' + str(size) + '" height="' + str(size) + '" xmlns="http://www.w3.org/2000/svg">')
    parts.append('<defs><clipPath id="' + clip_id + '"><path d="' + eye_d + '"/></clipPath></defs>')
    parts.append(render_background(params["bg"]))
    parts.append('<path d="' + eye_d + '" fill="' + sclera_color + '" stroke="' + stroke_color + '" stroke-width="3"/>')
    parts.append('<g clip-path="url(#' + clip_id + ')">')
    parts.append('<circle cx="100" cy="100" r="' + str(iris_radius) + '" fill="' + params["iris"] + '"/>')
    parts.append('<circle cx="100" cy="100" r="' + str(pupil_radius) + '" fill="white"/>')
    # Scala simbolo per riempire bene la pupilla senza essere eccessivo
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


st.markdown('<div class="proto-banner">Prototipo v8 - simbolo ridimensionato, campanile ridisegnato, colore bordo personalizzabile.</div>', unsafe_allow_html=True)


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
# Migra il vecchio id simbolo torre_peccioli al nuovo campanile_peccioli
if avatar.get("symbol") == "torre_peccioli":
    avatar["symbol"] = "campanile_peccioli"

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

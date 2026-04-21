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

IRIS_COLORS = [
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
]

SYMBOLS = [
    {"id": "torre_peccioli", "label": "Torre di Peccioli", "category": "peccioli"},
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

BROWS = [
    {"id": "none", "label": "Nessuno"},
    {"id": "straight", "label": "Diritto"},
    {"id": "arched", "label": "Arcuato"},
    {"id": "thick", "label": "Spesso"},
    {"id": "questioning", "label": "Interrogativo"},
]

BACKGROUNDS = [
    {"id": "blue-solid", "label": "Blu brand", "color": BRAND_BLUE},
    {"id": "yellow-solid", "label": "Giallo brand", "color": BRAND_YELLOW},
    {"id": "white-solid", "label": "Avorio", "color": "#fafafa"},
    {"id": "stars", "label": "Stelle", "color": BRAND_BLUE_DARK},
    {"id": "sunset", "label": "Tramonto NOLA", "color": "#c84a1e"},
    {"id": "peccioli", "label": "Colline Peccioli", "color": "#2ea36a"},
]

DEFAULT_AVATAR = {
    "shape": "almond",
    "iris": "#FFDE59",
    "symbol": "trumpet",
    "lashes": "classic",
    "brow": "none",
    "bg": "blue-solid",
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
    """Simboli piccoli (scala ~0.6) posizionati nell'iride colorata,
    sopra la pupilla. Centrati su (100, 87) per stare nella metà superiore
    dell'iride invece che sovrapposti alla pupilla nera."""
    cy = 88
    if sym_id == "torre_peccioli":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<rect x="-5" y="-10" width="10" height="18" fill="' + color + '"/>')
        parts.append('<polygon points="-7,-10 0,-16 7,-10" fill="' + color + '"/>')
        parts.append('<rect x="-2" y="-6" width="1.5" height="3" fill="#0a0a0a"/>')
        parts.append('<rect x="0.5" y="-6" width="1.5" height="3" fill="#0a0a0a"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "cipresso":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<ellipse cx="0" cy="-2" rx="4" ry="10" fill="' + color + '"/>')
        parts.append('<rect x="-0.8" y="7" width="1.6" height="4" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "collina":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<path d="M -12 6 Q -6 -4 0 2 Q 6 -6 12 6 Z" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "uliva":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<ellipse cx="0" cy="0" rx="8" ry="4" fill="' + color + '"/>')
        parts.append('<path d="M -8 0 Q 0 -5 8 0" fill="none" stroke="' + color + '" stroke-width="1.5"/>')
        parts.append('<ellipse cx="-5" cy="-2" rx="2" ry="1" fill="' + color + '"/>')
        parts.append('<ellipse cx="0" cy="-3" rx="2" ry="1" fill="' + color + '"/>')
        parts.append('<ellipse cx="5" cy="-2" rx="2" ry="1" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "trumpet":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<path d="M -10 -3 L -4 -5 L -4 5 L -10 3 Z" fill="' + color + '"/>')
        parts.append('<rect x="-4" y="-2" width="9" height="4" fill="' + color + '"/>')
        parts.append('<circle cx="8" cy="0" r="4.5" fill="none" stroke="' + color + '" stroke-width="1.8"/>')
        parts.append('<circle cx="-2" cy="-6" r="1" fill="' + color + '"/>')
        parts.append('<circle cx="1" cy="-6" r="1" fill="' + color + '"/>')
        parts.append('<circle cx="4" cy="-6" r="1" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "mask":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<path d="M -10 -2 Q -10 -6 -6 -7 Q 0 -8 6 -7 Q 10 -6 10 -2 Q 10 4 0 6 Q -10 4 -10 -2 Z" fill="' + color + '"/>')
        parts.append('<ellipse cx="-4" cy="-1" rx="2" ry="2" fill="white"/>')
        parts.append('<ellipse cx="4" cy="-1" rx="2" ry="2" fill="white"/>')
        parts.append('<line x1="-10" y1="-4" x2="-14" y2="-8" stroke="' + color + '" stroke-width="1.5"/>')
        parts.append('<line x1="10" y1="-4" x2="14" y2="-8" stroke="' + color + '" stroke-width="1.5"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "fleur":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<path d="M 0 -9 Q -4 -4 -2 0 Q -4 4 0 9 Q 4 4 2 0 Q 4 -4 0 -9 Z" fill="' + color + '"/>')
        parts.append('<path d="M -7 -2 Q -9 2 -4 7 Q 0 3 -2 0 Q -5 -5 -7 -2 Z" fill="' + color + '" opacity="0.85"/>')
        parts.append('<path d="M 7 -2 Q 9 2 4 7 Q 0 3 2 0 Q 5 -5 7 -2 Z" fill="' + color + '" opacity="0.85"/>')
        parts.append('<rect x="-6" y="-1" width="12" height="2" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "riverboat":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<path d="M -11 3 L 11 3 L 9 7 L -9 7 Z" fill="' + color + '"/>')
        parts.append('<rect x="-8" y="-2" width="16" height="5" fill="' + color + '"/>')
        parts.append('<rect x="-2" y="-8" width="2" height="6" fill="' + color + '"/>')
        parts.append('<rect x="2" y="-8" width="2" height="6" fill="' + color + '"/>')
        parts.append('<circle cx="7" cy="1" r="2.5" fill="none" stroke="white" stroke-width="1"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "balcony":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<rect x="-10" y="4" width="20" height="2" fill="' + color + '"/>')
        parts.append('<rect x="-10" y="-6" width="20" height="2" fill="' + color + '"/>')
        parts.append('<line x1="-8" y1="-4" x2="-8" y2="4" stroke="' + color + '" stroke-width="1"/>')
        parts.append('<line x1="-4" y1="-4" x2="-4" y2="4" stroke="' + color + '" stroke-width="1"/>')
        parts.append('<line x1="0" y1="-4" x2="0" y2="4" stroke="' + color + '" stroke-width="1"/>')
        parts.append('<line x1="4" y1="-4" x2="4" y2="4" stroke="' + color + '" stroke-width="1"/>')
        parts.append('<line x1="8" y1="-4" x2="8" y2="4" stroke="' + color + '" stroke-width="1"/>')
        parts.append('<path d="M -6 -4 Q -4 -2 -2 -4 M 2 -4 Q 4 -2 6 -4" fill="none" stroke="' + color + '" stroke-width="1"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "note":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<ellipse cx="-3" cy="6" rx="5" ry="3.5" fill="' + color + '" transform="rotate(-20 -3 6)"/>')
        parts.append('<rect x="1.5" y="-9" width="2" height="17" fill="' + color + '"/>')
        parts.append('<path d="M 3.5 -9 Q 11 -6 10 1.5" fill="none" stroke="' + color + '" stroke-width="2.2" stroke-linecap="round"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "wave":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<path d="M -11 -3 Q -5 -8 0 -3 Q 5 2 11 -3" fill="none" stroke="' + color + '" stroke-width="2.2" stroke-linecap="round"/>')
        parts.append('<path d="M -11 3 Q -5 -2 0 3 Q 5 8 11 3" fill="none" stroke="' + color + '" stroke-width="2.2" stroke-linecap="round"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "people":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<circle cx="-7" cy="-3" r="2.5" fill="' + color + '"/>')
        parts.append('<rect x="-9.5" y="0" width="5" height="6" rx="1" fill="' + color + '"/>')
        parts.append('<circle cx="0" cy="-5" r="3" fill="' + color + '"/>')
        parts.append('<rect x="-3" y="-2" width="6" height="8" rx="1" fill="' + color + '"/>')
        parts.append('<circle cx="7" cy="-3" r="2.5" fill="' + color + '"/>')
        parts.append('<rect x="4.5" y="0" width="5" height="6" rx="1" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "book":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<path d="M -9 -6 L 0 -4 L 9 -6 L 9 6 L 0 4 L -9 6 Z" fill="' + color + '"/>')
        parts.append('<line x1="0" y1="-4" x2="0" y2="4" stroke="white" stroke-width="0.8"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "star":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<polygon points="0,-10 3,-3 10,-3 4,2 6,9 0,5 -6,9 -4,2 -10,-3 -3,-3" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "heart":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<path d="M 0 8 C -10 0 -10 -8 -5 -8 C -2 -8 0 -5 0 -3 C 0 -5 2 -8 5 -8 C 10 -8 10 0 0 8 Z" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "eye_inside":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<path d="M -10 0 Q 0 -7 10 0 Q 0 7 -10 0 Z" fill="none" stroke="' + color + '" stroke-width="1.5"/>')
        parts.append('<circle cx="0" cy="0" r="3" fill="' + color + '"/>')
        parts.append('<circle cx="0" cy="0" r="1" fill="white"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "moon":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<path d="M -3 -8 A 8 8 0 1 0 -3 8 A 5 5 0 1 1 -3 -8 Z" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "lightning":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy) + ')">')
        parts.append('<polygon points="-2,-10 3,-2 -1,-2 2,10 -4,2 0,2" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    return ""


def render_lashes(shape, style):
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
        out.append('<line x1="' + str(x) + '" y1="' + str(top_y) + '" x2="' + str(x2) + '" y2="' + str(y2) + '" stroke="#1a1a1a" stroke-width="' + str(thick) + '" stroke-linecap="round"/>')
    return "".join(out)


def render_brow(shape, style):
    if style == "none":
        return ""
    if shape == "round":
        top_y = 28
    elif shape == "almond":
        top_y = 38
    elif shape == "wide":
        top_y = 28
    else:
        top_y = 55

    if style == "straight":
        return '<rect x="60" y="' + str(top_y) + '" width="80" height="4" fill="#1a1a1a" rx="2"/>'
    if style == "arched":
        return '<path d="M 60 ' + str(top_y + 3) + ' Q 100 ' + str(top_y - 6) + ' 140 ' + str(top_y + 3) + '" fill="none" stroke="#1a1a1a" stroke-width="4" stroke-linecap="round"/>'
    if style == "thick":
        return '<path d="M 55 ' + str(top_y + 3) + ' Q 100 ' + str(top_y - 4) + ' 145 ' + str(top_y + 3) + '" fill="none" stroke="#1a1a1a" stroke-width="7" stroke-linecap="round"/>'
    if style == "questioning":
        return '<path d="M 60 ' + str(top_y + 4) + ' Q 85 ' + str(top_y - 3) + ' 110 ' + str(top_y - 1) + ' Q 130 ' + str(top_y - 8) + ' 140 ' + str(top_y - 4) + '" fill="none" stroke="#1a1a1a" stroke-width="4" stroke-linecap="round"/>'
    return ""


def render_background(bg_id):
    bg = next((b for b in BACKGROUNDS if b["id"] == bg_id), BACKGROUNDS[0])
    out = ['<rect width="200" height="200" fill="' + bg["color"] + '"/>']
    if bg_id == "stars":
        stars = [(30,40),(160,35),(50,160),(170,140),(100,30),(25,110),(175,80),(90,170)]
        for sx, sy in stars:
            out.append('<circle cx="' + str(sx) + '" cy="' + str(sy) + '" r="1.5" fill="' + BRAND_YELLOW + '"/>')
    elif bg_id == "sunset":
        out.append('<rect width="200" height="100" fill="#ffa07a" opacity="0.6"/>')
        out.append('<circle cx="40" cy="40" r="15" fill="#ffdb4d" opacity="0.9"/>')
    elif bg_id == "peccioli":
        out.append('<path d="M 0 200 Q 50 150 100 170 Q 150 155 200 175 L 200 200 Z" fill="#1a7a4a" opacity="0.5"/>')
        out.append('<path d="M 0 200 Q 60 170 120 185 Q 160 175 200 190 L 200 200 Z" fill="#0d5530" opacity="0.6"/>')
    return "".join(out)


def contrast_on(hex_color):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    if lum > 0.6:
        return "#130089"
    return "#FFDE59"


@st.cache_data(show_spinner=False)
def build_eye_svg(params_tuple, size=240):
    """Cached render. params_tuple è una tupla hashable per permettere cache."""
    params = dict(params_tuple)
    eye_d = eye_path(params["shape"])

    if params["shape"] == "narrow":
        iris_radius = 22
    elif params["shape"] == "wide":
        iris_radius = 28
    else:
        iris_radius = 26

    if params["bg"] in ("yellow-solid", "white-solid"):
        stroke_color = BRAND_BLUE
    else:
        stroke_color = "white"

    if params["bg"] == "white-solid":
        sclera_color = "#f4f1e8"
    else:
        sclera_color = "white"

    symbol_color = contrast_on(params["iris"])

    # ID deterministico basato sul contenuto invece che random
    content = params["shape"] + params["iris"] + params["symbol"] + params["bg"]
    clip_id = "eye-clip-" + hashlib.md5(content.encode()).hexdigest()[:8]

    parts = []
    parts.append('<svg viewBox="0 0 200 200" width="' + str(size) + '" height="' + str(size) + '" xmlns="http://www.w3.org/2000/svg">')
    parts.append('<defs><clipPath id="' + clip_id + '"><path d="' + eye_d + '"/></clipPath></defs>')
    parts.append(render_background(params["bg"]))
    parts.append(render_brow(params["shape"], params.get("brow", "none")))
    parts.append('<path d="' + eye_d + '" fill="' + sclera_color + '" stroke="' + stroke_color + '" stroke-width="3"/>')
    parts.append('<g clip-path="url(#' + clip_id + ')">')
    parts.append('<circle cx="100" cy="100" r="' + str(iris_radius) + '" fill="' + params["iris"] + '"/>')
    parts.append('<circle cx="100" cy="100" r="' + str(iris_radius * 0.45) + '" fill="#0a0a0a"/>')
    parts.append('<circle cx="' + str(100 + iris_radius * 0.3) + '" cy="' + str(100 - iris_radius * 0.35) + '" r="' + str(iris_radius * 0.18) + '" fill="white" opacity="0.85"/>')
    parts.append(render_symbol(params["symbol"], symbol_color))
    parts.append('</g>')
    parts.append(render_lashes(params["shape"], params["lashes"]))
    parts.append('</svg>')
    return "".join(parts)


def eye_svg(avatar_dict, size=240):
    """Wrapper che converte dict in tuple per la cache."""
    keys = ["shape", "iris", "symbol", "lashes", "brow", "bg"]
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
css_lines.append('.cat-label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: ' + BRAND_BLUE + '; opacity: 0.7; margin-top: 0.8rem; margin-bottom: 0.3rem; }')
css_lines.append('</style>')

st.markdown("\n".join(css_lines), unsafe_allow_html=True)


# ==================== STATE ====================
if "username" not in st.session_state:
    st.session_state.username = None
if "view" not in st.session_state:
    st.session_state.view = "home"

# Inizializzazione dello stato widget (fondamentale per fix bug radio)
def ensure_avatar_state(avatar_dict):
    """Assicura che i valori dei widget siano sincronizzati con l'avatar salvato.
    Questo previene il bug 'clicco su A e mi prende B'."""
    for k, v in avatar_dict.items():
        widget_key = "w_" + k
        if widget_key not in st.session_state:
            st.session_state[widget_key] = v


st.markdown('<div class="proto-banner">Prototipo v3 - i dati si salvano sul server. Su Streamlit Cloud possono essere cancellati quando viene ridistribuito il codice.</div>', unsafe_allow_html=True)


db = load_db()


# ==================== LOGIN ====================
if st.session_state.username is None:
    login_hero = '<div class="login-hero"><div class="login-hero-title">Peccioli Eyes</div><div class="login-hero-sub">to New Orleans</div><div class="login-hero-year">2026</div><p style="color:rgba(255,255,255,0.85);margin-top:1.5rem;font-size:0.95rem;max-width:420px;margin-left:auto;margin-right:auto;line-height:1.6;">Crea il tuo sguardo personale. Scegli un nome e una password che ricorderai - niente email, niente dati personali.</p></div>'
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
                st.error("Non esiste un profilo con il nome '" + str(login_user) + "'. Creane uno nuovo dalla tab accanto.")
            elif db[u].get("password") != login_pwd:
                st.error("Password sbagliata. Riprova.")
            else:
                st.session_state.username = u
                # Reset widget state al login
                for k in ["w_shape", "w_iris", "w_symbol_cat", "w_symbol", "w_lashes", "w_brow", "w_bg"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()

    with tab_new:
        c1, c2 = st.columns(2)
        with c1:
            new_user = st.text_input("Scegli un nome", key="new_user", placeholder="Es. marco, giulia93...")
        with c2:
            new_pwd = st.text_input("Inventa una password", type="password", key="new_pwd", placeholder="Qualcosa che ricordi")
        st.caption("Il nome sara visibile agli altri nella galleria. La password la ricordi solo tu.")
        if st.button("Crea il mio profilo", key="btn_new", use_container_width=True):
            u = (new_user or "").strip().lower()
            if not u:
                st.error("Scegli un nome")
            elif len(u) < 2:
                st.error("Il nome deve avere almeno 2 caratteri")
            elif not new_pwd or len(new_pwd) < 3:
                st.error("La password deve avere almeno 3 caratteri")
            elif u in db:
                st.error("Un profilo con il nome '" + str(new_user) + "' esiste gia. Scegline un altro.")
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
                for k in ["w_shape", "w_iris", "w_symbol_cat", "w_symbol", "w_lashes", "w_brow", "w_bg"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.success("Profilo creato! Ora crea il tuo sguardo.")
                st.rerun()

    st.stop()


# ==================== LOGGATO ====================
user = db[st.session_state.username]
avatar = user["avatar"]
# Assicura sempre che il campo brow esista (backward compat)
if "brow" not in avatar:
    avatar["brow"] = "none"
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
                if k.startswith("w_"):
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
        home_text = '<div class="section-title-home">Ciao, ' + display_name + '</div><div class="section-sub-home">Benvenuto nel tuo portale</div><p style="color:#3a4a5c;line-height:1.7;font-size:0.95rem;">Questo e il tuo spazio personale dentro <strong>Peccioli Eyes</strong>. Il tuo sguardo e unico e ti rappresenta nel viaggio verso New Orleans.</p><p style="color:#3a4a5c;line-height:1.7;font-size:0.95rem;">Puoi modificarlo in qualunque momento dalla sezione <strong>Sguardo</strong>, e vedere tutti gli altri nella <strong>Galleria</strong>.</p>'
        st.markdown(home_text, unsafe_allow_html=True)

        total_users = len(db)
        stats_card = '<div style="background:white;border:1px solid rgba(19,0,137,0.1);border-radius:16px;padding:1rem 1.2rem;margin-top:1rem;"><div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:' + BRAND_BLUE + ';font-weight:700;opacity:0.7;">Sguardi creati finora</div><div style="font-family:\'Playfair Display\',serif;font-size:2rem;font-weight:800;color:' + BRAND_BLUE + ';">' + str(total_users) + '</div></div>'
        st.markdown(stats_card, unsafe_allow_html=True)


# ==================== EDITOR ====================
elif st.session_state.view == "editor":
    st.markdown('<div class="section-title-home">Crea il tuo sguardo</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub-home">Ogni dettaglio racconta chi sei</div>', unsafe_allow_html=True)

    # Inizializza widget state dalla prima volta o dopo login
    ensure_avatar_state(avatar)

    # Determina categoria iniziale del simbolo corrente
    current_symbol = avatar.get("symbol", "trumpet")
    current_sym_obj = next((s for s in SYMBOLS if s["id"] == current_symbol), SYMBOLS[0])
    if "w_symbol_cat" not in st.session_state:
        st.session_state.w_symbol_cat = current_sym_obj["category"]

    c_preview, c_controls = st.columns([1, 1.3])

    # Costruisci avatar live dai widget state (NON modifichiamo avatar direttamente)
    live_avatar = {
        "shape": st.session_state.get("w_shape", avatar["shape"]),
        "iris": st.session_state.get("w_iris", avatar["iris"]),
        "symbol": st.session_state.get("w_symbol", avatar["symbol"]),
        "lashes": st.session_state.get("w_lashes", avatar["lashes"]),
        "brow": st.session_state.get("w_brow", avatar.get("brow", "none")),
        "bg": st.session_state.get("w_bg", avatar["bg"]),
    }

    with c_preview:
        preview_svg = eye_svg(live_avatar, size=300)
        preview_card = '<div style="background:' + BRAND_BLUE_LIGHT + ';border-radius:20px;padding:1.5rem;text-align:center;position:sticky;top:1rem;">' + preview_svg + '<div style="margin-top:0.8rem;font-size:0.85rem;color:' + BRAND_BLUE + ';font-weight:500;">Anteprima dal vivo</div></div>'
        st.markdown(preview_card, unsafe_allow_html=True)

        if st.button("Sguardo casuale", use_container_width=True, key="randomize"):
            st.session_state.w_shape = random.choice(SHAPES)["id"]
            st.session_state.w_iris = random.choice([c[1] for c in IRIS_COLORS])
            rand_sym = random.choice(SYMBOLS)
            st.session_state.w_symbol = rand_sym["id"]
            st.session_state.w_symbol_cat = rand_sym["category"]
            st.session_state.w_lashes = random.choice(LASHES)["id"]
            st.session_state.w_brow = random.choice(BROWS)["id"]
            st.session_state.w_bg = random.choice(BACKGROUNDS)["id"]
            st.rerun()

        st.caption("L'anteprima e dal vivo. Clicca **Salva** in fondo per rendere permanenti le scelte.")

    with c_controls:
        st.markdown("**Forma dell'occhio**")
        shape_labels = [s["label"] for s in SHAPES]
        shape_ids = [s["id"] for s in SHAPES]
        default_idx = shape_ids.index(live_avatar["shape"]) if live_avatar["shape"] in shape_ids else 0
        new_shape_label = st.radio("Forma", shape_labels, index=default_idx, horizontal=True, label_visibility="collapsed", key="_sel_shape")
        st.session_state.w_shape = shape_ids[shape_labels.index(new_shape_label)]

        st.markdown("**Colore iride**")
        iris_labels = [c[0] for c in IRIS_COLORS]
        iris_values = [c[1] for c in IRIS_COLORS]
        default_idx = iris_values.index(live_avatar["iris"]) if live_avatar["iris"] in iris_values else 0
        new_iris_label = st.selectbox("Iride", iris_labels, index=default_idx, label_visibility="collapsed", key="_sel_iris")
        st.session_state.w_iris = iris_values[iris_labels.index(new_iris_label)]

        st.markdown("**Simbolo nell'iride**")
        cat_labels = [c[1] for c in SYMBOL_CATEGORIES]
        cat_ids = [c[0] for c in SYMBOL_CATEGORIES]
        default_cat_idx = cat_ids.index(st.session_state.w_symbol_cat) if st.session_state.w_symbol_cat in cat_ids else 0
        selected_cat_label = st.radio("Categoria", cat_labels, index=default_cat_idx, horizontal=True, label_visibility="collapsed", key="_sel_cat")
        selected_cat_id = cat_ids[cat_labels.index(selected_cat_label)]
        st.session_state.w_symbol_cat = selected_cat_id

        # Lista simboli della categoria scelta
        cat_symbols = [s for s in SYMBOLS if s["category"] == selected_cat_id]
        sym_labels = [s["label"] for s in cat_symbols]
        sym_ids = [s["id"] for s in cat_symbols]

        # Se il simbolo corrente non è in questa categoria, resetta al primo
        if live_avatar["symbol"] not in sym_ids:
            current_sym_in_cat = sym_ids[0]
        else:
            current_sym_in_cat = live_avatar["symbol"]

        default_idx = sym_ids.index(current_sym_in_cat)
        new_sym_label = st.radio("Simbolo", sym_labels, index=default_idx, label_visibility="collapsed", key="_sel_sym_" + selected_cat_id)
        st.session_state.w_symbol = sym_ids[sym_labels.index(new_sym_label)]

        st.markdown("**Ciglia**")
        lash_labels = [l["label"] for l in LASHES]
        lash_ids = [l["id"] for l in LASHES]
        default_idx = lash_ids.index(live_avatar["lashes"]) if live_avatar["lashes"] in lash_ids else 0
        new_lash_label = st.radio("Ciglia", lash_labels, index=default_idx, horizontal=True, label_visibility="collapsed", key="_sel_lashes")
        st.session_state.w_lashes = lash_ids[lash_labels.index(new_lash_label)]

        st.markdown("**Sopracciglio**")
        brow_labels = [b["label"] for b in BROWS]
        brow_ids = [b["id"] for b in BROWS]
        default_idx = brow_ids.index(live_avatar["brow"]) if live_avatar["brow"] in brow_ids else 0
        new_brow_label = st.radio("Sopracciglio", brow_labels, index=default_idx, horizontal=True, label_visibility="collapsed", key="_sel_brow")
        st.session_state.w_brow = brow_ids[brow_labels.index(new_brow_label)]

        st.markdown("**Sfondo**")
        bg_labels = [b["label"] for b in BACKGROUNDS]
        bg_ids = [b["id"] for b in BACKGROUNDS]
        default_idx = bg_ids.index(live_avatar["bg"]) if live_avatar["bg"] in bg_ids else 0
        new_bg_label = st.radio("Sfondo", bg_labels, index=default_idx, horizontal=True, label_visibility="collapsed", key="_sel_bg")
        st.session_state.w_bg = bg_ids[bg_labels.index(new_bg_label)]

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
                    "lashes": st.session_state.w_lashes,
                    "brow": st.session_state.w_brow,
                    "bg": st.session_state.w_bg,
                }
                db[st.session_state.username]["visible_in_gallery"] = visible
                save_db(db)
                st.success("Sguardo salvato!")
                st.rerun()
        with col_reset:
            if st.button("Annulla", use_container_width=True, key="btn_reset_avatar"):
                for k in ["w_shape", "w_iris", "w_symbol_cat", "w_symbol", "w_lashes", "w_brow", "w_bg"]:
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

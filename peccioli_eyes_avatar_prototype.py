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


def render_symbol(sym_id, color, cy=100):
    """Simboli piccoli disegnati attorno alla pupilla bianca centrale.
    cy=100 = centro occhio. Posizionati a distanza dalla pupilla bianca."""
    if sym_id == "torre_peccioli":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<rect x="-4" y="-8" width="8" height="14" fill="' + color + '"/>')
        parts.append('<polygon points="-6,-8 0,-13 6,-8" fill="' + color + '"/>')
        parts.append('<rect x="-1.5" y="-5" width="1.2" height="2.5" fill="white"/>')
        parts.append('<rect x="0.3" y="-5" width="1.2" height="2.5" fill="white"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "cipresso":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<ellipse cx="0" cy="-2" rx="3" ry="8" fill="' + color + '"/>')
        parts.append('<rect x="-0.7" y="5" width="1.4" height="3" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "collina":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<path d="M -10 5 Q -5 -3 0 1 Q 5 -5 10 5 Z" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "uliva":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<path d="M -8 2 Q 0 -4 8 2" fill="none" stroke="' + color + '" stroke-width="1.5"/>')
        parts.append('<ellipse cx="-4" cy="-1" rx="1.8" ry="1" fill="' + color + '"/>')
        parts.append('<ellipse cx="0" cy="-2" rx="1.8" ry="1" fill="' + color + '"/>')
        parts.append('<ellipse cx="4" cy="-1" rx="1.8" ry="1" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "trumpet":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<path d="M -9 -3 L -3 -5 L -3 5 L -9 3 Z" fill="' + color + '"/>')
        parts.append('<rect x="-3" y="-2" width="8" height="4" fill="' + color + '"/>')
        parts.append('<circle cx="7" cy="0" r="4" fill="none" stroke="' + color + '" stroke-width="1.6"/>')
        parts.append('<circle cx="-1" cy="-6" r="0.8" fill="' + color + '"/>')
        parts.append('<circle cx="1.5" cy="-6" r="0.8" fill="' + color + '"/>')
        parts.append('<circle cx="4" cy="-6" r="0.8" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "mask":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<path d="M -8 -2 Q -8 -5 -5 -6 Q 0 -7 5 -6 Q 8 -5 8 -2 Q 8 3 0 5 Q -8 3 -8 -2 Z" fill="' + color + '"/>')
        parts.append('<ellipse cx="-3" cy="-1" rx="1.5" ry="1.5" fill="white"/>')
        parts.append('<ellipse cx="3" cy="-1" rx="1.5" ry="1.5" fill="white"/>')
        parts.append('<line x1="-8" y1="-4" x2="-11" y2="-7" stroke="' + color + '" stroke-width="1.2"/>')
        parts.append('<line x1="8" y1="-4" x2="11" y2="-7" stroke="' + color + '" stroke-width="1.2"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "fleur":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<path d="M 0 -8 Q -3 -4 -1.5 0 Q -3 4 0 8 Q 3 4 1.5 0 Q 3 -4 0 -8 Z" fill="' + color + '"/>')
        parts.append('<path d="M -6 -1 Q -8 2 -3 6 Q 0 3 -1.5 1 Q -4 -3 -6 -1 Z" fill="' + color + '" opacity="0.85"/>')
        parts.append('<path d="M 6 -1 Q 8 2 3 6 Q 0 3 1.5 1 Q 4 -3 6 -1 Z" fill="' + color + '" opacity="0.85"/>')
        parts.append('<rect x="-5" y="0" width="10" height="1.8" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "riverboat":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<path d="M -9 3 L 9 3 L 7 6 L -7 6 Z" fill="' + color + '"/>')
        parts.append('<rect x="-6" y="-1" width="12" height="4" fill="' + color + '"/>')
        parts.append('<rect x="-1.5" y="-6" width="1.5" height="5" fill="' + color + '"/>')
        parts.append('<rect x="1.5" y="-6" width="1.5" height="5" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "balcony":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<rect x="-8" y="3" width="16" height="1.5" fill="' + color + '"/>')
        parts.append('<rect x="-8" y="-5" width="16" height="1.5" fill="' + color + '"/>')
        parts.append('<line x1="-6" y1="-3.5" x2="-6" y2="3" stroke="' + color + '" stroke-width="0.8"/>')
        parts.append('<line x1="-3" y1="-3.5" x2="-3" y2="3" stroke="' + color + '" stroke-width="0.8"/>')
        parts.append('<line x1="0" y1="-3.5" x2="0" y2="3" stroke="' + color + '" stroke-width="0.8"/>')
        parts.append('<line x1="3" y1="-3.5" x2="3" y2="3" stroke="' + color + '" stroke-width="0.8"/>')
        parts.append('<line x1="6" y1="-3.5" x2="6" y2="3" stroke="' + color + '" stroke-width="0.8"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "note":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<ellipse cx="-2" cy="5" rx="4" ry="3" fill="' + color + '" transform="rotate(-20 -2 5)"/>')
        parts.append('<rect x="1" y="-7" width="1.5" height="13" fill="' + color + '"/>')
        parts.append('<path d="M 2.5 -7 Q 9 -5 8 0.5" fill="none" stroke="' + color + '" stroke-width="1.8" stroke-linecap="round"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "wave":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<path d="M -9 -2 Q -4 -6 0 -2 Q 4 2 9 -2" fill="none" stroke="' + color + '" stroke-width="1.8" stroke-linecap="round"/>')
        parts.append('<path d="M -9 3 Q -4 -1 0 3 Q 4 7 9 3" fill="none" stroke="' + color + '" stroke-width="1.8" stroke-linecap="round"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "people":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<circle cx="-6" cy="-2" r="2" fill="' + color + '"/>')
        parts.append('<rect x="-8" y="1" width="4" height="5" rx="1" fill="' + color + '"/>')
        parts.append('<circle cx="0" cy="-3" r="2.5" fill="' + color + '"/>')
        parts.append('<rect x="-2.5" y="0" width="5" height="7" rx="1" fill="' + color + '"/>')
        parts.append('<circle cx="6" cy="-2" r="2" fill="' + color + '"/>')
        parts.append('<rect x="4" y="1" width="4" height="5" rx="1" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "book":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<path d="M -7 -5 L 0 -3 L 7 -5 L 7 5 L 0 3 L -7 5 Z" fill="' + color + '"/>')
        parts.append('<line x1="0" y1="-3" x2="0" y2="3" stroke="white" stroke-width="0.8"/>')
        parts.append('</g>')
        return "".join(parts)

    if sym_id == "star":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<polygon points="0,-8 2.5,-2.5 8,-2.5 3.5,1.5 5,7 0,4 -5,7 -3.5,1.5 -8,-2.5 -2.5,-2.5" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "heart":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<path d="M 0 6 C -8 -1 -8 -6 -4 -6 C -1.5 -6 0 -4 0 -2 C 0 -4 1.5 -6 4 -6 C 8 -6 8 -1 0 6 Z" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "eye_inside":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<path d="M -8 0 Q 0 -5 8 0 Q 0 5 -8 0 Z" fill="none" stroke="' + color + '" stroke-width="1.5"/>')
        parts.append('<circle cx="0" cy="0" r="2.5" fill="' + color + '"/>')
        parts.append('<circle cx="0" cy="0" r="0.8" fill="white"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "moon":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<path d="M -2 -7 A 6 6 0 1 0 -2 7 A 4 4 0 1 1 -2 -7 Z" fill="' + color + '"/>')
        parts.append('</g>')
        return "".join(parts)
    if sym_id == "lightning":
        parts = []
        parts.append('<g transform="translate(100 ' + str(cy - 18) + ')">')
        parts.append('<polygon points="-1.5,-8 2.5,-1.5 -0.5,-1.5 1.5,8 -3,1.5 0,1.5" fill="' + color + '"/>')
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
    return "#0a0a0a"


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

    if params["bg"] in ("yellow-solid", "white-solid"):
        stroke_color = BRAND_BLUE
    else:
        stroke_color = "white"

    if params["bg"] == "white-solid":
        sclera_color = "#f4f1e8"
    else:
        sclera_color = "white"

    symbol_color = contrast_on(params["iris"])

    content = params["shape"] + params["iris"] + params["symbol"] + params["bg"] + params["lashes"]
    clip_id = "eye-clip-" + hashlib.md5(content.encode()).hexdigest()[:8]

    pupil_radius = iris_radius * 0.35

    parts = []
    parts.append('<svg viewBox="0 0 200 200" width="' + str(size) + '" height="' + str(size) + '" xmlns="http://www.w3.org/2000/svg">')
    parts.append('<defs><clipPath id="' + clip_id + '"><path d="' + eye_d + '"/></clipPath></defs>')
    parts.append(render_background(params["bg"]))
    parts.append('<path d="' + eye_d + '" fill="' + sclera_color + '" stroke="' + stroke_color + '" stroke-width="3"/>')
    parts.append('<g clip-path="url(#' + clip_id + ')">')
    parts.append('<circle cx="100" cy="100" r="' + str(iris_radius) + '" fill="' + params["iris"] + '"/>')
    # SIMBOLO nella parte alta dell'iride (sopra la pupilla)
    parts.append(render_symbol(params["symbol"], symbol_color, cy=100))
    # PUPILLA BIANCA (risalta sul colore iride)
    parts.append('<circle cx="100" cy="100" r="' + str(pupil_radius) + '" fill="white"/>')
    # Piccolo highlight scuro per dare profondità
    parts.append('<circle cx="' + str(100 - pupil_radius * 0.3) + '" cy="' + str(100 + pupil_radius * 0.3) + '" r="' + str(pupil_radius * 0.2) + '" fill="' + symbol_color + '" opacity="0.25"/>')
    parts.append('</g>')
    parts.append(render_lashes(params["shape"], params["lashes"]))
    parts.append('</svg>')
    return "".join(parts)


def eye_svg(avatar_dict, size=240):
    keys = ["shape", "iris", "symbol", "lashes", "bg"]
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


# ==================== CALLBACKS (fix lentezza) ====================
def on_shape_change():
    st.session_state.w_shape = st.session_state._sel_shape_id

def on_iris_change():
    st.session_state.w_iris = st.session_state._sel_iris_val

def on_cat_change():
    st.session_state.w_symbol_cat = st.session_state._sel_cat_id
    # Reset simbolo alla prima voce della nuova categoria
    cat_syms = [s for s in SYMBOLS if s["category"] == st.session_state.w_symbol_cat]
    if cat_syms:
        st.session_state.w_symbol = cat_syms[0]["id"]

def on_symbol_change():
    st.session_state.w_symbol = st.session_state._sel_symbol_id

def on_lashes_change():
    st.session_state.w_lashes = st.session_state._sel_lashes_id

def on_bg_change():
    st.session_state.w_bg = st.session_state._sel_bg_id


st.markdown('<div class="proto-banner">Prototipo v4 - pupilla bianca, simboli sopra iride. Salvataggio su file locale, reset al redeploy.</div>', unsafe_allow_html=True)


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
                    if k.startswith("w_") or k.startswith("_sel_"):
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
                    if k.startswith("w_") or k.startswith("_sel_"):
                        del st.session_state[k]
                st.success("Profilo creato!")
                st.rerun()

    st.stop()


# ==================== LOGGATO ====================
user = db[st.session_state.username]
avatar = user["avatar"]
# Pulizia: rimuovi campo brow se esiste (legacy v3)
if "brow" in avatar:
    del avatar["brow"]
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
                if k.startswith("w_") or k.startswith("_sel_"):
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

    # Inizializza w_* dai valori attuali dell'avatar (solo prima volta)
    for key, default in [("w_shape", avatar["shape"]), ("w_iris", avatar["iris"]),
                          ("w_symbol", avatar["symbol"]), ("w_lashes", avatar["lashes"]),
                          ("w_bg", avatar["bg"])]:
        if key not in st.session_state:
            st.session_state[key] = default

    if "w_symbol_cat" not in st.session_state:
        current_sym_obj = next((s for s in SYMBOLS if s["id"] == st.session_state.w_symbol), SYMBOLS[0])
        st.session_state.w_symbol_cat = current_sym_obj["category"]

    # Avatar live letto SOLO dai session_state w_*
    live_avatar = {
        "shape": st.session_state.w_shape,
        "iris": st.session_state.w_iris,
        "symbol": st.session_state.w_symbol,
        "lashes": st.session_state.w_lashes,
        "bg": st.session_state.w_bg,
    }

    c_preview, c_controls = st.columns([1, 1.3])

    with c_preview:
        preview_svg = eye_svg(live_avatar, size=300)
        preview_card = '<div style="background:' + BRAND_BLUE_LIGHT + ';border-radius:20px;padding:1.5rem;text-align:center;">' + preview_svg + '<div style="margin-top:0.8rem;font-size:0.85rem;color:' + BRAND_BLUE + ';font-weight:500;">Anteprima dal vivo</div></div>'
        st.markdown(preview_card, unsafe_allow_html=True)

        if st.button("Sguardo casuale", use_container_width=True, key="randomize"):
            st.session_state.w_shape = random.choice(SHAPES)["id"]
            st.session_state.w_iris = random.choice([c[1] for c in IRIS_COLORS])
            rand_sym = random.choice(SYMBOLS)
            st.session_state.w_symbol = rand_sym["id"]
            st.session_state.w_symbol_cat = rand_sym["category"]
            st.session_state.w_lashes = random.choice(LASHES)["id"]
            st.session_state.w_bg = random.choice(BACKGROUNDS)["id"]
            st.rerun()

        st.caption("Clicca su **Salva** per rendere permanenti le scelte.")

    with c_controls:
        # FORMA
        st.markdown("**Forma dell'occhio**")
        shape_labels = [s["label"] for s in SHAPES]
        shape_ids = [s["id"] for s in SHAPES]
        current_shape_idx = shape_ids.index(st.session_state.w_shape) if st.session_state.w_shape in shape_ids else 0
        new_shape_label = st.radio("Forma", shape_labels, index=current_shape_idx, horizontal=True, label_visibility="collapsed", key="__rd_shape")
        st.session_state._sel_shape_id = shape_ids[shape_labels.index(new_shape_label)]
        if st.session_state._sel_shape_id != st.session_state.w_shape:
            st.session_state.w_shape = st.session_state._sel_shape_id
            st.rerun()

        # IRIDE
        st.markdown("**Colore iride**")
        iris_labels = [c[0] for c in IRIS_COLORS]
        iris_values = [c[1] for c in IRIS_COLORS]
        current_iris_idx = iris_values.index(st.session_state.w_iris) if st.session_state.w_iris in iris_values else 0
        new_iris_label = st.selectbox("Iride", iris_labels, index=current_iris_idx, label_visibility="collapsed", key="__sb_iris")
        new_iris_val = iris_values[iris_labels.index(new_iris_label)]
        if new_iris_val != st.session_state.w_iris:
            st.session_state.w_iris = new_iris_val
            st.rerun()

        # CATEGORIA SIMBOLI
        st.markdown("**Simbolo nell'iride**")
        cat_labels = [c[1] for c in SYMBOL_CATEGORIES]
        cat_ids = [c[0] for c in SYMBOL_CATEGORIES]
        current_cat_idx = cat_ids.index(st.session_state.w_symbol_cat) if st.session_state.w_symbol_cat in cat_ids else 0
        selected_cat_label = st.radio("Categoria", cat_labels, index=current_cat_idx, horizontal=True, label_visibility="collapsed", key="__rd_cat")
        selected_cat_id = cat_ids[cat_labels.index(selected_cat_label)]
        if selected_cat_id != st.session_state.w_symbol_cat:
            st.session_state.w_symbol_cat = selected_cat_id
            cat_syms = [s for s in SYMBOLS if s["category"] == selected_cat_id]
            if cat_syms:
                st.session_state.w_symbol = cat_syms[0]["id"]
            st.rerun()

        # SIMBOLO
        cat_symbols = [s for s in SYMBOLS if s["category"] == st.session_state.w_symbol_cat]
        sym_labels = [s["label"] for s in cat_symbols]
        sym_ids = [s["id"] for s in cat_symbols]
        if st.session_state.w_symbol not in sym_ids:
            st.session_state.w_symbol = sym_ids[0]
        current_sym_idx = sym_ids.index(st.session_state.w_symbol)
        new_sym_label = st.radio("Simbolo", sym_labels, index=current_sym_idx, label_visibility="collapsed", key="__rd_sym_" + st.session_state.w_symbol_cat)
        new_sym_id = sym_ids[sym_labels.index(new_sym_label)]
        if new_sym_id != st.session_state.w_symbol:
            st.session_state.w_symbol = new_sym_id
            st.rerun()

        # CIGLIA
        st.markdown("**Ciglia**")
        lash_labels = [l["label"] for l in LASHES]
        lash_ids = [l["id"] for l in LASHES]
        current_lash_idx = lash_ids.index(st.session_state.w_lashes) if st.session_state.w_lashes in lash_ids else 0
        new_lash_label = st.radio("Ciglia", lash_labels, index=current_lash_idx, horizontal=True, label_visibility="collapsed", key="__rd_lashes")
        new_lash_id = lash_ids[lash_labels.index(new_lash_label)]
        if new_lash_id != st.session_state.w_lashes:
            st.session_state.w_lashes = new_lash_id
            st.rerun()

        # SFONDO
        st.markdown("**Sfondo**")
        bg_labels = [b["label"] for b in BACKGROUNDS]
        bg_ids = [b["id"] for b in BACKGROUNDS]
        current_bg_idx = bg_ids.index(st.session_state.w_bg) if st.session_state.w_bg in bg_ids else 0
        new_bg_label = st.radio("Sfondo", bg_labels, index=current_bg_idx, horizontal=True, label_visibility="collapsed", key="__rd_bg")
        new_bg_id = bg_ids[bg_labels.index(new_bg_label)]
        if new_bg_id != st.session_state.w_bg:
            st.session_state.w_bg = new_bg_id
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
                    "lashes": st.session_state.w_lashes,
                    "bg": st.session_state.w_bg,
                }
                db[st.session_state.username]["visible_in_gallery"] = visible
                save_db(db)
                st.success("Sguardo salvato!")
                st.rerun()
        with col_reset:
            if st.button("Annulla", use_container_width=True, key="btn_reset_avatar"):
                for k in ["w_shape", "w_iris", "w_symbol_cat", "w_symbol", "w_lashes", "w_bg"]:
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

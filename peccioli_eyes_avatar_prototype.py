import streamlit as st
import json
import random
from pathlib import Path
from datetime import datetime

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
]

IRIS_COLORS = [
    ("Giallo brand", "#FFDE59"),
    ("Blu brand", "#130089"),
    ("Verde", "#2ea36a"),
    ("Terracotta", "#c84a1e"),
    ("Viola", "#7a3fb8"),
    ("Petrolio", "#0a5a7a"),
    ("Ambra", "#b8860b"),
    ("Grigio", "#636363"),
]

SYMBOLS = [
    {"id": "trumpet", "label": "Tromba"},
    {"id": "note", "label": "Nota"},
    {"id": "fleur", "label": "Giglio"},
    {"id": "star", "label": "Stella"},
    {"id": "wave", "label": "Onda"},
]

LASHES = [
    {"id": "classic", "label": "Classiche"},
    {"id": "long", "label": "Lunghe"},
    {"id": "short", "label": "Corte"},
    {"id": "none", "label": "Assenti"},
]

BACKGROUNDS = [
    {"id": "blue-solid", "label": "Blu", "color": BRAND_BLUE},
    {"id": "yellow-solid", "label": "Giallo", "color": BRAND_YELLOW},
    {"id": "white-solid", "label": "Bianco", "color": "#fafafa"},
    {"id": "stars", "label": "Stelle", "color": BRAND_BLUE_DARK},
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
    return ""


def render_symbol(sym_id, color):
    parts = []
    if sym_id == "trumpet":
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M -14 -4 L -6 -8 L -6 8 L -14 4 Z" fill="' + color + '"/>')
        parts.append('<rect x="-6" y="-4" width="14" height="8" fill="' + color + '"/>')
        parts.append('<circle cx="12" cy="0" r="7" fill="none" stroke="' + color + '" stroke-width="2.5"/>')
        parts.append('<circle cx="-3" cy="-9" r="1.6" fill="' + color + '"/>')
        parts.append('<circle cx="1" cy="-9" r="1.6" fill="' + color + '"/>')
        parts.append('<circle cx="5" cy="-9" r="1.6" fill="' + color + '"/>')
        parts.append('</g>')
    elif sym_id == "note":
        parts.append('<g transform="translate(100 100)">')
        parts.append('<ellipse cx="-4" cy="8" rx="7" ry="5" fill="' + color + '" transform="rotate(-20 -4 8)"/>')
        parts.append('<rect x="2" y="-12" width="3" height="22" fill="' + color + '"/>')
        parts.append('<path d="M 5 -12 Q 15 -8 13 2" fill="none" stroke="' + color + '" stroke-width="3" stroke-linecap="round"/>')
        parts.append('</g>')
    elif sym_id == "fleur":
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M 0 -13 Q -5 -6 -3 0 Q -5 6 0 13 Q 5 6 3 0 Q 5 -6 0 -13 Z" fill="' + color + '"/>')
        parts.append('<path d="M -10 -4 Q -12 2 -6 10 Q 0 4 -2 -2 Q -8 -8 -10 -4 Z" fill="' + color + '" opacity="0.85"/>')
        parts.append('<path d="M 10 -4 Q 12 2 6 10 Q 0 4 2 -2 Q 8 -8 10 -4 Z" fill="' + color + '" opacity="0.85"/>')
        parts.append('<rect x="-9" y="-1" width="18" height="2.5" fill="' + color + '"/>')
        parts.append('</g>')
    elif sym_id == "star":
        parts.append('<g transform="translate(100 100)">')
        parts.append('<polygon points="0,-14 4,-4 14,-4 6,3 9,13 0,7 -9,13 -6,3 -14,-4 -4,-4" fill="' + color + '"/>')
        parts.append('</g>')
    elif sym_id == "wave":
        parts.append('<g transform="translate(100 100)">')
        parts.append('<path d="M -14 -3 Q -7 -10 0 -3 Q 7 4 14 -3" fill="none" stroke="' + color + '" stroke-width="2.8" stroke-linecap="round"/>')
        parts.append('<path d="M -14 5 Q -7 -2 0 5 Q 7 12 14 5" fill="none" stroke="' + color + '" stroke-width="2.8" stroke-linecap="round"/>')
        parts.append('</g>')
    return "".join(parts)


def render_lashes(shape, style):
    if style == "none":
        return ""
    if shape == "round":
        top_y = 40
        xs = [50, 65, 80, 100, 120, 135, 150]
    elif shape == "almond":
        top_y = 52
        xs = [50, 70, 90, 100, 110, 130, 150]
    else:
        top_y = 70
        xs = [50, 70, 90, 100, 110, 130, 150]
    if style == "long":
        length = 18
        thick = 2.5
    elif style == "short":
        length = 8
        thick = 2.0
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
    return "".join(out)


def contrast_on(hex_color):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    if lum > 0.6:
        return "#130089"
    return "#FFDE59"


def build_eye_svg(params, size=240):
    eye_d = eye_path(params["shape"])
    if params["shape"] == "narrow":
        iris_radius = 22
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
    clip_id = "eye-clip-" + params["shape"] + "-" + str(random.randint(1000, 9999))

    parts = []
    parts.append('<svg viewBox="0 0 200 200" width="' + str(size) + '" height="' + str(size) + '" xmlns="http://www.w3.org/2000/svg">')
    parts.append('<defs><clipPath id="' + clip_id + '"><path d="' + eye_d + '"/></clipPath></defs>')
    parts.append(render_background(params["bg"]))
    parts.append('<path d="' + eye_d + '" fill="' + sclera_color + '" stroke="' + stroke_color + '" stroke-width="3"/>')
    parts.append('<g clip-path="url(#' + clip_id + ')">')
    parts.append('<circle cx="100" cy="100" r="' + str(iris_radius) + '" fill="' + params["iris"] + '"/>')
    parts.append('<circle cx="100" cy="100" r="' + str(iris_radius * 0.55) + '" fill="#0a0a0a"/>')
    parts.append('<circle cx="' + str(100 + iris_radius * 0.3) + '" cy="' + str(100 - iris_radius * 0.3) + '" r="' + str(iris_radius * 0.22) + '" fill="white" opacity="0.9"/>')
    parts.append(render_symbol(params["symbol"], symbol_color))
    parts.append('</g>')
    parts.append(render_lashes(params["shape"], params["lashes"]))
    parts.append('</svg>')
    return "".join(parts)


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


if "username" not in st.session_state:
    st.session_state.username = None
if "view" not in st.session_state:
    st.session_state.view = "home"


st.markdown('<div class="proto-banner">Prototipo - i dati si salvano in un file locale. Serve solo per valutare il flusso e l estetica, non per produzione.</div>', unsafe_allow_html=True)


db = load_db()


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
                st.success("Profilo creato! Ora crea il tuo sguardo.")
                st.rerun()

    st.stop()


user = db[st.session_state.username]
avatar = user["avatar"]
display_name = user["display_name"]


col_chip, col_nav = st.columns([2, 3])
with col_chip:
    chip_svg = build_eye_svg(avatar, size=40)
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
            st.rerun()

st.markdown("---")


if st.session_state.view == "home":
    c1, c2 = st.columns([1, 1.2])
    with c1:
        big_svg = build_eye_svg(avatar, size=280)
        home_card = '<div style="background:' + BRAND_BLUE_LIGHT + ';border-radius:24px;padding:1.5rem;text-align:center;">' + big_svg + '<div style="margin-top:0.8rem;font-family:\'Lobster Two\',cursive;font-style:italic;font-size:1.3rem;color:' + BRAND_BLUE + ';">Il tuo sguardo</div></div>'
        st.markdown(home_card, unsafe_allow_html=True)
    with c2:
        home_text = '<div class="section-title-home">Ciao, ' + display_name + '</div><div class="section-sub-home">Benvenuto nel tuo portale</div><p style="color:#3a4a5c;line-height:1.7;font-size:0.95rem;">Questo e il tuo spazio personale dentro <strong>Peccioli Eyes</strong>. Il tuo sguardo e unico e ti rappresenta nel viaggio verso New Orleans.</p><p style="color:#3a4a5c;line-height:1.7;font-size:0.95rem;">Puoi modificarlo in qualunque momento dalla sezione <strong>Sguardo</strong>, e vedere tutti gli altri nella <strong>Galleria</strong>.</p>'
        st.markdown(home_text, unsafe_allow_html=True)

        total_users = len(db)
        stats_card = '<div style="background:white;border:1px solid rgba(19,0,137,0.1);border-radius:16px;padding:1rem 1.2rem;margin-top:1rem;"><div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:' + BRAND_BLUE + ';font-weight:700;opacity:0.7;">Sguardi creati finora</div><div style="font-family:\'Playfair Display\',serif;font-size:2rem;font-weight:800;color:' + BRAND_BLUE + ';">' + str(total_users) + '</div></div>'
        st.markdown(stats_card, unsafe_allow_html=True)


elif st.session_state.view == "editor":
    st.markdown('<div class="section-title-home">Crea il tuo sguardo</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub-home">Ogni dettaglio racconta chi sei</div>', unsafe_allow_html=True)

    c_preview, c_controls = st.columns([1, 1.3])

    with c_preview:
        preview_svg = build_eye_svg(avatar, size=300)
        preview_card = '<div style="background:' + BRAND_BLUE_LIGHT + ';border-radius:20px;padding:1.5rem;text-align:center;">' + preview_svg + '<div style="margin-top:0.8rem;font-size:0.85rem;color:' + BRAND_BLUE + ';font-weight:500;">Anteprima dal vivo</div></div>'
        st.markdown(preview_card, unsafe_allow_html=True)

        if st.button("Sguardo casuale", use_container_width=True, key="randomize"):
            avatar["shape"] = random.choice(SHAPES)["id"]
            avatar["iris"] = random.choice([c[1] for c in IRIS_COLORS])
            avatar["symbol"] = random.choice(SYMBOLS)["id"]
            avatar["lashes"] = random.choice(LASHES)["id"]
            avatar["bg"] = random.choice(BACKGROUNDS)["id"]
            db[st.session_state.username]["avatar"] = avatar
            save_db(db)
            st.rerun()

    with c_controls:
        st.markdown("**Forma dell'occhio**")
        shape_labels = [s["label"] for s in SHAPES]
        shape_ids = [s["id"] for s in SHAPES]
        if avatar["shape"] in shape_ids:
            current_shape_idx = shape_ids.index(avatar["shape"])
        else:
            current_shape_idx = 0
        new_shape = st.radio("Forma", shape_labels, index=current_shape_idx, horizontal=True, label_visibility="collapsed", key="sel_shape")
        avatar["shape"] = shape_ids[shape_labels.index(new_shape)]

        st.markdown("**Colore iride**")
        iris_labels = [c[0] for c in IRIS_COLORS]
        iris_values = [c[1] for c in IRIS_COLORS]
        if avatar["iris"] in iris_values:
            current_iris_idx = iris_values.index(avatar["iris"])
        else:
            current_iris_idx = 0
        new_iris = st.selectbox("Iride", iris_labels, index=current_iris_idx, label_visibility="collapsed", key="sel_iris")
        avatar["iris"] = iris_values[iris_labels.index(new_iris)]

        st.markdown("**Simbolo nell'iride**")
        symbol_labels = [s["label"] for s in SYMBOLS]
        symbol_ids = [s["id"] for s in SYMBOLS]
        if avatar["symbol"] in symbol_ids:
            current_sym_idx = symbol_ids.index(avatar["symbol"])
        else:
            current_sym_idx = 0
        new_sym = st.radio("Simbolo", symbol_labels, index=current_sym_idx, horizontal=True, label_visibility="collapsed", key="sel_symbol")
        avatar["symbol"] = symbol_ids[symbol_labels.index(new_sym)]

        st.markdown("**Ciglia**")
        lash_labels = [l["label"] for l in LASHES]
        lash_ids = [l["id"] for l in LASHES]
        if avatar["lashes"] in lash_ids:
            current_lash_idx = lash_ids.index(avatar["lashes"])
        else:
            current_lash_idx = 0
        new_lash = st.radio("Ciglia", lash_labels, index=current_lash_idx, horizontal=True, label_visibility="collapsed", key="sel_lashes")
        avatar["lashes"] = lash_ids[lash_labels.index(new_lash)]

        st.markdown("**Sfondo**")
        bg_labels = [b["label"] for b in BACKGROUNDS]
        bg_ids = [b["id"] for b in BACKGROUNDS]
        if avatar["bg"] in bg_ids:
            current_bg_idx = bg_ids.index(avatar["bg"])
        else:
            current_bg_idx = 0
        new_bg = st.radio("Sfondo", bg_labels, index=current_bg_idx, horizontal=True, label_visibility="collapsed", key="sel_bg")
        avatar["bg"] = bg_ids[bg_labels.index(new_bg)]

        st.markdown("---")
        st.markdown("**Privacy**")
        visible = st.checkbox("Mostra il mio sguardo nella galleria pubblica", value=user.get("visible_in_gallery", True), key="sel_visible")

        if st.button("Salva il mio sguardo", use_container_width=True, type="primary"):
            db[st.session_state.username]["avatar"] = avatar
            db[st.session_state.username]["visible_in_gallery"] = visible
            save_db(db)
            st.success("Sguardo salvato!")

        db[st.session_state.username]["avatar"] = avatar
        save_db(db)


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
                    svg = build_eye_svg(u["avatar"], size=140)
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

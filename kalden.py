import streamlit as st
import google.generativeai as genai
from PIL import Image
import random
import json
import os
from datetime import datetime

# ══════════════════════════════════════════════════════════════
# 1. PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Jayesh Tutorial - SSC Genius AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════
# 2. PREMIUM DARK CSS — TEXT VISIBILITY FIXED
# ══════════════════════════════════════════════════════════════
custom_css = """
<style>
/* ── Hide Defaults ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}

/* ── Root Variables ── */
:root {
    --primary: #7C73FF;
    --primary-glow: rgba(124,115,255,0.35);
    --secondary: #FF6584;
    --accent: #00D68F;
    --bg-dark: #0F0F1E;
    --glass: rgba(255,255,255,0.07);
    --glass-hover: rgba(255,255,255,0.12);
    --glass-border: rgba(255,255,255,0.15);
    --text-primary: #FFFFFF;
    --text-secondary: #B0B0CC;
    --text-dim: #7878A0;
}

/* ── Global Text Override — MOST IMPORTANT ── */
.stApp, .stApp * {
    color: var(--text-primary) !important;
}

/* Specific overrides for elements that need dimmer text */
.stApp .stCaption, .stApp .stCaption * {
    color: var(--text-secondary) !important;
}

.stApp {
    background: var(--bg-dark);
}

/* Animated mesh background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 600px 600px at 15% 80%, rgba(124,115,255,0.13) 0%, transparent 70%),
        radial-gradient(ellipse 500px 500px at 85% 15%, rgba(255,101,132,0.09) 0%, transparent 70%),
        radial-gradient(ellipse 400px 400px at 50% 50%, rgba(0,214,143,0.07) 0%, transparent 70%);
    z-index: -1;
    animation: bgPulse 12s ease-in-out infinite alternate;
}
@keyframes bgPulse {
    0%   { opacity: .7; }
    100% { opacity: 1; }
}

.block-container {
    padding: 1rem 2rem 2rem;
    max-width: 1500px;
}

/* ── Title ── */
.main-title {
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #7C73FF 0%, #FF6584 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-align: center;
    line-height: 1.2 !important;
    animation: fadeDown .7s ease-out;
}
.subtitle {
    text-align: center;
    color: var(--text-secondary) !important;
    font-size: .95rem;
    margin-bottom: 1.2rem;
    animation: fadeDown .7s ease-out .15s both;
}

/* ── Glass Card ── */
.glass-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.25rem;
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    transition: border-color .3s, box-shadow .3s;
    animation: fadeUp .5s ease-out;
}
.glass-card:hover {
    border-color: rgba(124,115,255,0.35);
    box-shadow: 0 0 30px rgba(124,115,255,0.06);
}

/* ── Section Header ── */
.sec-head {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--primary) !important;
    margin-bottom: .75rem;
    display: flex;
    align-items: center;
    gap: .4rem;
}

/* ── Stat Cards ── */
.stat-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: .7rem .5rem;
    text-align: center;
    transition: transform .25s, box-shadow .25s;
}
.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 24px rgba(124,115,255,0.12);
}
.stat-num {
    font-size: 1.7rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7C73FF, #FF6584) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}
.stat-lbl {
    font-size: .65rem;
    color: var(--text-dim) !important;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

/* ── Buttons ── */
.stButton>button {
    background: linear-gradient(135deg, #7C73FF, #FF6584) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: .55rem 1rem !important;
    transition: all .25s !important;
    white-space: nowrap;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 18px var(--primary-glow) !important;
}
.stButton>button p, .stButton>button span {
    color: #FFFFFF !important;
}

/* ── Chat Messages ── */
.stChatMessage {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 14px !important;
    padding: .9rem !important;
    margin-bottom: .4rem !important;
}
.stChatMessage p, .stChatMessage span, .stChatMessage div,
.stChatMessage li, .stChatMessage strong, .stChatMessage em {
    color: #FFFFFF !important;
}
.stChatMessage code {
    color: #FFD93D !important;
    background: rgba(255,255,255,0.08) !important;
}
.stChatMessage pre {
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
}
.stChatMessage pre code {
    color: #E0E0FF !important;
}

[data-testid="stChatMessageAvatar-Assistant"] {
    background: linear-gradient(135deg, #7C73FF, #FF6584) !important;
}
[data-testid="stChatMessageAvatar-User"] {
    background: linear-gradient(135deg, #00D68F, #0EA5E9) !important;
}

/* ── Chat Input ── */
.stChatInput {
    border-radius: 14px !important;
    border: 1px solid var(--glass-border) !important;
    background: rgba(255,255,255,0.06) !important;
}
.stChatInput textarea {
    color: #FFFFFF !important;
    background: rgba(255,255,255,0.04) !important;
    caret-color: #7C73FF !important;
}
.stChatInput textarea::placeholder {
    color: var(--text-dim) !important;
}
.stChatInput label, .stChatInput div[data-testid="stChatInputLabel"] {
    color: var(--text-secondary) !important;
}

/* ── Text / Number Inputs ── */
.stTextInput>div>div>input,
.stNumberInput>div>div>input {
    background: rgba(255,255,255,0.06) !important;
    border-color: var(--glass-border) !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    caret-color: #7C73FF !important;
}
.stTextInput>div>div>input::placeholder,
.stNumberInput>div>div>input::placeholder {
    color: var(--text-dim) !important;
}
.stTextInput label, .stNumberInput label {
    color: #FFFFFF !important;
}

/* ── Selectbox ── */
.stSelectbox label {
    color: #FFFFFF !important;
}
.stSelectbox>div>div {
    background: rgba(255,255,255,0.06) !important;
    border-color: var(--glass-border) !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
}
.stSelectbox>div>div>div {
    color: #FFFFFF !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: var(--glass);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--glass-border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--text-dim) !important;
    font-weight: 600 !important;
    font-size: .9rem !important;
}
.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: #FFFFFF !important;
}
.stTabs [aria-selected="true"] p {
    color: #FFFFFF !important;
}

/* ── Radio ── */
.stRadio>div {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 10px;
    padding: .5rem;
}
.stRadio label p {
    color: #FFFFFF !important;
}

/* ── Checkbox ── */
.stCheckbox label p {
    color: #FFFFFF !important;
}

/* ── File Uploader ── */
section[data-testid="stFileUploader"] {
    border: 2px dashed var(--glass-border) !important;
    border-radius: 14px !important;
    background: var(--glass) !important;
    padding: .8rem !important;
}
section[data-testid="stFileUploader"] label,
section[data-testid="stFileUploader"] span,
section[data-testid="stFileUploader"] small {
    color: #FFFFFF !important;
}

/* ── Select Slider ── */
.stSelectSlider label p {
    color: #FFFFFF !important;
}
.stSelectSlider div[data-baseweb="slider"] {
    color: #FFFFFF !important;
}

/* ── Progress ── */
.stProgress>div>div>div {
    background: linear-gradient(135deg, #7C73FF, #FF6584) !important;
}
.stProgress div[role="progressbar"] p,
.stProgress p {
    color: #FFFFFF !important;
}

/* ── Success / Warning / Info / Error ── */
.stSuccess { border-radius: 12px !important; }
.stSuccess p, .stSuccess div { color: #1B7A3D !important; }
.stWarning { border-radius: 12px !important; }
.stWarning p, .stWarning div { color: #8B6914 !important; }
.stError   { border-radius: 12px !important; }
.stError p, .stError div { color: #C53030 !important; }
.stInfo    { border-radius: 12px !important; }
.stInfo p, .stInfo div { color: #2B6CB0 !important; }

/* ── Markdown rendered text ── */
.stMarkdown p, .stMarkdown li, .stMarkdown span,
.stMarkdown strong, .stMarkdown em, .stMarkdown h1,
.stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    color: #FFFFFF !important;
}
.stMarkdown code {
    color: #FFD93D !important;
    background: rgba(255,255,255,0.08) !important;
    padding: 2px 6px;
    border-radius: 4px;
}
.stMarkdown pre {
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
}

/* ── Divider ── */
hr { border-color: var(--glass-border) !important; }

/* ── Download Button ── */
.stDownloadButton>button {
    background: linear-gradient(135deg, #00D68F, #0EA5E9) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
.stDownloadButton>button p,
.stDownloadButton>button span {
    color: #FFFFFF !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--glass-border); border-radius: 4px; }

/* ── Keyframes ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-18px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Spinner text ── */
.stSpinner p {
    color: #FFFFFF !important;
}

/* ── Responsive ── */
@media (max-width: 768px) {
    .main-title { font-size: 1.7rem !important; }
    .stat-num   { font-size: 1.2rem; }
    .glass-card { padding: .8rem; }
    .block-container { padding: .6rem .8rem; }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 3. API SETUP — ONLY gemini-3.5-flash
# ══════════════════════════════════════════════════════════════
genai.configure(api_key=st.secrets["API_KEY"])

MODEL_MAP = {
    "⚡ Flash (Fast)": "gemini-3.5-flash",
    "🧠 Pro  (Smart)": "gemini-1.5-pro",
    "🚀 Flash Lite":   "gemini-2.0-flash-lite",
}

# ══════════════════════════════════════════════════════════════
# 4. SUBJECT DATA (SSC 9th — Maharashtra Board)
# ══════════════════════════════════════════════════════════════
SUBJECT_CHAPTERS = {
    "History": [
        "1. Sources of History",
        "2. India : Events after 1960",
        "3. India's Internal Challenges",
        "4. Economic Development",
        "5. Education",
        "6. Empowerment of Women",
        "7. Post-Cold War World",
    ],
    "Geography": [
        "1. Distributional Maps",
        "2. Endogenetic Movements",
        "3. Exogenetic Movements – 1",
        "4. Exogenetic Movements – 2",
        "5. Precipitation",
        "6. Properties of Sea Water",
        "7. International Trade",
        "8. Map Scale",
    ],
    "Science": [
        "1. Laws of Motion",
        "2. Work and Energy",
        "3. Current Electricity",
        "4. Measurement of Matter",
        "5. Acids, Bases and Salts",
        "6. Classification of Plants",
        "7. Energy Flow in Ecosystem",
        "8. Useful Micro-organisms",
        "9. Environmental Management",
        "10. Information Communication Technology",
        "11. Carbon: An Important Element",
        "12. Study of Sound",
    ],
    "Maths": [
        "1. Sets",
        "2. Real Numbers",
        "3. Polynomials",
        "4. Ratio and Proportion",
        "5. Linear Equations in Two Variables",
        "6. Financial Planning",
        "7. Statistics",
        "8. Trigonometry",
        "9. Surface Area and Volume",
    ],
    "English": [
        "1. Life",
        "2. A Synopsis – The Swiss Family Robinson",
        "3. Have you ever seen…?",
        "4. Have you thought of the verb 'have'…?",
        "5. The Necklace",
        "6. Invictus",
        "7. Nobody's Friend",
        "8. The Fall of Troy",
        "9. Autumn",
        "10. The Past in the Present",
        "11. Silver",
        "12. An Epitome of Courage",
        "13. A True Test of Cricket",
        "14. Reading Works of Art",
        "15. Four Poems on 'Sea'",
        "16. A Letter to Living",
        "17. The Road Not Taken",
    ],
}

SUBJECT_ICONS  = {"History":"📜","Geography":"🌍","Science":"🔬","Maths":"📐","English":"📖"}
SUBJECT_COLORS = {"History":"#FF6B6B","Geography":"#4ECDC4","Science":"#7C73FF","Maths":"#FFD93D","English":"#FF6584"}

# ══════════════════════════════════════════════════════════════
# 5. PERSISTENT STORAGE (JSON File)
# ══════════════════════════════════════════════════════════════
SAVE_FILE = "jayesh_tutorial_data.json"

def load_saved_data():
    """Load saved chat + stats from JSON file"""
    default = {
        "messages": [],
        "total_q": 0,
        "total_tests": 0,
        "subject_hist": {s: 0 for s in SUBJECT_CHAPTERS},
        "session_ts": datetime.now().strftime("%d %b %Y · %I:%M %p"),
        "selected_subject": "Science",
    }
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            # Merge with defaults in case new fields added
            for k, v in default.items():
                if k not in saved:
                    saved[k] = v
            # Ensure all subjects exist in hist
            for s in SUBJECT_CHAPTERS:
                if s not in saved["subject_hist"]:
                    saved["subject_hist"][s] = 0
            return saved
        except Exception:
            return default
    return default

def save_data_to_file():
    """Save current session state to JSON file"""
    try:
        data = {
            "messages": st.session_state.messages,
            "total_q": st.session_state.total_q,
            "total_tests": st.session_state.total_tests,
            "subject_hist": st.session_state.subject_hist,
            "session_ts": st.session_state.session_ts,
            "selected_subject": st.session_state.selected_subject,
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        pass  # Silently fail — don't break the app

# ══════════════════════════════════════════════════════════════
# 6. SESSION STATE INIT (from saved file)
# ══════════════════════════════════════════════════════════════
def init_state():
    saved = load_saved_data()
    defaults = {
        "messages": saved["messages"],
        "total_q": saved["total_q"],
        "total_tests": saved["total_tests"],
        "subject_hist": saved["subject_hist"],
        "session_ts": saved.get("session_ts", datetime.now().strftime("%d %b %Y · %I:%M %p")),
        "selected_subject": saved.get("selected_subject", "Science"),
        "needs_save": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ══════════════════════════════════════════════════════════════
# 7. PERSONA & HELPERS
# ══════════════════════════════════════════════════════════════
def get_persona(subject=None):
    p = """You are **Jayesh Sir**, a passionate 9th-SSC (Maharashtra Board) tutor.
RULES:
• Start EVERY reply with 'Jayesh Sir:- '
• Be warm, encouraging, and use emojis 🎯
• Use bullet points, numbered steps, and bold **keywords**
• Sprinkle Hindi/Marathi words for connect (e.g., "Bahut accha!", "Chalo samajhte hain")
• For Maths → step-by-step solutions with formula boxes
• For Science → real-life analogies + diagram descriptions
• For History/Geography → memory tricks, mnemonics, timeline flows
• For English → grammar rules with examples, vocabulary tips
• Always link answers to SSC Board exam patterns & marks distribution
• If student is wrong → gently correct with appreciation for trying
• End with a motivational line or a follow-up question"""
    if subject:
        p += f"\n• Currently teaching: **{subject}**"
    return p

def call_gemini(prompt, image=None, model_key="gemini-3.5-flash"):
    try:
        model = genai.GenerativeModel(model_key)
        if image:
            resp = model.generate_content([prompt, image])
        else:
            resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        return f"Jayesh Sir:- Oops! Kuch technical issue aa gaya 😅\n```\n{e}\n```"

def export_chat_text():
    if not st.session_state.messages:
        return ""
    txt  = f"📚 Jayesh Tutorial — Chat Export\n📅 {st.session_state.session_ts}\n{'='*55}\n\n"
    for m in st.session_state.messages:
        who = "👨‍🎓 Student" if m["role"] == "user" else "👨‍🏫 Jayesh Sir"
        txt += f"{who}:\n{m['content']}\n\n{'─'*45}\n\n"
    return txt

QUICK_PROMPTS = {
    "History":  ["📌 Important dates & events","🧠 Memory tricks & mnemonics","📝 Board expected questions","💡 Explain main theme simply"],
    "Geography":["🗺️ Map-pointing practice","📌 Key terms & definitions","📝 Board expected questions","💡 Real-life examples"],
    "Science":  ["🧪 Real-life analogies","📝 Board expected questions","🔬 Diagram / experiment tips","💡 Quick revision points"],
    "Maths":    ["📐 Step-by-step formula guide","📝 Board expected questions","🧮 Practice problems + solutions","⚠️ Common mistakes to avoid"],
    "English":  ["📖 Chapter summary & theme","📝 Board expected questions","✍️ Grammar rules + examples","💡 Important vocabulary & idioms"],
}

TIPS = [
    "📖 Read the chapter once *before* class — you'll understand 2× better!",
    "📝 Write answers in points — Board examiners love structured answers!",
    "🧠 Use the Pomodoro technique: 25 min study → 5 min break",
    "📐 For Maths: solve 5 problems daily — consistency beats cramming!",
    "🎯 Highlight keywords in your textbook — helps in quick revision",
    "⏰ Solve previous-year papers under exam conditions",
    "💪 Never skip diagrams in Science — they carry marks!",
    "📚 Make flashcards for History dates — review them daily",
    "🌙 Revise before sleeping — your brain consolidates during sleep!",
    "✍️ Write mock answers — writing practice improves speed & presentation!",
]

# ══════════════════════════════════════════════════════════════
# 8. HEADER & STATS
# ══════════════════════════════════════════════════════════════
st.markdown('<h1 class="main-title">🎓 Jayesh Tutorial — SSC Genius AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your personal AI tutor for 9th SSC Board &nbsp;|&nbsp; Powered by Gemini ✨</p>', unsafe_allow_html=True)

s1, s2, s3, s4, s5 = st.columns(5)
with s1:
    st.markdown(f'<div class="stat-card"><div class="stat-num">{st.session_state.total_q}</div><div class="stat-lbl">Questions</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown(f'<div class="stat-card"><div class="stat-num">{st.session_state.total_tests}</div><div class="stat-lbl">Tests</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown(f'<div class="stat-card"><div class="stat-num">{len(st.session_state.messages)}</div><div class="stat-lbl">Messages</div></div>', unsafe_allow_html=True)
with s4:
    fav = max(st.session_state.subject_hist, key=st.session_state.subject_hist.get) if any(st.session_state.subject_hist.values()) else "—"
    st.markdown(f'<div class="stat-card"><div class="stat-num">{SUBJECT_ICONS.get(fav,"📚")}</div><div class="stat-lbl">Top Subject</div></div>', unsafe_allow_html=True)
with s5:
    st.markdown(f'<div class="stat-card"><div class="stat-num">9th</div><div class="stat-lbl">SSC Board</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════
# 9. THREE-COLUMN LAYOUT
# ══════════════════════════════════════════════════════════════
col_left, col_center, col_right = st.columns([1.1, 2.6, 0.75])

# ────────────────── LEFT PANEL ──────────────────
with col_left:

    # ── Subject ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">📚 Subject</div>', unsafe_allow_html=True)
    for sub in SUBJECT_CHAPTERS:
        if st.button(f"{SUBJECT_ICONS[sub]}  {sub}", key=f"sub_{sub}", use_container_width=True):
            st.session_state.selected_subject = sub
            save_data_to_file()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    sel_sub = st.session_state.selected_subject

    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

    # ── Chapter ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">📖 Chapter</div>', unsafe_allow_html=True)
    chapter = st.selectbox("Pick chapter", SUBJECT_CHAPTERS[sel_sub], key="chap_sel", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

    # ── Settings ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">⚙️ Settings</div>', unsafe_allow_html=True)
    difficulty = st.selectbox("Difficulty", ["Easy 🟢","Medium 🟡","Hard 🔴"], index=1)
    model_lbl  = st.selectbox("AI Model", list(MODEL_MAP.keys()), index=0)
    model_key  = MODEL_MAP[model_lbl]
    st.markdown('</div>', unsafe_allow_html=True)

# ────────────────── CENTER PANEL ──────────────────
with col_center:

    tab_chat, tab_test, tab_summary, tab_doubt = st.tabs([
        "💬 Chat",
        "📝 Test Generator",
        "🧠 Quick Summary",
        "📸 Doubt Solver",
    ])

    # ═══════ TAB 1 — CHAT ═══════
    with tab_chat:
        st.markdown("### 💬 Chat with Jayesh Sir")

        # Quick prompts
        st.markdown("**⚡ Quick Prompts**")
        qp = QUICK_PROMPTS[sel_sub]
        q1, q2 = st.columns(2)
        for i, q in enumerate(qp):
            with (q1 if i % 2 == 0 else q2):
                if st.button(q, key=f"qp{i}", use_container_width=True):
                    st.session_state["prefill"] = q

        # Chat history
        chat_box = st.container()
        with chat_box:
            for m in st.session_state.messages:
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])

        # Input
        prefill = st.session_state.pop("prefill", "")
        if prompt := st.chat_input("Ask Jayesh Sir anything… 💭"):
            st.session_state.subject_hist[sel_sub] += 1
            st.session_state.total_q += 1

            full = f"{prefill}\n{prompt}" if prefill else prompt

            st.session_state.messages.append({"role": "user", "content": prompt})
            save_data_to_file()

            with chat_box:
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    with st.spinner("👨‍🏫 Jayesh Sir is thinking…"):
                        ai_prompt = (
                            f"{get_persona(sel_sub)}\n"
                            f"Subject: {sel_sub} | Chapter: {chapter} | Difficulty: {difficulty}\n"
                            f"Student Query: {full}"
                        )
                        resp = call_gemini(ai_prompt, model_key=model_key)
                        st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp})
                save_data_to_file()

    # ═══════ TAB 2 — TEST GENERATOR ═══════
    with tab_test:
        st.markdown("### 📝 Test Paper Generator")

        tc1, tc2 = st.columns(2)
        with tc1:
            test_chap  = st.text_input("📖 Chapter Name", value=chapter)
            test_marks = st.number_input("📊 Total Marks", 5, 100, 20, step=5)
        with tc2:
            test_type = st.selectbox("Question Type", [
                "All Mixed",
                "Short Answer (2-3 marks)",
                "Long Answer (5 marks)",
                "Fill in the Blanks (1 mark)",
                "Match the Following",
                "True or False",
                "Multiple Choice (MCQ)",
            ])
            ans_key = st.checkbox("✅ Include Answer Key", value=True)

        test_diff = st.select_slider("🎯 Difficulty", options=["Easy","Medium","Hard"], value="Medium")

        if st.button("🚀 Generate Test Paper", use_container_width=True, type="primary"):
            if test_chap:
                st.session_state.total_tests += 1
                save_data_to_file()
                with st.spinner("👨‍🏫 Jayesh Sir is preparing your test…"):
                    ans_note = "Include a DETAILED ANSWER KEY at the end." if ans_key else "Do NOT include answers."
                    tp = (
                        f"{get_persona(sel_sub)}\n\n"
                        f"Generate a COMPLETE, NEW, UNIQUE test paper:\n"
                        f"📚 Subject: {sel_sub}\n"
                        f"📖 Chapter: {test_chap}\n"
                        f"📊 Total Marks: {test_marks}\n"
                        f"📝 Question Type: {test_type}\n"
                        f"🎯 Difficulty: {test_diff}\n"
                        f"✅ {ans_note}\n\n"
                        f"Format professionally:\n"
                        f"• Header: Subject / Chapter / Total Marks / Time\n"
                        f"• Clear numbering & marks per question\n"
                        f"• Proper spacing\n"
                        f"• Follow SSC Board pattern strictly\n"
                    )
                    resp = call_gemini(tp, model_key=model_key)
                    st.session_state.messages.append({"role": "assistant", "content": f"📋 **Test Paper — {test_chap}**\n\n{resp}"})
                    save_data_to_file()
                    st.markdown(resp)

                    st.download_button(
                        "📥 Download Test Paper",
                        data=resp,
                        file_name=f"Test_{sel_sub}_{test_chap}_{test_marks}m.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                    st.success("✅ Test paper ready!")
            else:
                st.warning("⚠️ Enter chapter name first!")

    # ═══════ TAB 3 — QUICK SUMMARY ═══════
    with tab_summary:
        st.markdown(f"### 🧠 Quick Summary — {SUBJECT_ICONS[sel_sub]} {chapter}")

        sum_style = st.selectbox("Summary Style", [
            "📊 Bullet Points",
            "🧠 Mind Map (text)",
            "📝 Detailed Notes",
            "🎯 Exam Crash Course (1-page)",
            "❓ FAQ Style",
            "🏷️ Keyword Flashcards",
        ])

        if st.button("🧠 Generate Summary", use_container_width=True, type="primary"):
            with st.spinner("👨‍🏫 Jayesh Sir is creating your summary…"):
                sp = (
                    f"{get_persona(sel_sub)}\n\n"
                    f"Create a comprehensive summary:\n"
                    f"📚 Subject: {sel_sub}\n"
                    f"📖 Chapter: {chapter}\n"
                    f"📋 Style: {sum_style}\n\n"
                    f"Make it:\n"
                    f"• Easy to remember & exam-focused\n"
                    f"• Include mnemonics / memory tricks\n"
                    f"• Bold **keywords**\n"
                    f"• SSC Board exam tips\n"
                )
                resp = call_gemini(sp, model_key=model_key)
                st.session_state.messages.append({"role": "assistant", "content": f"🧠 **Summary — {chapter}**\n\n{resp}"})
                save_data_to_file()
                st.markdown(resp)

                st.download_button(
                    "📥 Download Summary",
                    data=resp,
                    file_name=f"Summary_{sel_sub}_{chapter}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

    # ═══════ TAB 4 — DOUBT SOLVER (IMAGE) ═══════
    with tab_doubt:
        st.markdown("### 📸 Doubt Solver — Upload Image")
        img_file = st.file_uploader("Upload a photo of your question / diagram", type=["jpg","jpeg","png"], key="doubt_img")
        doubt_txt = st.text_input("Any extra context? (optional)", placeholder="e.g. 'Explain step 3' or 'Why is this answer X?'")

        if st.button("🔍 Solve Doubt", use_container_width=True, type="primary"):
            if img_file:
                with st.spinner("👨‍🏫 Jayesh Sir is reading your image…"):
                    image = Image.open(img_file)
                    dp = (
                        f"{get_persona(sel_sub)}\n\n"
                        f"The student has uploaded an image of a question/diagram.\n"
                        f"Subject: {sel_sub} | Chapter: {chapter}\n"
                        f"Extra context: {doubt_txt if doubt_txt else 'None'}\n\n"
                        f"Look at the image carefully and:\n"
                        f"1. Identify the question/topic\n"
                        f"2. Explain step-by-step\n"
                        f"3. Give exam tips related to this topic\n"
                    )
                    resp = call_gemini(dp, image=image, model_key=model_key)
                    st.session_state.messages.append({"role": "assistant", "content": f"📸 **Doubt Solved!**\n\n{resp}"})
                    save_data_to_file()
                    st.markdown(resp)
            else:
                st.warning("⚠️ Please upload an image first!")

# ────────────────── RIGHT PANEL ──────────────────
with col_right:

    # ── Actions ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">🛠️ Actions</div>', unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        save_data_to_file()
        st.rerun()

    chat_exp = export_chat_text()
    if chat_exp:
        st.download_button(
            "📥 Export Chat",
            data=chat_exp,
            file_name=f"Jayesh_Chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

    # ── Daily Tip ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">💡 Tip of the Day</div>', unsafe_allow_html=True)
    st.info(f"Jayesh Sir says:\n\n{random.choice(TIPS)}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

    # ── Subject Progress ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">📊 Usage</div>', unsafe_allow_html=True)
    for sub, cnt in st.session_state.subject_hist.items():
        if cnt > 0:
            pct = min(cnt / 10, 1.0)
            st.progress(pct, text=f"{SUBJECT_ICONS[sub]} {sub} ({cnt})")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

    # ── About ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">ℹ️ About</div>', unsafe_allow_html=True)
    st.caption(
        "🎓 Jayesh Tutorial\n"
        "📱 SSC 9th Board Prep\n"
        "🤖 Powered by Gemini AI\n"
        f"🕐 Session: {st.session_state.session_ts}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 10. AUTO-SAVE ON PAGE RERUN (safety net)
# ══════════════════════════════════════════════════════════════
save_data_to_file()

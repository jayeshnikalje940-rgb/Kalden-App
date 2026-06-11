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
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════
# 2. COMPLETE CSS — SIDEBAR STYLE + TEXT VISIBLE
# ══════════════════════════════════════════════════════════════
custom_css = """
<style>
/* ── Hide Defaults ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Root Colors ── */
:root {
    --primary: #7C73FF;
    --primary-glow: rgba(124,115,255,0.4);
    --secondary: #FF6584;
    --accent: #00D68F;
    --bg-dark: #0F0F1E;
    --bg-sidebar: #161630;
    --glass: rgba(255,255,255,0.06);
    --glass-border: rgba(255,255,255,0.12);
    --text-primary: #FFFFFF;
    --text-secondary: #B8B8D4;
    --text-dim: #7878A0;
}

/* ── Main App Background ── */
.stApp {
    background: var(--bg-dark) !important;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 600px 600px at 20% 80%, rgba(124,115,255,0.10) 0%, transparent 70%),
        radial-gradient(ellipse 500px 500px at 80% 20%, rgba(255,101,132,0.07) 0%, transparent 70%),
        radial-gradient(ellipse 400px 400px at 50% 50%, rgba(0,214,143,0.05) 0%, transparent 70%);
    z-index: -1;
    pointer-events: none;
}

/* ── GLOBAL TEXT FIX — SAB KUCH WHITE ── */
.stApp, .stApp p, .stApp span, .stApp label,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stApp li, .stApp strong, .stApp em, .stApp a,
.stApp th, .stApp td, .stApp small {
    color: var(--text-primary) !important;
}

.stApp .stCaption {
    color: var(--text-secondary) !important;
}

/* ── SIDEBAR STYLING ── */
[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--glass-border) !important;
    min-width: 280px !important;
    max-width: 320px !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.2rem 1rem !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] strong {
    color: #FFFFFF !important;
}

/* Sidebar section headers */
.sidebar-header {
    font-size: 0.80rem;
    font-weight: 700;
    color: var(--primary) !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 1.2rem 0 0.5rem 0;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid var(--glass-border);
}

/* ── Block Container ── */
.block-container {
    padding: 1.5rem 2.5rem 2rem !important;
    max-width: 1400px;
}

/* ── Title ── */
.main-title {
    font-size: 2.6rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #7C73FF 0%, #FF6584 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-align: center;
    line-height: 1.2 !important;
    margin-bottom: 0.1rem !important;
}
.subtitle {
    text-align: center;
    color: var(--text-dim) !important;
    font-size: 0.90rem;
    margin-bottom: 1rem;
}

/* ── Stat Cards Row ── */
.stat-row {
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 0.8rem;
}
.stat-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 0.6rem 1.2rem;
    text-align: center;
    min-width: 100px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(124,115,255,0.15);
}
.stat-num {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7C73FF, #FF6584);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.3;
}
.stat-lbl {
    font-size: 0.60rem;
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
    padding: 0.50rem 1rem !important;
    transition: all 0.25s !important;
    white-space: nowrap;
    font-size: 0.90rem !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 18px var(--primary-glow) !important;
}
.stButton>button p, .stButton>button span {
    color: #FFFFFF !important;
}

/* Subject button active state */
.subject-active > button {
    background: linear-gradient(135deg, #00D68F, #0EA5E9) !important;
    box-shadow: 0 0 20px rgba(0,214,143,0.3) !important;
}

/* ── Chat Messages ── */
.stChatMessage {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 14px !important;
    padding: 0.9rem !important;
    margin-bottom: 0.4rem !important;
}
.stChatMessage p, .stChatMessage span, .stChatMessage div,
.stChatMessage li, .stChatMessage strong, .stChatMessage em,
.stChatMessage h1, .stChatMessage h2, .stChatMessage h3,
.stChatMessage h4, .stChatMessage td, .stChatMessage th {
    color: #FFFFFF !important;
}
.stChatMessage code {
    color: #FFD93D !important;
    background: rgba(255,255,255,0.08) !important;
}
.stChatMessage pre {
    background: rgba(0,0,0,0.35) !important;
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
    font-size: 1rem !important;
}
.stChatInput textarea::placeholder {
    color: var(--text-dim) !important;
}

/* ── Text / Number Inputs ── */
.stTextInput>div>div>input,
.stNumberInput>div>div>input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid var(--glass-border) !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    caret-color: #7C73FF !important;
    font-size: 0.95rem !important;
}
.stTextInput>div>div>input::placeholder {
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
    border: 1px solid var(--glass-border) !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
}
.stSelectbox>div>div>div {
    color: #FFFFFF !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 5px;
    background: var(--glass);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--glass-border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--text-dim) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 6px 14px !important;
}
.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: #FFFFFF !important;
}
.stTabs [aria-selected="true"] p {
    color: #FFFFFF !important;
}

/* ── Radio ── */
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
    padding: 0.8rem !important;
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

/* ── Progress ── */
.stProgress>div>div>div {
    background: linear-gradient(135deg, #7C73FF, #FF6584) !important;
}
.stProgress p {
    color: #FFFFFF !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
}
.streamlit-expanderHeader p {
    color: #FFFFFF !important;
}

/* ── Success / Warning / Info / Error ── */
.stSuccess {
    border-radius: 12px !important;
    background: rgba(0,214,143,0.15) !important;
    border: 1px solid rgba(0,214,143,0.3) !important;
}
.stSuccess p { color: #00D68F !important; }

.stWarning {
    border-radius: 12px !important;
    background: rgba(255,211,61,0.15) !important;
    border: 1px solid rgba(255,211,61,0.3) !important;
}
.stWarning p { color: #FFD93D !important; }

.stError {
    border-radius: 12px !important;
    background: rgba(239,68,68,0.15) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
}
.stError p { color: #EF4444 !important; }

.stInfo {
    border-radius: 12px !important;
    background: rgba(124,115,255,0.12) !important;
    border: 1px solid rgba(124,115,255,0.25) !important;
}
.stInfo p { color: #7C73FF !important; }

/* ── Markdown text ── */
.stMarkdown p, .stMarkdown li, .stMarkdown span,
.stMarkdown strong, .stMarkdown em,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    color: #FFFFFF !important;
}
.stMarkdown code {
    color: #FFD93D !important;
    background: rgba(255,255,255,0.08) !important;
    padding: 2px 6px;
    border-radius: 4px;
}

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

/* ── Divider ── */
hr {
    border-color: var(--glass-border) !important;
    margin: 0.6rem 0 !important;
}

/* ── Spinner ── */
.stSpinner p {
    color: #FFFFFF !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--glass-border); border-radius: 4px; }

/* ── Sidebar Toggle Button ── */
button[kind="header"] {
    display: none !important;
}

/* ── Responsive ── */
@media (max-width: 768px) {
    .main-title { font-size: 1.6rem !important; }
    .stat-num { font-size: 1.1rem; }
    .block-container { padding: 0.5rem 0.8rem !important; }
    .stat-card { min-width: 70px; padding: 0.4rem 0.6rem; }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 3. API SETUP — gemini-3.5-flash ONLY
# ══════════════════════════════════════════════════════════════
genai.configure(api_key=st.secrets["API_KEY"])

# ══════════════════════════════════════════════════════════════
# 4. SUBJECT DATA
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

SUBJECT_ICONS = {"History":"📜","Geography":"🌍","Science":"🔬","Maths":"📐","English":"📖"}

# ══════════════════════════════════════════════════════════════
# 5. PERSISTENT STORAGE
# ══════════════════════════════════════════════════════════════
SAVE_FILE = "jayesh_tutorial_data.json"

def load_saved_data():
    default = {
        "messages": [],
        "total_q": 0,
        "total_tests": 0,
        "subject_hist": {s: 0 for s in SUBJECT_CHAPTERS},
        "selected_subject": "Science",
    }
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            for k, v in default.items():
                if k not in saved:
                    saved[k] = v
            for s in SUBJECT_CHAPTERS:
                if s not in saved.get("subject_hist", {}):
                    saved["subject_hist"][s] = 0
            return saved
        except Exception:
            return default
    return default

def save_data():
    try:
        data = {
            "messages": st.session_state.messages,
            "total_q": st.session_state.total_q,
            "total_tests": st.session_state.total_tests,
            "subject_hist": st.session_state.subject_hist,
            "selected_subject": st.session_state.selected_subject,
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# ══════════════════════════════════════════════════════════════
# 6. SESSION STATE
# ══════════════════════════════════════════════════════════════
def init_state():
    saved = load_saved_data()
    for k, v in {
        "messages": saved["messages"],
        "total_q": saved["total_q"],
        "total_tests": saved["total_tests"],
        "subject_hist": saved["subject_hist"],
        "selected_subject": saved.get("selected_subject", "Science"),
    }.items():
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

def call_gemini(prompt, image=None):
    try:
        model = genai.GenerativeModel("gemini-3.5-flash")
        if image:
            resp = model.generate_content([prompt, image])
        else:
            resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        return f"Jayesh Sir:- Oops! Technical issue 😅\n```\n{e}\n```"

def export_chat():
    if not st.session_state.messages:
        return ""
    txt = f"📚 Jayesh Tutorial — Chat Export\n📅 {datetime.now().strftime('%d %b %Y · %I:%M %p')}\n{'='*55}\n\n"
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
    "🧠 Use Pomodoro technique: 25 min study → 5 min break",
    "📐 For Maths: solve 5 problems daily — consistency beats cramming!",
    "🎯 Highlight keywords — helps in quick revision",
    "⏰ Solve previous-year papers under exam conditions",
    "💪 Never skip diagrams in Science — they carry marks!",
    "📚 Make flashcards for History dates — review daily",
    "🌙 Revise before sleeping — brain consolidates during sleep!",
    "✍️ Write mock answers — practice improves speed & presentation!",
]

# ══════════════════════════════════════════════════════════════
# 8. SIDEBAR — SUBJECTS + CHAPTERS + SETTINGS
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎓 Jayesh Tutorial")
    st.caption("SSC 9th Board • AI Tutor")

    st.markdown('<p class="sidebar-header">📚 SELECT SUBJECT</p>', unsafe_allow_html=True)

    for sub in SUBJECT_CHAPTERS:
        is_active = st.session_state.selected_subject == sub
        btn_key = f"sub_btn_{sub}"
        if st.button(
            f"{'✅' if is_active else SUBJECT_ICONS[sub]}  {sub}",
            key=btn_key,
            use_container_width=True,
        ):
            st.session_state.selected_subject = sub
            save_data()
            st.rerun()

    sel_sub = st.session_state.selected_subject

    st.markdown('<p class="sidebar-header">📖 SELECT CHAPTER</p>', unsafe_allow_html=True)
    chapter = st.selectbox(
        "Chapter",
        SUBJECT_CHAPTERS[sel_sub],
        key="chap_sel",
        label_visibility="collapsed"
    )

    st.markdown('<p class="sidebar-header">⚙️ SETTINGS</p>', unsafe_allow_html=True)
    difficulty = st.selectbox("Difficulty", ["Easy 🟢","Medium 🟡","Hard 🔴"], index=1)

    st.markdown("---")

    # ── Stats in Sidebar ──
    st.markdown('<p class="sidebar-header">📊 YOUR STATS</p>', unsafe_allow_html=True)
    st.markdown(f"**💬 Questions Asked:** {st.session_state.total_q}")
    st.markdown(f"**📝 Tests Generated:** {st.session_state.total_tests}")
    st.markdown(f"**📜 Total Messages:** {len(st.session_state.messages)}")

    fav = max(st.session_state.subject_hist, key=st.session_state.subject_hist.get) if any(st.session_state.subject_hist.values()) else None
    if fav:
        st.markdown(f"**🏆 Top Subject:** {SUBJECT_ICONS[fav]} {fav}")

    # Subject usage bars
    for sub, cnt in st.session_state.subject_hist.items():
        if cnt > 0:
            pct = min(cnt / 10, 1.0)
            st.progress(pct, text=f"{SUBJECT_ICONS[sub]} {sub} ({cnt})")

    st.markdown("---")

    # ── Actions ──
    st.markdown('<p class="sidebar-header">🛠️ ACTIONS</p>', unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        save_data()
        st.rerun()

    chat_exp = export_chat()
    if chat_exp:
        st.download_button(
            "📥 Export Chat",
            data=chat_exp,
            file_name=f"Jayesh_Chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("---")
    st.info(f"💡 **Tip:** {random.choice(TIPS)}")

# ══════════════════════════════════════════════════════════════
# 9. MAIN AREA — HEADER + TABS
# ══════════════════════════════════════════════════════════════
st.markdown('<h1 class="main-title">🎓 Jayesh Tutorial — SSC Genius AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your personal AI tutor for 9th SSC Board | Powered by Gemini ✨</p>', unsafe_allow_html=True)

# Stats row (HTML for clean look)
st.markdown(f"""
<div class="stat-row">
    <div class="stat-card">
        <div class="stat-num">{st.session_state.total_q}</div>
        <div class="stat-lbl">Questions</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">{st.session_state.total_tests}</div>
        <div class="stat-lbl">Tests</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">{len(st.session_state.messages)}</div>
        <div class="stat-lbl">Messages</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">{SUBJECT_ICONS.get(fav if any(st.session_state.subject_hist.values()) else None, '📚')}</div>
        <div class="stat-lbl">Top Subject</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">9th</div>
        <div class="stat-lbl">SSC Board</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════
# 10. TABS
# ══════════════════════════════════════════════════════════════
tab_chat, tab_test, tab_summary, tab_doubt = st.tabs([
    "💬 Chat",
    "📝 Test Generator",
    "🧠 Quick Summary",
    "📸 Doubt Solver",
])

# ═══════ TAB 1 — CHAT ═══════
with tab_chat:
    st.markdown(f"### 💬 Chat with Jayesh Sir — {SUBJECT_ICONS[sel_sub]} {sel_sub}")

    # Quick prompts
    st.markdown("**⚡ Quick Prompts**")
    qp = QUICK_PROMPTS[sel_sub]
    q1, q2, q3, q4 = st.columns(4)
    cols_qp = [q1, q2, q3, q4]
    for i, q in enumerate(qp):
        with cols_qp[i]:
            if st.button(q, key=f"qp{i}", use_container_width=True):
                st.session_state["prefill"] = q

    # Chat history
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Chat input
    prefill = st.session_state.pop("prefill", "")
    if prompt := st.chat_input("Ask Jayesh Sir anything… 💭"):
        st.session_state.subject_hist[sel_sub] += 1
        st.session_state.total_q += 1

        full = f"{prefill}\n{prompt}" if prefill else prompt

        st.session_state.messages.append({"role": "user", "content": prompt})
        save_data()

        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("👨‍🏫 Jayesh Sir is thinking…"):
                ai_prompt = (
                    f"{get_persona(sel_sub)}\n"
                    f"Subject: {sel_sub} | Chapter: {chapter} | Difficulty: {difficulty}\n"
                    f"Student Query: {full}"
                )
                resp = call_gemini(ai_prompt)
                st.markdown(resp)

        st.session_state.messages.append({"role": "assistant", "content": resp})
        save_data()

# ═══════ TAB 2 — TEST GENERATOR ═══════
with tab_test:
    st.markdown(f"### 📝 Test Paper Generator — {SUBJECT_ICONS[sel_sub]} {sel_sub}")

    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        test_chap  = st.text_input("📖 Chapter Name", value=chapter)
    with tc2:
        test_marks = st.number_input("📊 Total Marks", 5, 100, 20, step=5)
    with tc3:
        test_type = st.selectbox("Question Type", [
            "All Mixed",
            "Short Answer (2-3 marks)",
            "Long Answer (5 marks)",
            "Fill in the Blanks (1 mark)",
            "Match the Following",
            "True or False",
            "Multiple Choice (MCQ)",
        ])

    ac1, ac2 = st.columns(2)
    with ac1:
        ans_key = st.checkbox("✅ Include Answer Key", value=True)
    with ac2:
        test_diff = st.select_slider("🎯 Difficulty", options=["Easy","Medium","Hard"], value="Medium")

    if st.button("🚀 Generate Test Paper", use_container_width=True, type="primary"):
        if test_chap:
            st.session_state.total_tests += 1
            save_data()
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
                resp = call_gemini(tp)
                st.session_state.messages.append({"role": "assistant", "content": f"📋 **Test Paper — {test_chap}**\n\n{resp}"})
                save_data()
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
            resp = call_gemini(sp)
            st.session_state.messages.append({"role": "assistant", "content": f"🧠 **Summary — {chapter}**\n\n{resp}"})
            save_data()
            st.markdown(resp)

            st.download_button(
                "📥 Download Summary",
                data=resp,
                file_name=f"Summary_{sel_sub}_{chapter}.txt",
                mime="text/plain",
                use_container_width=True,
            )

# ═══════ TAB 4 — DOUBT SOLVER ═══════
with tab_doubt:
    st.markdown(f"### 📸 Doubt Solver — {SUBJECT_ICONS[sel_sub]} {sel_sub}")

    dc1, dc2 = st.columns(2)
    with dc1:
        img_file = st.file_uploader("📸 Upload Question Image", type=["jpg","jpeg","png"], key="doubt_img")
    with dc2:
        doubt_txt = st.text_input("Extra context?", placeholder="e.g. 'Explain step 3'")

    if st.button("🔍 Solve Doubt", use_container_width=True, type="primary"):
        if img_file:
            with st.spinner("👨‍🏫 Jayesh Sir is reading your image…"):
                image = Image.open(img_file)
                dp = (
                    f"{get_persona(sel_sub)}\n\n"
                    f"The student uploaded an image of a question/diagram.\n"
                    f"Subject: {sel_sub} | Chapter: {chapter}\n"
                    f"Extra context: {doubt_txt if doubt_txt else 'None'}\n\n"
                    f"Look at the image carefully and:\n"
                    f"1. Identify the question/topic\n"
                    f"2. Explain step-by-step\n"
                    f"3. Give exam tips related to this topic\n"
                )
                resp = call_gemini(dp, image=image)
                st.session_state.messages.append({"role": "assistant", "content": f"📸 **Doubt Solved!**\n\n{resp}"})
                save_data()
                st.markdown(resp)
        else:
            st.warning("⚠️ Please upload an image first!")

# ══════════════════════════════════════════════════════════════
# 11. AUTO-SAVE
# ══════════════════════════════════════════════════════════════
save_data()

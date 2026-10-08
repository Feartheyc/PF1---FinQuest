import streamlit as st
import streamlit.components.v1 as components
from sidebar import render_sidebar
from utils import (
    img_to_base64, 
    render_interactive_dialogue, 
    render_language_selector, 
    t
)
from engine import init_game, try_apply_effects
from content import get_event_data, get_total_levels
from config import apply_custom_css
from leaderboard import render_leaderboard_ui
from phishing_game import render_phishing_game
from investmentsim import render_investmentsim

# ==========================================
# 1. APP CONFIGURATION & STATE INITIALIZATION
# ==========================================
st.set_page_config(page_title="Financial Journey", layout="wide", page_icon="🌏", initial_sidebar_state="collapsed")

if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = "English"

if "game" not in st.session_state: 
    st.session_state.game = {"state": "MAIN_MENU"}

apply_custom_css()

# ==========================================
# 2. MENU RENDERING FUNCTIONS
# ==========================================
def render_main_menu():
    st.markdown(f"""
        <div class="menu-header-box">
            <div class="menu-title">🌏 {t("FinLife")}</div>
            <div class="menu-subtitle">{t("A Financial Literacy RPG Journey")}</div>
        </div>
    """, unsafe_allow_html=True)

    _, col_center, _ = st.columns([1, 2.2, 1])
    with col_center:
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button(f"🚀 {t('START JOURNEY')}", use_container_width=True):
                st.session_state.game['state'] = "INTRO"
                st.rerun()
        with b_c2:
            if st.button(f"📜 {t('HOW TO PLAY')}", use_container_width=True):
                st.session_state.game['state'] = "TUTORIAL"
                st.rerun()

        b_c3, b_c4 = st.columns(2)
        with b_c3:
            if st.button(f"🛡️ {t('CYBER SHIELD')}", use_container_width=True):
                st.session_state.game['state'] = "CYBER_GAME"
                st.rerun()
        with b_c4:
            if st.button(f"❤️ {t('CREDITS')}", use_container_width=True):
                st.session_state.game['state'] = "CREDITS"
                st.rerun()

def render_credits():
    st.markdown(f'<div class="menu-title" style="font-size: 2.5rem; text-align:center;">{t("CREDITS")}</div>', unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div class="menu-card">
                <h3 style="color:#4ade80; margin-top:0;">{t("Developed By Team FinLife")}</h3>
                <p style="color:#94a3b8; font-size:0.85rem;">{t("Created for the Athrava Project Friday 2026")}</p>
                <hr style="border-color: #334155; margin: 15px 0;">
                <p style="text-align:left; font-size:0.9rem; line-height:1.6;">
                <b>• {t("Team")}:</b> Yuvraj Chavan, Akash Rana, Rishi Bhuta, Sufiyan Mukadam<br>
                <b>• {t("Tech Stack")}:</b> Python, Streamlit, Pandas, SQLite<br>
                <b>• {t("Features")}:</b> {t("RPG Gameplay, Stock Simulator, Cyber Safety")}<br>
                <b>• {t("Mission")}:</b> {t("Making financial literacy accessible to rural India.")}
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        if st.button(f"⬅ {t('BACK TO MENU')}", use_container_width=True):
            st.session_state.game['state'] = "MAIN_MENU"
            st.rerun()

def render_tutorial():
    st.markdown(f'<div class="menu-title" style="font-size: 2.5rem; text-align:center;">{t("HOW TO PLAY")}</div>', unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div class="menu-card" style="text-align: left;">
                <h4 style="color:#facc15; margin:0 0 5px 0;">1. {t("Choose Your Persona")}</h4>
                <p style="font-size:0.85rem; color:#cbd5e1; margin-bottom:12px;">{t("Select from Farmer, Student, Employee, or Founder. Each has unique financial challenges.")}</p>
                <h4 style="color:#facc15; margin:0 0 5px 0;">2. {t("Evaluate Hidden Risks")}</h4>
                <p style="font-size:0.85rem; color:#cbd5e1; margin-bottom:12px;">{t("Options only show direct cash flow. Hidden debts, interest traps, and prudence points update silently based on your choices.")}</p>
                <h4 style="color:#facc15; margin:0 0 5px 0;">3. {t("Dynamic Investable Capital")}</h4>
                <p style="font-size:0.85rem; color:#cbd5e1; margin-bottom:12px;">{t("Your Investable Pool expands with high prudence and savings, but shrinks under heavy stress.")}</p>
                <h4 style="color:#facc15; margin:0 0 5px 0;">4. {t("Avoid Debt & Burnout")}</h4>
                <p style="font-size:0.85rem; color:#cbd5e1; margin:0;">{t("If your Stress reaches 100%, you enter emergency restructuring. Keep liabilities low!")}</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        if st.button(f"⬅ {t('BACK TO MENU')}", use_container_width=True):
            st.session_state.game['state'] = "MAIN_MENU"
            st.rerun()

# ==========================================
# 3. HELPERS
# ==========================================
def format_effects(effects):
    if "cash" in effects and effects["cash"] != 0:
        val = effects["cash"]
        sign = "+" if val > 0 else "-"
        return f" ({sign}₹{abs(val):,})"
    return ""

def render_hud_content(p):
    ins_status = f"✅ {t('Active')}" if p.get('insurance') else f"❌ {t('None')}"
    return f"""
    <div class="hud-container">
        <div class="hud-item"><div class="hud-label">{t("ROLE")}</div><div class="hud-value">{t(p['persona'])}</div></div>
        <div class="hud-item"><div class="hud-label">{t("CASH")}</div><div class="hud-value money-val">₹{p['cash']:,}</div></div>
        <div class="hud-item"><div class="hud-label">{t("SAVINGS")}</div><div class="hud-value money-val">₹{p['savings']:,}</div></div>
        <div class="hud-item"><div class="hud-label">{t("DEBT")}</div><div class="hud-value debt-val">₹{p['loan']:,}</div></div>
        <div class="hud-item"><div class="hud-label">{t("INVEST POOL")}</div><div class="hud-value invest-val">₹{p.get('investments', 0):,}</div></div>
        <div class="hud-item"><div class="hud-label">{t("SCORE")}</div><div class="hud-value" style="color:#67e8f9;">{p.get('score_points', 0)} pts</div></div>
        <div class="hud-item"><div class="hud-label">{t("STRESS")}</div><div class="hud-value stress-val">{p['stress']}%</div></div>
        <div class="hud-item"><div class="hud-label">{t("INSURANCE")}</div><div class="hud-value ins-val">{ins_status}</div></div>
    </div>
    """

def render_mini_map(persona, current_lvl):
    total_levels = get_total_levels(persona)

    dots_html = ""
    for i in range(total_levels):
        if i < current_lvl:
            status = "completed"
            content = "✓"
        elif i == current_lvl:
            status = "active"
            content = ""
        else:
            status = "pending"
            content = ""

        dots_html += f"<div class='step {status}'>{content}</div>"

        if i < total_levels - 1:
            line_status = "line-active" if i < current_lvl else "line-pending"
            dots_html += f"<div class='step-line {line_status}'></div>"

    return f"""
<style>
    .progress-wrapper {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 12px 24px;
        margin-bottom: 24px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
    }}
    .step {{
        width: 24px; height: 24px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 11px;
        z-index: 2;
        transition: all 0.3s;
    }}
    .step.completed {{ background: #4ade80; color: #064e3b; box-shadow: 0 0 10px rgba(74, 222, 128, 0.4); }}
    .step.active {{ 
        background: #ef4444; border: 2px solid white; 
        box-shadow: 0 0 14px rgba(239, 68, 68, 0.8); 
        transform: scale(1.2);
    }}
    .step.pending {{ background: #1e293b; border: 2px solid #334155; }}

    .step-line {{
        flex-grow: 1;
        height: 3px;
        margin: 0 4px;
        border-radius: 2px;
    }}
    .line-active {{ background: #4ade80; }}
    .line-pending {{ background: #1e293b; }}
</style>
<div class="progress-wrapper">
    {dots_html}
</div>
"""

# ==========================================
# 4. SCENE RENDERING
# ==========================================
def render_persona_selection():
    st.markdown(f"<h2 style='text-align:center; margin-bottom: 2rem;'>🌏 {t('Select Your Persona')}</h2>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    chars = [
        {"col": c1, "role": "Farmer", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825021.png", "desc": "Crops, weather risks, seasonal credit.", "btn": "🚜 Select Farmer"},
        {"col": c2, "role": "Employee", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825038.png", "desc": "Fixed salary, lifestyle debt, health shocks.", "btn": "👔 Select Employee"},
        {"col": c3, "role": "Student", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825108.png", "desc": "Allowances, hardware crises, career forks.", "btn": "🎓 Select Student"},
        {"col": c4, "role": "Founder", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825072.png", "desc": "Cap tables, runway, unit economics.", "btn": "🚀 Select Founder"}
    ]
    for char in chars:
        with char["col"]:
            st.markdown(f'<div class="char-card"><img src="{char["img"]}" class="char-img"><h4>{t(char["role"])}</h4><p style="font-size:0.8rem; color:#94a3b8; margin-bottom:15px;">{char["desc"]}</p></div>', unsafe_allow_html=True)
            if st.button(char["btn"], key=f"sel_{char['role']}", use_container_width=True):
                st.session_state.game = init_game(char["role"])
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(f"⬅ {t('Back to Main Menu')}", use_container_width=True):
        st.session_state.game['state'] = "MAIN_MENU"
        st.rerun()

def render_map():
    p = st.session_state.game
    current_lvl = p['event_index']
    persona = p['persona']
    total_lvls = get_total_levels(persona)

    # Check for direct map node clicks
    if "select_level" in st.query_params:
        target = int(st.query_params["select_level"])
        del st.query_params["select_level"]
        if target <= current_lvl:
            p['event_index'] = target
            p['state'] = "PLAYING"
            st.rerun()

    st.markdown(render_hud_content(p), unsafe_allow_html=True)

    col_map, col_info = st.columns([3.4, 1.2], gap="large")

    with col_map:
        persona_map_files = {
            "Farmer": "assets/map_farmer.png",
            "Student": "assets/map_student.png",
            "Employee": "assets/map_business.png",
            "Founder": "assets/map_startup.png"
        }
        target_map_file = persona_map_files.get(persona, "assets/level_map.png")
        map_b64 = img_to_base64(target_map_file) or img_to_base64("assets/level_map.png")

        # Candy Crush style isometric coordinates along the path
        node_coords = [
            (22, 68),  # Level 1
            (32, 58),  # Level 2
            (42, 52),  # Level 3
            (52, 57),  # Level 4
            (68, 54),  # Level 5
            (72, 40),  # Level 6
            (56, 36),  # Level 7
            (38, 30),  # Level 8
            (26, 22),  # Level 9
        ]

        nodes_html = ""
        for i in range(total_lvls):
            x, y = node_coords[i] if i < len(node_coords) else (50, 50)
            lvl_num = i + 1

            if i < current_lvl:
                status = "completed"
                badge = "✓"
                click_action = f"onclick='parentSelect({i})'"
            elif i == current_lvl:
                status = "current"
                badge = f"{lvl_num}"
                click_action = f"onclick='parentSelect({i})'"
            else:
                status = "locked"
                badge = "🔒"
                click_action = ""

            nodes_html += f"""
            <div class="node-wrapper" style="left: {x}%; top: {y}%;" {click_action}>
                <div class="level-node {status}">
                    <span>{badge}</span>
                </div>
                <div class="level-label">Lvl {lvl_num}</div>
                {f'<div class="current-arrow">▼</div>' if status == 'current' else ''}
            </div>
            """

        components.html(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700;800&display=swap" rel="stylesheet">
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
                body {{ background: transparent; overflow: hidden; }}

                .map-stage {{
                    position: relative;
                    width: 100%;
                    height: 560px;
                    border-radius: 20px;
                    background-image: url('data:image/png;base64,{map_b64}');
                    background-size: cover;
                    background-position: center;
                    border: 2px solid rgba(255, 255, 255, 0.12);
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), inset 0 0 50px rgba(0, 0, 0, 0.3);
                }}

                .node-wrapper {{
                    position: absolute;
                    transform: translate(-50%, -50%);
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    cursor: pointer;
                    transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
                    z-index: 10;
                }}
                .node-wrapper:hover {{
                    transform: translate(-50%, -58%) scale(1.15);
                    z-index: 20;
                }}

                .level-node {{
                    width: 44px;
                    height: 44px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-family: 'Poppins', sans-serif;
                    font-weight: 800;
                    font-size: 16px;
                    box-shadow: 0 6px 0 rgba(0, 0, 0, 0.4), 0 10px 15px rgba(0, 0, 0, 0.4);
                    transition: all 0.2s ease;
                }}

                .level-node.completed {{
                    background: linear-gradient(135deg, #fbbf24, #f59e0b);
                    color: #78350f;
                    border: 3px solid #fef3c7;
                    box-shadow: 0 6px 0 #b45309, 0 10px 18px rgba(245, 158, 11, 0.5);
                }}

                .level-node.current {{
                    background: linear-gradient(135deg, #ef4444, #dc2626);
                    color: white;
                    border: 3px solid #ffffff;
                    box-shadow: 0 6px 0 #991b1b, 0 0 25px rgba(239, 68, 68, 0.9);
                    animation: pulseCurrent 1.5s infinite;
                }}

                .level-node.locked {{
                    background: linear-gradient(135deg, #334155, #1e293b);
                    color: #64748b;
                    border: 2px solid #475569;
                    box-shadow: 0 4px 0 #0f172a;
                    font-size: 13px;
                    cursor: not-allowed;
                }}

                .level-label {{
                    font-family: 'Poppins', sans-serif;
                    font-size: 10px;
                    font-weight: 800;
                    color: #ffffff;
                    background: rgba(15, 23, 42, 0.85);
                    padding: 2px 7px;
                    border-radius: 8px;
                    margin-top: 5px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    text-shadow: 0 1px 2px black;
                }}

                .current-arrow {{
                    position: absolute;
                    top: -26px;
                    color: #facc15;
                    font-size: 20px;
                    animation: floatArrow 0.8s infinite alternate ease-in-out;
                    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.8));
                }}

                @keyframes pulseCurrent {{
                    0% {{ transform: scale(1); box-shadow: 0 6px 0 #991b1b, 0 0 15px rgba(239, 68, 68, 0.6); }}
                    50% {{ transform: scale(1.1); box-shadow: 0 6px 0 #991b1b, 0 0 30px rgba(239, 68, 68, 1); }}
                    100% {{ transform: scale(1); box-shadow: 0 6px 0 #991b1b, 0 0 15px rgba(239, 68, 68, 0.6); }}
                }}

                @keyframes floatArrow {{
                    0% {{ transform: translateY(0); }}
                    100% {{ transform: translateY(-8px); }}
                }}
            </style>
        </head>
        <body>
            <div class="map-stage">
                {nodes_html}
            </div>
            <script>
                function parentSelect(lvlIndex) {{
                    const url = new URL(window.parent.location);
                    url.searchParams.set('select_level', lvlIndex);
                    window.parent.location.href = url.href;
                }}
            </script>
        </body>
        </html>
        """, height=575)

    with col_info:
        st.markdown(f"### 📍 {t('Current Level')} {current_lvl + 1}")
        evt = get_event_data(p['persona'], current_lvl)
        
        if evt:
            st.markdown(f"**{t(evt['title'])}**")
            st.caption(f"{t('NPC')}: {evt['avatar']} {t(evt['npc'])}")
            
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            if st.button(f"▶️ {t('Play Level')}", type="primary", use_container_width=True): 
                p['state'] = "PLAYING"
                st.rerun()
        else:
            if st.button(f"🏆 {t('Finish Journey')}", type="primary", use_container_width=True): 
                p['state'] = "END"
                st.rerun()

        st.markdown("---")
        st.markdown(f"#### 🏛️ {t('Financial Terminal')}")
        if st.button(f"📈 {t('Stock Market')}", use_container_width=True):
            st.session_state.cash = float(p.get('investments', 1000))
            st.session_state.username = p['persona']
            p['state'] = "MARKET"
            st.rerun()

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        if st.button(f"⬅ {t('Change Persona')}", use_container_width=True): 
            p['state'] = "INTRO"
            st.rerun()

def render_scene():
    p = st.session_state.game

    if p.get('stress', 0) >= 100:
        render_distress_screen(p)
        return

    evt = get_event_data(p['persona'], p['event_index'])
    if not evt: 
        p['state'] = "MAP"
        st.rerun()
        return

    render_sidebar(p)

    st.markdown(render_hud_content(p), unsafe_allow_html=True)
    st.markdown(render_mini_map(p['persona'], p['event_index']), unsafe_allow_html=True)

    if p.get('last_feedback'):
        st.markdown(f"<div class='game-alert alert-{p['feedback_type']}'>{t(p['last_feedback'])}</div>", unsafe_allow_html=True)
        p['last_feedback'] = None

    # Unified card without redundant empty container
    st.markdown('<div class="scene-card">', unsafe_allow_html=True)
    render_interactive_dialogue(evt["avatar"], evt["npc"], evt["story"])
    if "thought" in evt: 
        st.markdown(f'<div class="thought-bubble">💭 <b>{t("Inner Thought")}:</b> {t(evt["thought"])}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if "advisor" in evt:
        with st.expander(f"💡 {t('Financial Principle & Trade-off')}"):
            st.markdown(f"{t(evt['advisor'])}")

    if "choices" in evt:
        cols = st.columns(len(evt["choices"]), gap="medium")
        for i, (txt, eff) in enumerate(evt["choices"].items()):
            with cols[i]:
                btn_label = f"{t(txt)}{format_effects(eff)}"
                if st.button(btn_label, key=f"btn_{p['event_index']}_{i}", use_container_width=True):
                    msg = eff.pop('__msg', None)
                    success, s_msg = try_apply_effects(eff)
                    p['last_feedback'], p['feedback_type'] = (msg or s_msg), ("good" if success else "bad")
                    if success: 
                        p['event_index'] += 1
                    st.rerun()

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1.5, 8.5])
    with col_l:
        if st.button(f"🗺️ {t('Map')}", use_container_width=True): 
            p['state'] = "MAP"
            st.rerun()

def render_distress_screen(p):
    st.markdown("""
        <div class="scene-card" style="border: 2px solid #ef4444; background: rgba(69, 10, 10, 0.85); text-align: center;">
            <h1 style="color: #f87171;">⚠️ FINANCIAL BURNOUT & CRISIS</h1>
            <p style="font-size: 1.1rem; color: #fecaca; margin-bottom: 12px;">
                Your Stress has reached 100%! Overwhelming debt service obligations and acute financial pressure have triggered an emergency intervention.
            </p>
            <p style="font-size: 0.95rem; color: #cbd5e1;">
                A financial counselor steps in to restructure your liabilities. Emergency liquidations and debt settlements will cut your stress, but at a severe penalty to your balance sheet.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚨 Restructure Debt & Liquidate Reserves", use_container_width=True, type="primary"):
            penalty = int(p['loan'] * 0.25)
            p['cash'] = max(0, p['cash'] - penalty)
            p['savings'] = max(0, p['savings'] - penalty)
            p['loan'] = max(0, p['loan'] - penalty)
            p['stress'] = 45
            p['score_points'] = max(0, p.get('score_points', 0) - 40)
            p['last_feedback'] = "Emergency Restructuring executed: Creditors accepted haircuts; non-core cash surrendered."
            p['feedback_type'] = "bad"
            st.rerun()

# ==========================================
# 5. MAIN APP LOOP
# ==========================================
render_language_selector()

state = st.session_state.game['state']

if state == "MAIN_MENU":
    render_main_menu()
elif state == "CREDITS":
    render_credits()
elif state == "TUTORIAL":
    render_tutorial()
elif state == "INTRO": 
    render_persona_selection()
elif state == "CYBER_GAME": 
    render_phishing_game()
elif state == "MAP": 
    render_map()
elif state == "PLAYING": 
    render_scene()
elif state == "MARKET":
    render_investmentsim()
elif state == "END":
    p = st.session_state.game
    nw = (p['cash'] + p['savings'] + p.get('investments', 0)) - p['loan']
    st.balloons()
    st.markdown(f"<div class='menu-card'><h1>{t('Journey Complete')}</h1><h2>{t('Net Worth')}: ₹{nw:,}</h2><p style='color:#67e8f9;'>Final Literacy Score: {p.get('score_points', 0)} pts</p></div>", unsafe_allow_html=True)
    render_leaderboard_ui(final_score=nw)
    if st.button(f"↺ {t('Restart Journey')}", use_container_width=True): 
        st.session_state.game = {"state": "MAIN_MENU"}
        st.rerun()
import streamlit as st
import streamlit.components.v1 as components
import base64
import re
import io
from gtts import gTTS
from content import GLOSSARY 
from translate import Translator

# --- 1. TRANSLATION & LOCALIZATION ENGINE ---

LANG_CODE_MAP = {
    "English": "en", 
    "Hindi": "hi", 
    "Bengali": "bn", 
    "Marathi": "mr",
    "Telugu": "te", 
    "Tamil": "ta", 
    "Gujarati": "gu", 
    "Odia": "or",
    "Punjabi": "pa", 
    "Kannada": "kn", 
    "Malayalam": "ml"
}

COMMON_UI_DICTIONARY = {
    "hi": {
        "FinLife": "फिनलाइफ",
        "A Financial Literacy RPG Journey": "वित्तीय साक्षरता आरपीजी यात्रा",
        "START JOURNEY": "यात्रा शुरू करें",
        "HOW TO PLAY": "कैसे खेलें",
        "CYBER SHIELD": "साइबर शील्ड",
        "CREDITS": "क्रेडिट",
        "BACK TO MENU": "मुख्य मेनू पर वापस जाएं",
        "Role": "भूमिका",
        "Cash": "नकद",
        "Savings": "बचत",
        "Debt": "कर्ज",
        "Invest Pool": "निवेश पूल",
        "Score": "स्कोर",
        "Stress": "तनाव",
        "Insurance": "बीमा",
        "Select Your Persona": "अपना पात्र चुनें",
        "Govt Schemes": "सरकारी योजनाएं",
        "Schemes available for you right now": "आपके लिए उपलब्ध योजनाएं",
        "Claim Benefit": "लाभ प्राप्त करें",
        "Approved": "स्वीकृत",
        "added to": "में जोड़े गए",
        "Insurance ACTIVE": "बीमा सक्रिय है",
        "No new schemes available at this level. Keep playing!": "इस स्तर पर कोई नई योजना नहीं है। खेलते रहें!"
    },
    "mr": {
        "FinLife": "फिनलाइफ",
        "A Financial Literacy RPG Journey": "आर्थिक साक्षरता आरपीजी प्रवास",
        "START JOURNEY": "प्रवास सुरू करा",
        "HOW TO PLAY": "कसे खेळायचे",
        "CYBER SHIELD": "सायबर शिल्ड",
        "CREDITS": "श्रेय",
        "BACK TO MENU": "मेनूवर परत जा",
        "Role": "भूमिका",
        "Cash": "रोख",
        "Savings": "बचत",
        "Debt": "कर्ज",
        "Invest Pool": "गुंतवणूक पूल",
        "Score": "गुण",
        "Stress": "तणाव",
        "Insurance": "विमा",
        "Select Your Persona": "तुमचे व्यक्तिमत्त्व निवडा",
        "Govt Schemes": "शासकीय योजना",
        "Schemes available for you right now": "तुमच्यासाठी उपलब्ध योजना",
        "Claim Benefit": "लाभ मिळवा",
        "Approved": "मंजूर",
        "added to": "मध्ये जोडले",
        "Insurance ACTIVE": "विमा सक्रिय आहे",
        "No new schemes available at this level. Keep playing!": "या पातळीवर नवीन योजना उपलब्ध नाहीत. खेळत राहा!"
    },
    "bn": {
        "FinLife": "ফিনলাইফ",
        "A Financial Literacy RPG Journey": "আর্থিক সাক্ষরতা আরপিজি যাত্রা",
        "START JOURNEY": "যাত্রা শুরু করুন",
        "HOW TO PLAY": "কীভাবে খেলবেন",
        "CYBER SHIELD": "সাইবার শিল্ড",
        "CREDITS": "কৃতিত্ব",
        "BACK TO MENU": "মেনুতে ফিরে যান",
        "Role": "ভূমিকা",
        "Cash": "নগদ",
        "Savings": "সঞ্চয়",
        "Debt": "ঋণ",
        "Invest Pool": "বিনিয়োগ পুল",
        "Score": "স্কোর",
        "Stress": "মানসিক চাপ",
        "Insurance": "বীমা",
        "Select Your Persona": "আপনার চরিত্র নির্বাচন করুন",
        "Govt Schemes": "সরকারি প্রকল্প",
        "Schemes available for you right now": "আপনার জন্য উপলব্ধ প্রকল্প",
        "Claim Benefit": "সুবিধা দাবি করুন",
        "Approved": "অনুমোদিত",
        "added to": "যোগ করা হয়েছে",
        "Insurance ACTIVE": "বীমা সক্রিয়",
        "No new schemes available at this level. Keep playing!": "এই স্তরে নতুন কোনো প্রকল্প নেই। খেলতে থাকুন!"
    }
}

MEMORY_CACHE = {}

def translate_text(text, target_lang="English"):
    if target_lang == "English" or not text or not str(text).strip():
        return text

    lang_code = LANG_CODE_MAP.get(target_lang, "en")
    if lang_code == "en":
        return text

    clean = str(text).strip()

    if lang_code in COMMON_UI_DICTIONARY and clean in COMMON_UI_DICTIONARY[lang_code]:
        return COMMON_UI_DICTIONARY[lang_code][clean]

    cache_key = (clean, lang_code)
    if cache_key in MEMORY_CACHE:
        return MEMORY_CACHE[cache_key]

    try:
        translator = Translator(to_lang=lang_code)
        translated = translator.translate(clean)
        MEMORY_CACHE[cache_key] = translated
        return translated
    except Exception:
        return text

def t(text):
    selected_lang = st.session_state.get("selected_lang", "English")
    return translate_text(text, selected_lang)

def render_language_selector():
    if "selected_lang" not in st.session_state:
        st.session_state.selected_lang = "English"

    cols = st.columns([6, 1.2])
    with cols[1]:
        lang_options = list(LANG_CODE_MAP.keys())
        current_idx = lang_options.index(st.session_state.selected_lang) if st.session_state.selected_lang in lang_options else 0
        lang = st.selectbox(
            "Language",
            options=lang_options,
            index=current_idx,
            label_visibility="collapsed",
            key="global_lang_selector"
        )
        if lang != st.session_state.selected_lang:
            st.session_state.selected_lang = lang
            st.rerun()

# --- 2. MULTIMEDIA & DIALOGUE UTILS ---

def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return "" 

@st.cache_data(show_spinner=False, max_entries=200)
def generate_audio_b64(text, lang_code):
    if not text:
        return ""
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return base64.b64encode(fp.read()).decode()
    except Exception:
        try:
            tts = gTTS(text=text, lang="en", slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return base64.b64encode(fp.read()).decode()
        except Exception:
            return ""

def render_interactive_dialogue(avatar, npc, text):
    translated_main_text = t(text)
    processed_text = translated_main_text
    curr_lang = st.session_state.get("selected_lang", "English")
    lang_code = LANG_CODE_MAP.get(curr_lang, "en")

    main_audio_b64 = generate_audio_b64(translated_main_text, lang_code)

    sorted_keys = sorted(GLOSSARY.keys(), key=len, reverse=True)
    for term in sorted_keys:
        pattern = re.compile(rf"\b({re.escape(term)})\b", re.IGNORECASE)
        if pattern.search(processed_text):
            translated_def = t(GLOSSARY[term]).replace("'", "&apos;").replace('"', '&quot;')
            translated_term = t(term)
            def_audio_b64 = generate_audio_b64(t(GLOSSARY[term]), lang_code)
            replacement = f"<span class='highlight' onclick=\"showDef('{translated_term}', '{translated_def}', '{def_audio_b64}')\">\\1</span>"
            processed_text = pattern.sub(replacement, processed_text)

    html_content = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {{ 
                font-family: 'Poppins', sans-serif; 
                background: transparent; 
                color: #e2e8f0; 
                margin: 0; 
                padding: 0; 
                overflow: hidden; 
            }}
            .dialogue-wrapper {{
                display: flex;
                gap: 16px;
                align-items: flex-start;
            }}
            .avatar-badge {{
                width: 52px;
                height: 52px;
                background: rgba(30, 41, 59, 0.8);
                border: 2px solid #475569;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 26px;
                flex-shrink: 0;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            }}
            .bubble-body {{
                flex-grow: 1;
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 0 16px 16px 16px;
                padding: 16px 20px;
                position: relative;
            }}
            .header-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            }}
            .npc-name {{
                color: #facc15;
                font-size: 0.82rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.8px;
            }}
            .listen-pill {{
                background: rgba(250, 204, 21, 0.12);
                border: 1px solid rgba(250, 204, 21, 0.35);
                color: #fde047;
                padding: 3px 10px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                gap: 4px;
            }}
            .listen-pill:hover {{
                background: #facc15;
                color: #0f172a;
                transform: scale(1.04);
            }}
            .story-text {{
                font-size: 0.96rem;
                line-height: 1.65;
                color: #cbd5e1;
                margin: 0;
            }}
            .highlight {{
                color: #facc15;
                text-decoration: underline;
                text-decoration-style: dotted;
                text-underline-offset: 3px;
                cursor: pointer;
                font-weight: 600;
            }}
            .highlight:hover {{
                color: #fef08a;
            }}
            #def-card {{
                display: none;
                margin-top: 12px;
                background: #090d16;
                border: 1px solid #facc15;
                border-left: 4px solid #facc15;
                padding: 12px 16px;
                border-radius: 10px;
                animation: fadeIn 0.2s ease-out;
            }}
            .def-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 4px;
            }}
            .def-title {{
                color: #facc15;
                font-weight: 700;
                font-size: 0.88rem;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .def-close {{
                cursor: pointer;
                color: #94a3b8;
                font-size: 1.2rem;
                line-height: 1;
            }}
            .def-body {{
                color: #e2e8f0;
                font-size: 0.88rem;
                line-height: 1.5;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(-4px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
    </head>
    <body>
        <div class="dialogue-wrapper">
            <div class="avatar-badge">{avatar}</div>
            <div class="bubble-body">
                <div class="header-row">
                    <span class="npc-name">{t(npc)}</span>
                    <button class="listen-pill" onclick="playVoice('{main_audio_b64}')">🔊 Listen</button>
                </div>
                <p class="story-text">{processed_text}</p>
                <div id="def-card">
                    <div class="def-header">
                        <div class="def-title">
                            <span id="def-term">TERM</span>
                            <button class="listen-pill" id="def-audio-btn" style="padding: 1px 8px;">🔊</button>
                        </div>
                        <span class="def-close" onclick="closeDef()">×</span>
                    </div>
                    <div id="def-desc" class="def-body">Definition</div>
                </div>
            </div>
        </div>

        <script>
            var currentAudio = null;

            function playVoice(b64) {{
                if (!b64) return;
                if (currentAudio) {{
                    currentAudio.pause();
                    currentAudio.currentTime = 0;
                }}
                currentAudio = new Audio("data:audio/mp3;base64," + b64);
                currentAudio.play().catch(function(e) {{ console.log(e); }});
            }}

            function showDef(term, def, audioB64) {{
                document.getElementById('def-term').innerText = term;
                document.getElementById('def-desc').innerText = def;
                var btn = document.getElementById('def-audio-btn');
                btn.onclick = function() {{ playVoice(audioB64); }};
                document.getElementById('def-card').style.display = 'block';
            }}

            function closeDef() {{
                document.getElementById('def-card').style.display = 'none';
                if (currentAudio) currentAudio.pause();
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_content, height=160)
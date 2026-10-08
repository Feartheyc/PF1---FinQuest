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
        "Invest": "निवेश",
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
        "Invest": "गुंतवणूक",
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
        "Invest": "বিনিয়োগ",
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
    """Generates server-side base64 MP3 payload via gTTS for instant click-to-play audio."""
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

    # Generate audio for character narration on-demand
    main_audio_b64 = generate_audio_b64(translated_main_text, lang_code)

    # Highlight glossary keywords
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
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Poppins', sans-serif; background-color: transparent; color: #e2e8f0; margin: 0; padding: 4px; overflow: hidden; }}
            .dialogue-container {{ display: flex; gap: 15px; align-items: flex-start; }}
            .avatar-box {{ width: 50px; height: 50px; background: #334155; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; border: 2px solid #475569; flex-shrink: 0; }}
            .speech-bubble {{ background: #1e293b; border: 1px solid #475569; padding: 15px 20px; border-radius: 0 15px 15px 15px; color: #e2e8f0; flex-grow: 1; font-size: 16px; position: relative; }}
            
            .header-bar {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }}
            .speaker-name {{ color: #facc15; font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }}
            
            .voice-btn {{ 
                background: rgba(250, 204, 21, 0.15); 
                border: 1px solid rgba(250, 204, 21, 0.4); 
                color: #fde047; 
                padding: 2px 10px; 
                border-radius: 20px; 
                font-size: 0.72rem; 
                font-weight: 600; 
                cursor: pointer; 
                transition: 0.2s; 
                display: flex;
                align-items: center;
                gap: 4px;
            }}
            .voice-btn:hover {{ background: #facc15; color: #0f172a; transform: scale(1.04); }}
            
            .highlight {{ color: #facc15; text-decoration: underline; text-decoration-style: dotted; cursor: pointer; font-weight: 600; }}
            
            #modal {{ display: none; position: fixed; bottom: 5px; left: 5px; right: 5px; background: #0f172a; border: 1px solid #facc15; border-left: 5px solid #facc15; padding: 12px; border-radius: 8px; z-index: 9999; }}
            .modal-header {{ display: flex; justify-content: space-between; align-items: center; }}
            .modal-title {{ color: #facc15; font-weight: bold; font-size: 0.85em; display: flex; align-items: center; gap: 8px; }}
            .modal-close {{ cursor: pointer; color: #94a3b8; font-size: 1.2em; }}
        </style>
    </head>
    <body>
        <div class="dialogue-container">
            <div class="avatar-box">{avatar}</div>
            <div class="speech-bubble">
                <div class="header-bar">
                    <span class="speaker-name">{t(npc)}</span>
                    <button class="voice-btn" onclick="playVoice('{main_audio_b64}')">🔊 Listen</button>
                </div>
                {processed_text}
            </div>
        </div>

        <div id="modal">
            <div class="modal-header">
                <div class="modal-title">
                    <span id="modal-term">TERM</span>
                    <button class="voice-btn" id="modal-audio-btn">🔊</button>
                </div>
                <span class="modal-close" onclick="closeModal()">×</span>
            </div>
            <div id="modal-text" style="color: #cbd5e1; font-size: 0.9em; margin-top: 6px;">Def</div>
        </div>

        <script>
            var activeAudio = null;

            function playVoice(b64Data) {{
                if (!b64Data) return;
                if (activeAudio) {{
                    activeAudio.pause();
                    activeAudio.currentTime = 0;
                }}
                activeAudio = new Audio("data:audio/mp3;base64," + b64Data);
                activeAudio.play().catch(function(e) {{ console.log("Audio playback error:", e); }});
            }}

            function showDef(term, def, audioB64) {{
                document.getElementById('modal-term').innerText = term;
                document.getElementById('modal-text').innerText = def;
                var btn = document.getElementById('modal-audio-btn');
                btn.onclick = function() {{ playVoice(audioB64); }};
                document.getElementById('modal').style.display = 'block';
            }}

            function closeModal() {{ 
                document.getElementById('modal').style.display = 'none'; 
                if (activeAudio) activeAudio.pause();
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_content, height=145)
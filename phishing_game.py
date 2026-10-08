import streamlit as st
from utils import t

# ==========================================
# 1. CYBER SHIELD SCENARIOS
# ==========================================
PHISHING_SCENARIOS = [
    {
        "id": 1,
        "sender": "SBI-Alert <alert@sbi-bank-verify99.in>",
        "subject": "⚠️ Immediate KYC Suspension Notice",
        "body": "Dear Customer, your State Bank account will be frozen in 24 hours due to non-updated PAN KYC. Click the official portal link to update your documents immediately: http://bit.ly/sbi-kyc-verify-urgent",
        "is_phishing": True,
        "explanation": "Banks NEVER send bit.ly shortlinks or threaten account suspension within 24 hours. The sender domain 'sbi-bank-verify99.in' is fraudulent."
    },
    {
        "id": 2,
        "sender": "Electricity Dept <bill-desk@bescom.gov.in>",
        "subject": "Electricity Bill Payment Receipt",
        "body": "Dear Consumer, your electricity bill payment of ₹1,420 for Consumer No. 98124912 has been successfully processed via BBPS. Transaction reference: BBPS7812941.",
        "is_phishing": False,
        "explanation": "Legitimate government email from a genuine domain (.gov.in) with no panic triggers, OTP requests, or suspicious external download links."
    },
    {
        "id": 3,
        "sender": "Income Tax Dept <refund@incometax-efiling-refunds.com>",
        "subject": "Income Tax Refund of ₹24,850 Approved",
        "body": "Your assessment year 2025-26 refund of ₹24,850 has been approved. Please verify your debit card number and CVV on the refund portal to credit the funds immediately.",
        "is_phishing": True,
        "explanation": "The Income Tax Department NEVER asks for Debit Card numbers, PINs, or CVVs. Official refunds are credited directly to pre-validated bank accounts via ECS."
    },
    {
        "id": 4,
        "sender": "WhatsApp Rewards <prize@lucky-draw-telecom.net>",
        "subject": "🎉 You have won ₹25,00,000 in KBC Lottery!",
        "body": "Congratulations! Your mobile number won the 2026 Telecom Lucky Draw. Send ₹1,500 registration charge via UPI to claims@upi to claim your winning certificate.",
        "is_phishing": True,
        "explanation": "Classic advance-fee fraud. Genuine lotteries or rewards never ask winners to pay an 'upfront processing fee' to release prize money."
    },
    {
        "id": 5,
        "sender": "Indian Railways (IRCTC) <ticketadmin@irctc.co.in>",
        "subject": "Electronic Reservation Slip (ERS) - PNR: 4819284192",
        "body": "Your train ticket for Journey from CSMT to PUNE on 14-Oct-2026 has been booked. PNR: 4819284192. Please carry an original government photo ID during journey.",
        "is_phishing": False,
        "explanation": "Genuine transactional notification from official IRCTC domain (.co.in) confirming a confirmed PNR."
    }
]

# ==========================================
# 2. MAIN CYBER SHIELD UI
# ==========================================
def render_phishing_game():
    # Initialize Quiz State
    if "cyber_index" not in st.session_state:
        st.session_state.cyber_index = 0
    if "cyber_score" not in st.session_state:
        st.session_state.cyber_score = 0
    if "cyber_feedback" not in st.session_state:
        st.session_state.cyber_feedback = None

    # Header Bar with Exit Button
    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        st.markdown(f"## 🛡️ {t('Cyber Shield: Fraud & Phishing Defense')}")
        st.caption(t("Analyze simulated SMS, emails, and alerts. Determine whether they are legitimate or fraudulent."))
    with top_col2:
        if st.button(f"⬅ {t('Main Menu')}", key="cyber_exit_top", use_container_width=True):
            st.session_state.cyber_index = 0
            st.session_state.cyber_score = 0
            st.session_state.cyber_feedback = None
            if "game" in st.session_state:
                st.session_state.game["state"] = "MAIN_MENU"
            st.rerun()

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 8px 0 20px 0;'>", unsafe_allow_html=True)

    idx = st.session_state.cyber_index
    total_q = len(PHISHING_SCENARIOS)

    # Completion Screen
    if idx >= total_q:
        score = st.session_state.cyber_score
        st.balloons()
        st.markdown(f"""
        <div class="menu-card" style="text-align: center; padding: 30px;">
            <h1 style="color: #4ade80;">🎉 {t('Training Completed')}</h1>
            <h2>{t('Defense Score')}: {score} / {total_q}</h2>
            <p style="color: #cbd5e1; font-size: 1rem; margin-top: 10px;">
                {'🛡️ Outstanding! You have master-level digital threat awareness.' if score >= 4 else '⚠️ Good effort! Review the safety guidelines to spot red flags faster.'}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button(f"↺ {t('Play Again')}", use_container_width=True, type="primary"):
                st.session_state.cyber_index = 0
                st.session_state.cyber_score = 0
                st.session_state.cyber_feedback = None
                st.rerun()
        with btn_c2:
            if st.button(f"⬅ {t('Exit to Main Menu')}", key="cyber_exit_end", use_container_width=True):
                st.session_state.cyber_index = 0
                st.session_state.cyber_score = 0
                st.session_state.cyber_feedback = None
                if "game" in st.session_state:
                    st.session_state.game["state"] = "MAIN_MENU"
                st.rerun()
        return

    # Scenario Card
    item = PHISHING_SCENARIOS[idx]

    # Progress Indicator
    st.progress((idx) / total_q, text=f"Question {idx + 1} of {total_q}")

    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 22px; margin: 15px 0 20px 0; box-shadow: 0 10px 25px rgba(0,0,0,0.4);">
        <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 4px;"><b>FROM:</b> <span style="color: #cbd5e1;">{item['sender']}</span></div>
        <div style="font-size: 0.95rem; font-weight: 700; color: #facc15; margin-bottom: 12px;"><b>SUBJECT:</b> {item['subject']}</div>
        <hr style="border-color: rgba(255,255,255,0.06); margin-bottom: 14px;">
        <div style="font-size: 1rem; line-height: 1.6; color: #f8fafc; font-family: monospace; background: rgba(0,0,0,0.25); padding: 14px; border-radius: 10px; border-left: 3px solid #38bdf8;">
            {item['body']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feedback Toast/Alert
    if st.session_state.cyber_feedback:
        fb = st.session_state.cyber_feedback
        color = "#22c55e" if fb["correct"] else "#ef4444"
        icon = "✅" if fb["correct"] else "❌"
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border-left: 4px solid {color}; padding: 14px 18px; border-radius: 10px; margin-bottom: 18px;">
            <b style="color: {color}; font-size: 1rem;">{icon} {fb['title']}</b><br>
            <span style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5;">{fb['text']}</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"➡️ {t('Next Message')}", use_container_width=True, type="primary"):
            st.session_state.cyber_index += 1
            st.session_state.cyber_feedback = None
            st.rerun()

    else:
        # Decision Action Buttons
        col_safe, col_phish = st.columns(2, gap="medium")
        with col_safe:
            if st.button("🟢 " + t("SAFE / LEGITIMATE"), key=f"btn_safe_{idx}", use_container_width=True):
                user_chose_phishing = False
                is_correct = (user_chose_phishing == item["is_phishing"])
                if is_correct:
                    st.session_state.cyber_score += 1

                st.session_state.cyber_feedback = {
                    "correct": is_correct,
                    "title": "Correct! Legitimate message." if is_correct else "Incorrect! This was a Phishing attempt.",
                    "text": item["explanation"]
                }
                st.rerun()

        with col_phish:
            if st.button("🔴 " + t("PHISHING / FRAUD"), key=f"btn_phish_{idx}", use_container_width=True):
                user_chose_phishing = True
                is_correct = (user_chose_phishing == item["is_phishing"])
                if is_correct:
                    st.session_state.cyber_score += 1

                st.session_state.cyber_feedback = {
                    "correct": is_correct,
                    "title": "Spot on! Fraud detected." if is_correct else "Incorrect! This was actually a genuine notification.",
                    "text": item["explanation"]
                }
                st.rerun()
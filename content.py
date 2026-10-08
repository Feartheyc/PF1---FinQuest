import streamlit as st

def c(text, effects, msg=None):
    return {"text": text, "effects": effects, "msg": msg}

# --- GLOSSARY ---
GLOSSARY = {
    "KCC": "Kisan Credit Card: Low interest loans for farmers.",
    "Hybrid": "High-yield seeds that need more water.",
    "Mandi": "Wholesale market for crops.",
    "Interest": "Extra money paid back on a loan.",
    "Subsidy": "Government discount.",
    "Asset": "Valuable item owned (land, gold).",
    "PF": "Provident Fund: Retirement savings.",
    "EMI": "Monthly loan repayment.",
    "SIP": "Systematic Investment: Monthly investing.",
    "Inflation": "Price rise over time.",
    "Equity": "Ownership share in a business.",
    "Bootstrap": "Starting business with own money.",
    "VC": "Investors who fund startups.",
    "Burn Rate": "Monthly cash spending speed.",
    "Runway": "Months left before money runs out.",
    "Pivot": "Changing business strategy.",
    "IPO": "Selling shares to public market.",
    "ELSS": "Tax-saving mutual funds with a 3-year lock-in.",
    "Organic": "Farming without chemicals, crops sell for higher prices.",
    "Solar Pump": "Water pump running on sun energy, saves electricity bill.",
    "Freelance": "Working part-time for different clients to earn extra money."
}

# ==========================================
# 1. DYNAMIC FARMER SCENARIOS
# ==========================================
def farmer_sowing(p):
    return {
        "title": "Sowing Season", "npc": "Moneylender Seth", "avatar": "👹", 
        "story": "Ramesh! Why run to the bank? Take ₹20,000 cash right now with zero paperwork.", 
        "thought": "Bank takes days... but Seth's compound interest is notoriously ruthless. Rain is due this week.", 
        "advisor": "Compare the true annual cost: 5% a month compounding equals roughly 80% APR. KCC caps at 4-7% subsidised. Can your seasonal crop margin absorb an 80% capital cost?",
        "choices": {
            "Take Seth's Cash": {
                "cash": 20000, 
                "loan": 20000, 
                "score_points": -35,
                "add_flag": "predatory_loan", 
                "stress": 15, 
                "__msg": "⚠️ Signed high-rate informal note. Creditor tracking your crop."
            },
            "Go to Bank (KCC)": {
                "cash": 20000, 
                "loan": 20000, 
                "score_points": 40,
                "confidence": 10, 
                "stress": -5,
                "__msg": "✅ Subsidized agricultural credit line approved by bank manager."
            }
        }
    }

def farmer_seeds(p):
    return {
        "title": "Seed Quality", "npc": "Shopkeeper", "avatar": "🏪", 
        "story": "I have Hybrid Seeds (₹3,000) and Local Seeds (₹1,000). Hybrid yields double, but demands constant irrigation.", 
        "thought": "My borewell is old... if the monsoon delays, hybrid crops dry out instantly.", 
        "advisor": "Assess input resilience: High-yield seeds amplify returns only when primary input risks (water/fertilizer) are zero. Without insured irrigation, local seeds provide defensive survival.",
        "choices": {
            "Buy Hybrid Seeds": {
                "cash": -3000, 
                "add_flag": "hybrid_seeds", 
                "score_points": 10,
                "stress": 10, 
                "__msg": "High-yield hybrid planted. Water vulnerability heightened."
            },
            "Buy Local Seeds": {
                "cash": -1000, 
                "score_points": 25,
                "confidence": 5, 
                "stress": -5,
                "__msg": "Drought-resistant indigenous variety planted."
            }
        }
    }

def farmer_harvest(p):
    return {
        "title": "Harvest Price", "npc": "Middleman", "avatar": "⚖️", 
        "story": "Harvest looks decent. I'll pay ₹30,000 right now in your yard. The APMC Mandi is 50km out.", 
        "thought": "Transport costs ₹3,000 and a full day's work. But middleman margins are huge.", 
        "advisor": "Calculate your Net Price Per Unit: Compare (Mandi Gross - Logistics Cost - Wastage) against (Spot Gate Cash). If the difference exceeds 25%, transport is mathematically profitable.",
        "choices": {
            "Sell at Farmgate": {
                "cash": 30000, 
                "score_points": -10,
                "regret": 10, 
                "__msg": "Accepted instant payment; middleman pocketed the trade surplus."
            },
            "Transport to Mandi": {
                "cash": 45000, 
                "score_points": 35,
                "stress": 5, 
                "__msg": "Auction completed at full open mandi market rate."
            }
        }
    }

def farmer_debt_payoff(p):
    if p["flags"].get("predatory_loan"):
        return {
            "title": "Seth's Collection", "npc": "Seth's Enforcer", "avatar": "🥊",
            "story": "Ramesh! That ₹20,000 has compounded to ₹40,000! Pay up immediately or we confiscate your dairy cattle!",
            "thought": "I should never have taken his easy money... it doubled in months!",
            "advisor": "When dealing with predatory creditors, compound interest eats all operating margin. Liquidate non-core cash now or carry an unpayable recurring debt trap.",
            "choices": {
                "Settle Seth's Demand": (
                    {
                        "cash": -40000, 
                        "loan": -p.get("loan", 20000), 
                        "score_points": 20,
                        "stress": -10, 
                        "__msg": "Predatory lender satisfied; liabilities settled."
                    } if p["cash"] >= 40000 else {
                        "loan": 20000, 
                        "score_points": -30,
                        "stress": 30, 
                        "__msg": "Insufficient funds! Creditor applied penal rates to balance."
                    }
                ),
                "Pawn Family Gold": {
                    "cash": -20000, 
                    "loan": -10000, 
                    "score_points": -15,
                    "stress": 15, 
                    "__msg": "Family jewelry pledged to appease debt enforcers."
                }
            }
        }
    return {
        "title": "Bank KCC Renewal", "npc": "Bank Manager", "avatar": "🏦",
        "story": "Namaste Ramesh. Your KCC crop loan of ₹20,000 is due for seasonal rollover. Clear it today to maintain your 7% subsidized status.",
        "thought": "Paying on time keeps my interest subvention benefit alive.",
        "advisor": "Prompt repayment on institutional crop credit keeps your interest subsidy active (lowering rates from 7% down to 4%) and protects your credit record.",
        "choices": {
            "Clear & Renew KCC": {
                "cash": -20000, 
                "loan": -20000, 
                "score_points": 40,
                "confidence": 15, 
                "__msg": "Crop credit ledger closed and renewed in good standing."
            },
            "Defer Repayment": {
                "stress": 15, 
                "loan": 2000, 
                "score_points": -25,
                "__msg": "Default recorded. Subvention subsidy cancelled by bank."
            }
        }
    }

def farmer_education(p):
    return {
        "title": "Daughter's School", "npc": "Wife", "avatar": "👩", 
        "story": "Lakshmi needs secondary school admission. The Private English Academy is ₹15,000; the District Govt School is free.", 
        "thought": "I want her to have skills I never possessed... but can our reserves manage ₹15,000?", 
        "advisor": "Human capital returns compound over decades, but short-term solvency must be protected. Ensure this tuition does not require high-interest emergency borrowing.",
        "choices": {
            "Private Academy": {
                "cash": -15000, 
                "score_points": 35,
                "confidence": 20, 
                "__msg": "Enrolled in English academy. Household skills base expanded."
            },
            "District School": {
                "savings": 5000, 
                "score_points": 15,
                "confidence": 5, 
                "__msg": "Enrolled in district school; family reserve cash preserved."
            }
        }
    }

def farmer_equipment(p):
    return {
        "title": "Farm Machinery", "npc": "Equipment Dealer", "avatar": "🚜", 
        "story": "Why break your back? Buy a 45HP Tractor! Easy financing: ₹5,00,000 loan, 7-year tenure.", 
        "thought": "A tractor brings immense respect... but an EMI of ₹9,00,0 every single month?", 
        "advisor": "Examine Asset Utilization: A machine must generate revenue (via custom-hiring to neighbors) to justify debt financing. Idle machinery on small acreage turns into negative cash flow.",
        "choices": {
            "Finance Tractor": {
                "loan": 500000, 
                "score_points": -20,
                "stress": 25, 
                "__msg": "Long-term equipment loan signed. Fixed monthly obligation begins."
            },
            "Rent Custom Hiring": {
                "cash": -5000, 
                "score_points": 30,
                "confidence": 10, 
                "__msg": "Contracted tractor solely for ploughing days; balance sheet clear."
            }
        }
    }

def farmer_wedding(p):
    return {
        "title": "Family Obligation", "npc": "Village Elder", "avatar": "🎉", 
        "story": "Your sister's wedding demands a 500-guest feast and gold. Sell your highway parcel for ₹5 Lakhs to make a statement!", 
        "thought": "If I sell the land, that recurring harvest income is gone forever.", 
        "advisor": "Selling revenue-producing productive assets (agricultural land) to fund one-day consumption is the single biggest cause of generational rural poverty.",
        "choices": {
            "Liquidate Acre": {
                "cash": 500000, 
                "add_flag": "sold_land", 
                "score_points": -50,
                "stress": 20, 
                "regret": 25, 
                "__msg": "Highway land deed transferred away forever."
            },
            "Prudent Ceremony": {
                "cash": -40000, 
                "score_points": 45,
                "confidence": 15, 
                "__msg": "Ceremony solemnized respectfully without asset liquidation."
            }
        }
    }

def farmer_solar(p):
    return {
        "title": "Energy Upgrade", "npc": "Govt Officer", "avatar": "👮", 
        "story": "Install a 5HP PM-KUSUM Solar Pump for ₹50,000. The government covers 60% of total outlay.", 
        "thought": "Diesel costs me ₹30,000 every single year. But ₹50,000 upfront is real money.", 
        "advisor": "Calculate the Payback Period: If annual fuel savings equal ₹30,000, a ₹50,000 outlay amortizes fully in under 24 months, after which irrigation is entirely free.",
        "choices": {
            "Install Solar": {
                "cash": -50000, 
                "score_points": 50,
                "confidence": 20, 
                "stress": -10, 
                "__msg": "Solar grid activated: Farm operating overhead reduced permanently."
            },
            "Retain Diesel Pump": {
                "cash": -4000, 
                "score_points": -10,
                "stress": 5, 
                "__msg": "Retained fuel pump; exposed to continuous diesel price rises."
            }
        }
    }

def farmer_sustainable(p):
    if p["flags"].get("sold_land"):
        return {
            "title": "Reduced Harvest", "npc": "Contract Buyer", "avatar": "🌾",
            "story": "Without that roadside parcel you sold for the wedding, your total harvest tonnage is halved this season.",
            "thought": "The wedding was glorious, but my seasonal cash flow is permanently crippled.",
            "advisor": "This is the true downstream opportunity cost of asset liquidation: reduced baseline operational earnings year after year.",
            "choices": {
                "Sell Small Harvest": {"cash": 20000, "score_points": 10, "stress": 10, "__msg": "Harvest crop cleared with lower output tonnage."},
                "Work Wage Labor": {"cash": 30000, "score_points": 5, "stress": 20, "__msg": "Daily wage shifts performed to bridge living shortfall."}
            }
        }
    return {
        "title": "Direct Farm Contract", "npc": "FPO Representative", "avatar": "🌱",
        "story": "Our Farmer Producer Company wants an annual contract for your organic produce at a 30% premium.",
        "thought": "Direct corporate tie-ups eliminate middlemen completely.",
        "advisor": "FPO aggregation combines smallholder supply to demand institutional pricing power. Collective marketing reduces individual marketing volatility.",
        "choices": {
            "Sign FPO Contract": {
                "cash": 80000, 
                "score_points": 45,
                "confidence": 25, 
                "__msg": "Procurement contract locked with agricultural collective."
            },
            "Spot Market Selling": {
                "cash": 50000, 
                "score_points": 15,
                "stress": 5, 
                "__msg": "Produce unloaded at prevailing spot prices."
            }
        }
    }

FARMER_EVENTS = [
    farmer_sowing, farmer_seeds, farmer_harvest, farmer_debt_payoff,
    farmer_education, farmer_equipment, farmer_wedding, farmer_solar, farmer_sustainable
]

# ==========================================
# 2. DYNAMIC EMPLOYEE SCENARIOS
# ==========================================
def emp_offer(p):
    return {
        "title": "Salary Structure", "npc": "HR Director", "avatar": "👔", 
        "story": "Welcome to the corporate team! Choose your CTC structure: Maximize take-home cash or maximize Provident Fund (EPF) and voluntary pension contribution?", 
        "thought": "Cash in hand lets me rent a nicer flat. EPF locks money away until retirement.", 
        "advisor": "Remember forced compounding: EPF guarantees 8%+ risk-free sovereign returns with tax-exempt interest. Extra cash in hand often dissolves into lifestyle creep.",
        "choices": {
            "High Cash-in-Hand": {
                "cash": 50000, 
                "score_points": 5,
                "stress": 5, 
                "__msg": "Direct take-home selected; long-term statutory savings forfeited."
            },
            "High EPF Contribution": {
                "cash": 38000, 
                "savings": 12000, 
                "score_points": 35,
                "confidence": 10, 
                "__msg": "Provident fund mandate enrolled; retirement deductions automated."
            }
        }
    }

def emp_lifestyle(p):
    return {
        "title": "Status Upgrade", "npc": "Colleague", "avatar": "📱", 
        "story": "Everyone on the floor got the new flagship smartphone. It's only ₹8,000 down and ₹7,000/month on No-Cost EMI!", 
        "thought": "My current phone is 2 years old... but everyone places theirs on the conference table.", 
        "advisor": "Calculate your Net Working Hours to buy this: If your hourly wage is ₹300, a ₹80,000 phone costs 266 hours of pure labor. Does an appliance justify 33 workdays?",
        "choices": {
            "Sign 12-Month EMI": {
                "cash": -8000, 
                "loan": 72000, 
                "score_points": -25,
                "add_flag": "phone_emi", 
                "stress": 10, 
                "__msg": "Flagship device unboxed; monthly consumer installments scheduled."
            },
            "Keep Current Device": {
                "score_points": 35,
                "confidence": 10, 
                "__msg": "Resisted peer consumption pressure; personal runway safeguarded."
            }
        }
    }

def emp_transport(p):
    return {
        "title": "Commute Choices", "npc": "Family Member", "avatar": "🚗", 
        "story": "Riding the suburban train is exhausting. Let's finance a mid-size SUV! Total loan: ₹12,00,000 with ₹24,000 EMI.", 
        "thought": "An SUV looks respectable outside our society... but ₹24,000 is over a third of my take-home pay!", 
        "advisor": "Apply the 20/4/10 Rule: At least 20% down, loan tenure under 4 years, and total auto costs (EMI + Fuel + Insurance) under 10% of gross monthly income.",
        "choices": {
            "Finance the SUV": {
                "cash": -200000, 
                "loan": 1000000, 
                "score_points": -35,
                "add_flag": "suv_loan", 
                "stress": 20, 
                "__msg": "Automobile delivered; heavy monthly bank auto-debit activated."
            },
            "Certified Pre-Owned": {
                "cash": -150000, 
                "score_points": 35,
                "confidence": 10, 
                "__msg": "Reliable vehicle bought outright; zero debt obligations created."
            }
        }
    }

def emp_speculation(p):
    return {
        "title": "Inside Tip", "npc": "Telegram Group", "avatar": "📉", 
        "story": "Guaranteed 100% returns in 14 days! Small-cap biotech stock about to announce US FDA approval. Put ₹50,000 in right now.", 
        "thought": "If I double this, my debt vanishes... but who is leaking this info?", 
        "advisor": "Information Asymmetry: By the time retail investors hear 'guaranteed tips' on social media, insiders are already preparing their exit liquidity. Never speculate with emergency reserves.",
        "choices": {
            "Speculate ₹50,000": {
                "cash": -50000, 
                "score_points": -40,
                "regret": 20, 
                "__msg": "Biotech crashed on market open; capital trapped."
            },
            "Automate Broad Index SIP": {
                "cash": -25000, 
                "investments": 25000, 
                "score_points": 40,
                "confidence": 15, 
                "__msg": "Broad index units accumulated systematically."
            }
        }
    }

def emp_insurance(p):
    return {
        "title": "Risk Management", "npc": "Insurance Advisor", "avatar": "🏥", 
        "story": "Your company provides basic ₹2 Lakh cover, but a single critical illness costs ₹15 Lakhs. Super top-up family health cover costs ₹20,000/year.", 
        "thought": "I'm young and fit. Why give away ₹20,000 every single year?", 
        "advisor": "Corporate insurance ends the exact moment you lose or switch your job. Personal health insurance acts as a firewall around your investment portfolio.",
        "choices": {
            "Buy Dedicated Super Top-Up": {
                "cash": -20000, 
                "insurance": True, 
                "score_points": 45,
                "confidence": 15, 
                "__msg": "Independent health insurance policy active for household."
            },
            "Rely Strictly on Employer": {
                "score_points": -20,
                "stress": 10, 
                "__msg": "Dependent solely on corporate group umbrella."
            }
        }
    }

def emp_consequence_crunch(p):
    has_phone = p["flags"].get("phone_emi", False)
    has_suv = p["flags"].get("suv_loan", False)

    if has_phone or has_suv:
        return {
            "title": "Liquidity Squeeze", "npc": "Banking App", "avatar": "⚠️",
            "story": "Month-end salary credited, but automated EMIs for your lifestyle purchases immediately deducted ₹30,000+. Your liquid checking balance is critically low.",
            "thought": "My salary arrived and evaporated within twenty seconds.",
            "advisor": "This is debt-service fatigue. High fixed commitments turn even high-earning professionals into paycheck-to-paycheck prisoners.",
            "choices": {
                "Swipe Credit Card for Expenses": {
                    "cash": 25000, 
                    "loan": 25000, 
                    "score_points": -30,
                    "stress": 20, 
                    "__msg": "Living costs rolled over to credit card revolver."
                },
                "Enforce Austerity Budget": {
                    "cash": 5000, 
                    "loan": -10000, 
                    "score_points": 25,
                    "stress": 10, 
                    "__msg": "Expenses frozen; cash diverted toward loan principal."
                }
            }
        }

    return {
        "title": "Surplus Allocation", "npc": "Banking App", "avatar": "💰",
        "story": "With zero lifestyle EMI commitments eating your monthly income, you have a solid ₹35,000 discretionary surplus this month.",
        "thought": "Living debt-free gives me room to breathe and deploy capital.",
        "advisor": "High savings rates accelerate financial independence. Allocate surplus systematically between emergency liquidity and tax-advantaged equity instruments.",
        "choices": {
            "Deploy to Emergency Liquid Fund": {
                "savings": 35000, 
                "score_points": 35,
                "confidence": 15, 
                "__msg": "Liquid reserve balance increased to cover living costs."
            },
            "Lump-sum Equity SIP": {
                "investments": 35000, 
                "score_points": 40,
                "confidence": 15, 
                "__msg": "Diversified fund units credited to demat account."
            }
        }
    }

def emp_layoff(p):
    return {
        "title": "Corporate Downsizing", "npc": "Company Notice", "avatar": "🏢", 
        "story": "Due to macro restructuring, the company announces a 25% workforce reduction. Performance evaluations will decide retention.", 
        "thought": "Panic won't fix anything. I need to demonstrate high business value immediately.", 
        "advisor": "During economic contraction, liquidity provides negotiating power, while specialized technical skills protect career viability.",
        "choices": {
            "Complete Executive Certification": {
                "cash": -15000, 
                "score_points": 35,
                "confidence": 20, 
                "__msg": "Advanced certifications registered; retention confirmed."
            },
            "Passively Await Appraisals": {
                "score_points": -10,
                "stress": 25, 
                "__msg": "No proactive upskilling; uncertainty persisted during review."
            }
        }
    }

def emp_tax(p):
    return {
        "title": "Tax Optimization", "npc": "Chartered Accountant", "avatar": "📑", 
        "story": "Advance tax deadline is here. You face ₹35,000 tax liability unless invested in Section 80C ELSS mutual funds.", 
        "thought": "ELSS locks funds for 3 years, but saves cash from being handed to the exchequer.", 
        "advisor": "Weigh lock-in periods against tax savings: ELSS combines tax-deductible contributions with disciplined long-term equity growth, beating traditional fixed schemes.",
        "choices": {
            "Invest in ELSS Equity": {
                "cash": -35000, 
                "investments": 35000, 
                "score_points": 45,
                "confidence": 15, 
                "__msg": "Statutory 80C rebate claimed while retaining capital in equities."
            },
            "Surrender Flat Tax": {
                "cash": -35000, 
                "score_points": 5, 
                "__msg": "Standard tax assessment remitted to tax authorities."
            }
        }
    }

def emp_seniority(p):
    return {
        "title": "Leadership Dilemma", "npc": "Executive Committee", "avatar": "💼", 
        "story": "You are offered a Director-level position. Total compensation increases 45%, but you must manage 70-hour workweeks across international time zones.", 
        "thought": "Is the status and compensation worth the toll on my personal health and family?", 
        "advisor": "Calculate your compensation per hour worked, not just annual headline figures. Increased compensation that triggers medical degradation results in net-negative wealth.",
        "choices": {
            "Accept Directorship": {
                "cash": 120000, 
                "score_points": 25,
                "stress": 25, 
                "__msg": "Executive title ratified; corporate obligations increased."
            },
            "Maintain Senior Specialist Role": {
                "score_points": 30,
                "confidence": 15, 
                "stress": -10, 
                "__msg": "Individual contributor track maintained with healthy work-life balance."
            }
        }
    }

EMPLOYEE_EVENTS = [
    emp_offer, emp_lifestyle, emp_transport, emp_speculation,
    emp_insurance, emp_consequence_crunch, emp_layoff, emp_tax, emp_seniority
]

# ==========================================
# 3. DYNAMIC FOUNDER SCENARIOS
# ==========================================
def founder_concept(p):
    return {
        "title": "The Leap", "npc": "Inner Voice", "avatar": "💡", 
        "story": "You built an AI-driven logistics prototype with early traction. Resign from your secure job now or develop it on weekends?", 
        "thought": "Bootstrapping on weekends is exhausting, but leaving without personal reserves is terrifying.", 
        "advisor": "Calculate your personal survival runway: Founders need 12-18 months of personal household living expenses completely isolated from venture cash before going all-in.",
        "choices": {
            "Resign & Go All-In": {
                "cash": -30000, 
                "score_points": 25,
                "confidence": 15, 
                "stress": 15, 
                "__msg": "Resignation tendered; venture timeline starts now."
            },
            "Bootstrapped Moonlighting": {
                "score_points": 20,
                "stress": 25, 
                "__msg": "Dual commitments balanced while testing initial traction."
            }
        }
    }

def founder_cofounder(p):
    return {
        "title": "Equity Distribution", "npc": "Lead Architect", "avatar": "🧑‍💻", 
        "story": "A top-tier technical architect is ready to lead engineering, but demands 45% founder equity with a 4-year vesting schedule.", 
        "thought": "Giving away half the cap table early hurts... but without great tech, we have nothing.", 
        "advisor": "Equity is the most expensive currency a founder owns. Ensure vesting cliffs (1-year minimum) so non-performing co-founders cannot leave with massive unearned equity stakes.",
        "choices": {
            "Grant 45% with 4-Yr Vesting": {
                "score_points": 40,
                "confidence": 15, 
                "equity": -45, 
                "__msg": "Technical co-founder agreement finalized with 1-year cliff."
            },
            "Hire Contract Developers": {
                "cash": -50000, 
                "score_points": 10,
                "stress": 15, 
                "__msg": "Cap table preserved; software development paid in cash."
            }
        }
    }

def founder_mvp(p):
    return {
        "title": "Product Launch", "npc": "First Beta Users", "avatar": "🚀", 
        "story": "The initial build has UX quirks and occasional crashes. Do you ship the minimum viable product now or spend 4 more months refining code?", 
        "thought": "Launching broken code is humiliating. But delay burns ₹1,00,000 every month in servers and living costs.", 
        "advisor": "Shipping early validates whether users actually care enough to complain. Perfectionism during early stages is just disguised fear of market rejection.",
        "choices": {
            "Ship MVP Now": {
                "cash": 40000, 
                "score_points": 40,
                "confidence": 10, 
                "stress": 10, 
                "__msg": "Beta released publicly; initial customer feedback documented."
            },
            "Delay & Refactor": {
                "cash": -60000, 
                "score_points": -15,
                "stress": 15, 
                "__msg": "Release delayed; operational cash spent on code refactoring."
            }
        }
    }

def founder_seed(p):
    return {
        "title": "Venture Capital Offer", "npc": "Partner at VC Fund", "avatar": "💰", 
        "story": "We are offering ₹1 Crore seed capital in exchange for 20% preferred stock and a board seat.", 
        "thought": "₹1 Crore would let us scale aggressively... but venture expectations mean aggressive hypergrowth.", 
        "advisor": "Venture capital is rocket fuel: it makes viable businesses reach orbit, but causes fragile ones to detonate. Take VC money only if your distribution model is proven.",
        "choices": {
            "Accept ₹1 Crore Seed": {
                "cash": 10000000, 
                "equity": -20, 
                "score_points": 35,
                "stress": 10, 
                "__msg": "Seed capital closed; equity stake allocated to investor fund."
            },
            "Bootstrap Organically": {
                "score_points": 35,
                "confidence": 20, 
                "stress": 20, 
                "__msg": "Term sheet declined; operations funded strictly from customer revenue."
            }
        }
    }

def founder_pivot(p):
    return {
        "title": "Unit Economics", "npc": "Analytics Lead", "avatar": "📊", 
        "story": "Data reveals Customer Acquisition Cost (CAC) is ₹4,200 while Lifetime Value (LTV) is only ₹3,100. Our unit economics are negative.", 
        "thought": "We are losing money on every single conversion. We need to restructure our business model.", 
        "advisor": "A business model with LTV < CAC is a leaky bucket. Subsidizing unprofitable volume with investor cash leads directly to insolvency.",
        "choices": {
            "Pivot to Enterprise B2B": {
                "cash": -80000, 
                "score_points": 50,
                "confidence": 20, 
                "__msg": "Business focused toward enterprise contract accounts."
            },
            "Subsidize Consumer Growth": {
                "cash": -250000, 
                "score_points": -40,
                "stress": 25, 
                "__msg": "Marketing spending accelerated into negative unit-economic channels."
            }
        }
    }

def founder_crunch(p):
    return {
        "title": "Runway Warning", "npc": "Fractional CFO", "avatar": "📉", 
        "story": "Macro fundraising markets have frozen. At our current burn rate, we have exactly 60 days of operating runway left.", 
        "thought": "Do we make ruthless cuts right now, or gamble on a term sheet landing in time?", 
        "advisor": "When runway dips under 90 days, survival overrides growth. Founders must immediately cut all non-core expenses to achieve default-alive status.",
        "choices": {
            "Cut Non-Core Operations": {
                "score_points": 40,
                "stress": 15, 
                "confidence": 10, 
                "__msg": "Operating expenses trimmed; runway extended by several quarters."
            },
            "Pursue Bridge Round": {
                "cash": 200000, 
                "loan": 200000, 
                "score_points": -20,
                "stress": 30, 
                "__msg": "Bridge financing taken on structured debt terms."
            }
        }
    }

def founder_exit(p):
    return {
        "title": "Acquisition Offer", "npc": "Enterprise Conglomerate", "avatar": "🏢", 
        "story": "A strategic global player offers an all-cash buyout of ₹5,00,00,000 (₹5 Crores) for our technology stack and user base.", 
        "thought": "This is life-changing financial security... or do we reject it and attempt a public IPO?", 
        "advisor": "Assess bird-in-hand valuation against execution risk: A guaranteed cash exit de-risks personal wealth permanently, whereas scaling to IPO entails multi-year market volatility.",
        "choices": {
            "Accept Acquisition Offer": {
                "cash": 50000000, 
                "score_points": 60,
                "confidence": 30, 
                "__msg": "Company acquired; liquidation transaction completed."
            },
            "Reject & Scale for IPO": {
                "score_points": 30,
                "confidence": 20, 
                "stress": 35, 
                "__msg": "Independent path selected; company gears up for public listing."
            }
        }
    }

def founder_expansion(p):
    return {
        "title": "International Scale", "npc": "VP Strategy", "avatar": "🌍", 
        "story": "Do we allocate ₹15,00,000 to launch sales offices in Singapore and Dubai, or consolidate our domestic margins?", 
        "thought": "Global positioning attracts institutional capital, but overseas compliance is treacherous.", 
        "advisor": "Premature scaling kills more startups than competitors do. Expand cross-border only when your domestic market share is stable and profitable.",
        "choices": {
            "Expand Globally": {
                "cash": -1500000, 
                "investments": 3000000, 
                "score_points": 35,
                "stress": 20, 
                "__msg": "International legal entities incorporated in Dubai and Singapore."
            },
            "Strengthen Domestic Moat": {
                "cash": 500000, 
                "score_points": 40,
                "confidence": 15, 
                "__msg": "Domestic market share and profit margins secured."
            }
        }
    }

def founder_finale(p):
    return {
        "title": "Market Turbulence", "npc": "Financial Daily", "avatar": "📉", 
        "story": "A severe economic downturn hits the sector. Venture capital dries up and tech enterprise budgets are slashed across the board.", 
        "thought": "Our balance sheet strength right now decides whether we survive or vanish.", 
        "advisor": "Recessions wipe out companies built on debt and burn, but allow capital-disciplined operators to acquire distressed competitors at bargain prices.",
        "choices": {
            "Acquire Distressed Competitors": {
                "cash": -1000000, 
                "investments": 4000000, 
                "score_points": 50,
                "confidence": 25, 
                "__msg": "Competitor assets acquired at distressed valuation multiples."
            },
            "Fortify Cash Reserves": {
                "savings": 1000000, 
                "score_points": 35,
                "confidence": 15, 
                "__msg": "Capital preserved in low-risk treasury bills during downcycle."
            }
        }
    }

FOUNDER_EVENTS = [
    founder_concept, founder_cofounder, founder_mvp, founder_seed,
    founder_pivot, founder_crunch, founder_exit, founder_expansion, founder_finale
]

# ==========================================
# 4. DYNAMIC STUDENT SCENARIOS
# ==========================================
def stud_allowance(p): 
    return {
        "title": "Allowance Day", "npc": "Dad", "avatar": "👨‍🦳", 
        "story": "Here is your monthly allowance of ₹6,000, son. Remember to make it last the entire 30 days.", 
        "thought": "Between canteen food, printing notes, and hostel chai, this money disappears within two weeks if I don't budget.", 
        "advisor": "Track your baseline non-negotiable living costs first (canteen, commute). Stash away at least 20% the day money arrives before lifestyle spending begins.",
        "choices": {
            "Automate 30% Savings First": {
                "cash": 4200, 
                "savings": 1800, 
                "score_points": 40,
                "confidence": 10, 
                "__msg": "Savings portion immediately moved into student bank deposit."
            },
            "Discretionary Spending": {
                "cash": 6000, 
                "score_points": -10,
                "stress": 10, 
                "__msg": "Full allowance kept in wallet; high chance of running out early."
            }
        }
    }

def stud_insurance(p): 
    return {
        "title": "Campus Health Protection", "npc": "Senior Student", "avatar": "🎓", 
        "story": "Listen, I cracked my wrist playing inter-college football last semester and the nursing home bill wiped out my father's savings. Sign up for the student institutional group cover for ₹1,200.", 
        "thought": "₹1,200 is three weekends of treats... but an accident would completely derail my studies.", 
        "advisor": "Insurance converts an unpredictable, catastrophic financial liability (₹50,000+) into a small, predictable, affordable fee (₹1,200).",
        "choices": {
            "Enroll in Student Cover": (
                {
                    "cash": -1200, 
                    "insurance": True, 
                    "score_points": 45,
                    "confidence": 15, 
                    "__msg": "Accident and emergency medical policy certificate received."
                } if p["cash"] >= 1200 else {
                    "score_points": -10,
                    "stress": 10, 
                    "__msg": "Couldn't clear fee; institutional policy enrollment lapsed."
                }
            ),
            "Decline Coverage": {
                "score_points": -20,
                "regret": 10, 
                "__msg": "Health risk carried out-of-pocket."
            }
        }
    }

def stud_crypto(p): 
    return {
        "title": "Hostel Speculation", "npc": "Roommate", "avatar": "😎", 
        "story": "Bro! Look at this Telegram channel. 'DogeMoon' is jumping 400% tonight. Put ₹2,000 in right now and get a new laptop next week!", 
        "thought": "He talks big... but this smells like an unregulated pump and dump scheme.", 
        "advisor": "Any financial instrument that promises triple-digit returns in days relies on continuous inflow of gullible buyers to pay off early promoters. Capital preservation comes first.",
        "choices": {
            "Throw In ₹2,000": {
                "cash": -2000, 
                "score_points": -35,
                "regret": 15, 
                "stress": 10, 
                "__msg": "Token crashed on exchange; trading pair frozen."
            },
            "Refuse Hype": {
                "score_points": 35,
                "confidence": 15, 
                "__msg": "Ignored social tipping scam; capital remained safe."
            }
        }
    }

def stud_exam(p): 
    return {
        "title": "Semester Exam Deadline", "npc": "Admin Office", "avatar": "🏫", 
        "story": "Notice: Semester university examination fees of ₹3,000 are due immediately. Late submissions will result in semester detention.", 
        "thought": "I forgot about the deadline! Where do I pull ₹3,000 from right now?", 
        "advisor": "This is why an emergency cash cushion is necessary. Pulling from savings is disciplined; borrowing creates interest penalties and stress.",
        "choices": {
            "Pay from Cash Balance": {
                "cash": -3000, 
                "score_points": 20,
                "confidence": 5, 
                "__msg": "Examination admission receipt generated."
            },
            "Pay from Accumulated Savings": {
                "savings": -3000, 
                "score_points": 25,
                "stress": 5, 
                "__msg": "Personal emergency reserve utilized to pay registration fee."
            },
            "Borrow from Moneylending App": {
                "loan": 3500, 
                "score_points": -25,
                "stress": 20, 
                "__msg": "Microloan app took high processing deduction."
            }
        }
    }

def stud_phone(p):
    if p.get("insurance"): 
        return {
            "title": "Accident Shielded", "npc": "Campus Service Center", "avatar": "🛠️", 
            "story": "Your backpack slipped and your phone screen completely shattered! But you show them your institutional insurance card.", 
            "thought": "Thank goodness I listened to that senior and paid the ₹1,200 premium!", 
            "advisor": "Insurance works precisely like this: a minor upfront expense prevents an emergency financial loss from wiping out your semester budget.",
            "choices": {
                "Claim Zero-Deductible Repair": {
                    "score_points": 50,
                    "confidence": 20, 
                    "insurance": False, 
                    "__msg": "Device glass repaired under cashless student insurance claim."
                }
            }
        }
    return {
        "title": "Hardware Disaster", "npc": "Repair Center", "avatar": "🛠️", 
        "story": "Your phone fell down the concrete stairs and the screen is completely black. Replacement display costs ₹6,000 upfront.", 
        "thought": "Disaster! I need this phone for lecture attendance and online submissions, but I have no insurance!", 
        "advisor": "When unprotected assets break, choices turn ugly: deplete your savings or fall into predatory instant borrowing traps.",
        "choices": {
            "Pay Full Repair from Savings": {
                "savings": -6000, 
                "score_points": 10,
                "stress": 15, 
                "__msg": "Hard-earned savings disbursed for hardware replacement."
            },
            "Take Instant Personal Loan": {
                "loan": 7500, 
                "score_points": -30,
                "stress": 25, 
                "__msg": "Repair funded via instant student digital lending app."
            }
        }
    }

def stud_intern(p):
    if p.get('confidence', 0) >= 60: 
        return {
            "title": "Competitive Interview", "npc": "Corporate Recruiter", "avatar": "🤝", 
            "story": "We were thoroughly impressed by your poise, clarity, and analytical capability during the interview. We are offering you a paid Summer Analyst Internship!", 
            "thought": "All that financial discipline and preparation paid off!", 
            "advisor": "Disciplined habits build internal confidence. Use this substantial cash inflow to establish your earliest long-term equity investment base.",
            "choices": {
                "Accept Offer & Sign Contract": {
                    "cash": 30000, 
                    "score_points": 50,
                    "confidence": 20, 
                    "__msg": "Offer letter countersigned; paid corporate internship confirmed."
                }
            }
        }
    return {
        "title": "Campus Selection", "npc": "Campus Recruiter", "avatar": "🤝", 
        "story": "You had acceptable test scores, but you lacked confidence and communication clarity under technical questioning. We selected another candidate.", 
        "thought": "I froze up... I need to invest in practical communication and professional skills.", 
        "advisor": "Soft skills, poise, and clarity of thought determine career conversion. Dedicate time to presentation workshops and peer mock interviews.",
        "choices": {
            "Acknowledge Feedback & Upskill": {
                "score_points": 15,
                "stress": 10, 
                "confidence": 5, 
                "__msg": "Feedback noted to prepare for subsequent recruitment drives."
            }
        }
    }

def stud_gig(p): 
    return {
        "title": "Freelance Opportunity", "npc": "Startup Client", "avatar": "💻", 
        "story": "A tech firm offers ₹8,000 for a 4-day web scraping and documentation sprint. However, your university semester finals are next Monday.", 
        "thought": "₹8,000 is immense for a student... but a dip in my GPA could cost me future campus placement eligibility.", 
        "advisor": "Weigh short-term immediate income against long-term asset value: Your degree grade is an asset that impacts your starting salary for years to come.",
        "choices": {
            "Accept Sprint Gig": {
                "cash": 8000, 
                "score_points": 10,
                "stress": 20, 
                "__msg": "Freelance payment received, but study preparation suffered."
            },
            "Decline & Prioritize GPA": {
                "score_points": 35,
                "confidence": 15, 
                "__msg": "Declined freelance work to focus on exam performance."
            }
        }
    }

def stud_placement(p): 
    return {
        "title": "Final Placement Drive", "npc": "Hostel Warden", "avatar": "👔", 
        "story": "The marquee campus placement drives start tomorrow morning. Professional formal attire is strictly mandatory for corporate interview hall entry.", 
        "thought": "A custom formal suit costs ₹3,000. Going casual means disqualification.", 
        "advisor": "Dress for the credibility you wish to project. Professional attire is a high-ROI career investment, but borrow or rent if liquid reserves are tight.",
        "choices": {
            "Purchase Tailored Suit": {
                "cash": -3000, 
                "score_points": 35,
                "confidence": 20, 
                "__msg": "Formal wardrobe prepared; cleared entry for campus interview."
            },
            "Borrow from Roommate": {
                "score_points": 25,
                "stress": 5, 
                "confidence": 5, 
                "__msg": "Formal attire borrowed; dress code requirements fulfilled."
            },
            "Attend in Semi-Casuals": {
                "score_points": -25,
                "confidence": -15, 
                "regret": 20, 
                "__msg": "Penalized by corporate placement panel for casual dress."
            }
        }
    }

STUDENT_EVENTS = [
    stud_allowance, stud_insurance, stud_crypto, stud_exam, 
    stud_phone, stud_intern, stud_gig, stud_placement
]

# ==========================================
# 5. MASTER ROUTER & TOTAL LEVEL GETTER
# ==========================================
def get_total_levels(persona):
    mapping = {
        "Student": len(STUDENT_EVENTS),
        "Farmer": len(FARMER_EVENTS),
        "Employee": len(EMPLOYEE_EVENTS),
        "Founder": len(FOUNDER_EVENTS)
    }
    return mapping.get(persona, 8)

def get_event_data(persona, index):
    if persona == "Student":
        if index < len(STUDENT_EVENTS): 
            evt = STUDENT_EVENTS[index](st.session_state.game)
            return _format_event(evt)
        return None
    elif persona == "Farmer":
        if index < len(FARMER_EVENTS):
            evt = FARMER_EVENTS[index](st.session_state.game)
            return _format_event(evt)
        return None
    elif persona == "Employee":
        if index < len(EMPLOYEE_EVENTS):
            evt = EMPLOYEE_EVENTS[index](st.session_state.game)
            return _format_event(evt)
        return None
    elif persona == "Founder":
        if index < len(FOUNDER_EVENTS):
            evt = FOUNDER_EVENTS[index](st.session_state.game)
            return _format_event(evt)
        return None
    return None

def _format_event(evt):
    choices_dict = {}
    for text, effects in evt["choices"].items():
        eff_copy = effects.copy()
        msg = eff_copy.pop("__msg", None)
        eff_copy["__msg"] = msg
        choices_dict[text] = eff_copy

    return {
        "story": evt["story"],
        "choices": choices_dict,
        "npc": evt["npc"],
        "avatar": evt["avatar"],
        "thought": evt.get("thought", "..."),
        "advisor": evt.get("advisor", "Weigh immediate cash constraints against long-term balance sheet effects.")
    }
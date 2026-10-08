import streamlit as st

def c(text, effects, msg=None):
    return {"text": text, "effects": effects, "msg": msg}

# ==========================================
# MASTER GLOSSARY DATABASE
# ==========================================
GLOSSARY = {
    "7/12 Extract": "Official land record in Maharashtra/India detailing ownership, survey numbers, and crop history.",
    "Arhatiya": "Commission agent or informal rural financier who advances cash in exchange for crop purchasing rights.",
    "MSP": "Minimum Support Price: Agricultural floor price guaranteed by the government to protect farmers against market crashes.",
    "CapEx": "Capital Expenditure: Major one-time funds spent to acquire long-term productive assets (borewells, machinery, servers).",
    "OpEx": "Operational Expenditure: Ongoing recurring costs required for day-to-day operations (diesel, wages, cloud fees).",
    "Interest Subvention": "Government interest subsidy (reducing crop credit from 7% down to 4%) rewarded for timely loan repayment.",
    "Custom Hiring": "Hiring agricultural machinery and implements on an hourly rental basis rather than debt-financing outright ownership.",
    "BNPL": "Buy Now Pay Later: Micro-credit financing that imposes severe compounded interest penalties upon delayed installments.",
    "Opportunity Cost": "The value of the next best alternative given up when making a specific financial or career decision.",
    "SIP": "Systematic Investment Plan: Automated, disciplined monthly investing into diversified mutual funds.",
    "F&O": "Futures and Options: High-leverage derivative trading where retail traders frequently risk total capital wipeout.",
    "Bond Penalty": "Contractual monetary fine enforced by companies if an employee resigns before completing mandatory service tenure.",
    "EPF": "Employees' Provident Fund: Government-backed retirement savings account earning tax-free compounding sovereign returns.",
    "Super Top-Up": "Secondary health insurance policy that covers catastrophic medical bills once a primary threshold deductible is crossed.",
    "Deductible": "The out-of-pocket medical bill amount a policyholder must pay before insurance claims kick in.",
    "Endowment Plan": "Traditional insurance policy combining life cover with low-yield returns, often severely underperforming inflation.",
    "ELSS": "Equity Linked Savings Scheme: Tax-saving mutual fund offering Section 80C deductions with a 3-year lock-in.",
    "Runway": "The total number of months a startup or household can survive before completely depleting its liquid cash reserves.",
    "Vesting": "Schedule under which founders and early employees gradually earn full ownership of their equity over a 4-year period.",
    "Cliff": "Initial qualifying period (typically 1 year) before any portion of allocated equity shares vest.",
    "Cap Table": "Capitalization Table: Official ledger specifying equity ownership percentages, share dilution, and valuations.",
    "CAC": "Customer Acquisition Cost: Total sales and marketing expense required to sign one new paying customer.",
    "LTV": "Customer Lifetime Value: Total gross profit anticipated from a single customer over their full engagement tenure.",
    "Invoice Factoring": "Selling unpaid customer invoices to a financial intermediary at a discount to secure immediate working capital."
}

# ==========================================
# 1. FARMER SCENARIOS (RAMESH)
# ==========================================
def farmer_sowing(p):
    return {
        "title": "The Sowing Window",
        "npc": "Agro-Dealer Sethji",
        "avatar": "🏬",
        "story": "Monsoon clouds are gathering over the ridge. If you don't sow within 48 hours, soil moisture evaporates for two weeks. The Grameen Bank demands your updated 7/12 Extract and 10 working days to sanction crop credit. I can load ₹20,000 worth of certified seed and cash right now—provided your harvest is pledged to my shop.",
        "thought": "Bank interest is only 7% with interest subvention, but waiting 10 days means missing the monsoon. Sethji is right here, but his ledger margins at harvest time are notorious.",
        "advisor": "Timing risk vs. Capital cost: Biological planting deadlines cannot wait for bank bureaucracy. However, pledging harvest sales surrenders all pricing power at harvest. Weigh borrowing spot seed vs. mortgaging the full crop.",
        "choices": {
            "Accept Sethji's Spot Credit": {
                "cash": 20000,
                "loan": 23000,
                "score_points": 10,
                "add_flag": "tied_to_arhatiya",
                "stress": 10,
                "__msg": "Field planted on time before the rain. Output committed to Sethji's ledger."
            },
            "Wait for Bank Sanction": {
                "cash": 20000,
                "loan": 20000,
                "score_points": 25,
                "add_flag": "late_sowing",
                "stress": 20,
                "__msg": "Subsidized bank credit secured, but sowing delayed by 8 dry days."
            }
        }
    }

def farmer_seeds(p):
    late = p["flags"].get("late_sowing", False)
    story_text = "Soil moisture is lower than usual due to the delayed planting. Do you commit acreage entirely to high-value BT Cotton, or intercrop Soybean with indigenous Pigeon Pea pulses?" if late else "Topsoil moisture is ideal. Do you allocate acreage entirely to high-value BT Cotton, or intercrop Soybean with indigenous Pigeon Pea pulses to fix nitrogen?"
    
    return {
        "title": "Acreage Allocation",
        "npc": "Agriculture Extension Officer",
        "avatar": "🌾",
        "story": story_text,
        "thought": "BT Cotton can fetch ₹70,000 in a strong market, but whiteflies or drought will ruin it. Intercropped pulses guarantee steady food and cash, but the profit ceiling is modest.",
        "advisor": "Single-crop concentration risk: Monoculture magnifies biological vulnerability. Intercropping pulses adds organic nitrogen, cuts synthetic fertilizer bills, and provides downside insurance if cotton prices crash.",
        "choices": {
            "100% BT Cotton Acreage": {
                "cash": -4000,
                "add_flag": "monoculture_cotton",
                "score_points": 5,
                "stress": 15,
                "__msg": "High-capital cash crop planted. High upside, zero drought buffer."
            },
            "Intercrop Soybean + Pulses": {
                "cash": -2000,
                "add_flag": "intercropped",
                "score_points": 35,
                "confidence": 10,
                "stress": -5,
                "__msg": "Diversified field layout planted. Lower fertilizer dependency and climate resilience."
            }
        }
    }

def farmer_harvest(p):
    is_cotton = p["flags"].get("monoculture_cotton", False)
    if is_cotton:
        crop_desc = "Your cotton crop yielded 14 quintals."
        base_val = 55000
    else:
        crop_desc = "Your soybean and pulse harvest yielded a stable 11 quintals."
        base_val = 42000

    return {
        "title": "The APMC Yard",
        "npc": "Commission Dalal",
        "avatar": "⚖️",
        "story": f"{crop_desc} The APMC mandi is crowded today. Dalals are quoting an open auction spot price of ₹{base_val:,}. But Sethji's collection agent is standing right beside your trolley, demanding your agreed pre-sowing delivery.",
        "thought": "If I break agreement with Sethji to sell to the highest mandi bidder, he will blacklist my credit line forever. If I sell to him, he discounts my rate.",
        "advisor": "Relationship credit vs. Spot auction: Rural smallholders rely on local Arhatiya dealers for emergency family liquidity when banks turn them away. Weigh the one-time spot gain against ongoing working capital access.",
        "choices": {
            "Honor Sethji's Procurement": {
                "cash": int(base_val * 0.88),
                "loan": -15000,
                "score_points": 20,
                "confidence": 5,
                "__msg": "Harvest sold via tied dealer. Seasonal input debt cleared; credit line intact."
            },
            "Sell to Highest Mandi Bidder": {
                "cash": base_val,
                "score_points": 25,
                "add_flag": "seth_hostile",
                "stress": 20,
                "__msg": "Maximized open auction cash. Sethji notified and demanding immediate loan recall."
            }
        }
    }

def farmer_debt_payoff(p):
    is_hostile = p["flags"].get("seth_hostile", False)
    if is_hostile:
        return {
            "title": "The Ledger Settlement",
            "npc": "Agro-Dealer Sethji",
            "avatar": "😠",
            "story": "You sold your harvest behind my back! I want my entire principal of ₹23,000 plus ₹5,000 default penalty cleared before sundown, or I file a complaint with the village elders.",
            "thought": "I made higher cash at the mandi, but now he is forcing an emergency settlement.",
            "advisor": "When commercial trust breaks, informal lenders turn punitive. Clear unhedged debts immediately to avoid legal and social escalation.",
            "choices": {
                "Clear Ledger in Full": (
                    {
                        "cash": -28000,
                        "loan": -p.get("loan", 23000),
                        "score_points": 15,
                        "stress": -10,
                        "__msg": "Hostile creditor cleared entirely. Cash drained, but clean slate."
                    } if p["cash"] >= 28000 else {
                        "loan": 10000,
                        "stress": 30,
                        "score_points": -25,
                        "__msg": "Unable to clear! Panchayat intervention forced land collateral pledge."
                    }
                ),
                "Negotiate Restructured Note": {
                    "cash": -10000,
                    "loan": 18000,
                    "score_points": 5,
                    "stress": 15,
                    "__msg": "Partial settlement accepted under higher recurring interest rate."
                }
            }
        }

    return {
        "title": "KCC Annual Renewal",
        "npc": "Grameen Bank Field Officer",
        "avatar": "🏦",
        "story": "Namaste Ramesh. Your KCC crop loan of ₹20,000 has completed its 12-month tenure. Clear the balance today for 24 hours to renew your limit and claim your 3% Interest Subvention rebate.",
        "thought": "Depositing the cash resets the cycle and gives me a higher loan sanction for next season.",
        "advisor": "The rollover discipline: Institutional agricultural credit drops from 7% to 4% effective interest only if the balance touches zero at least once every 365 days.",
        "choices": {
            "Deposit & Renew KCC": {
                "cash": -20000,
                "loan": -20000,
                "score_points": 40,
                "confidence": 15,
                "__msg": "KCC renewed successfully with interest subvention bonus applied."
            },
            "Defer Rollover Repayment": {
                "loan": 3000,
                "score_points": -20,
                "stress": 10,
                "__msg": "Rollover missed. Subvention revoked; standard commercial rate (11%) applied."
            }
        }
    }

def farmer_education(p):
    return {
        "title": "Groundwater Shock",
        "npc": "Rig Contractor",
        "avatar": "🚜",
        "story": "The monsoon receded early and the village canal ran dry. You can make a CapEx bet by drilling a 450-foot borewell for ₹40,000 with no guarantee of striking water, or pay heavy OpEx to buy hourly diesel pump sharing rounds from your neighbor.",
        "thought": "If I strike water, land productivity doubles. If it's a dry borehole, ₹40,000 is gone. Buying water is a continuous drain but guaranteed.",
        "advisor": "CapEx vs. OpEx analysis: In hydrogeologically volatile areas, unhedged drilling is speculative. Shared water purchases preserve capital until reserves can comfortably absorb a dry hole.",
        "choices": {
            "Drill Independent Borewell": {
                "cash": -40000,
                "score_points": 10,
                "add_flag": "drilled_borewell",
                "stress": 15,
                "__msg": "Drilled 450 feet: Struck moderate water flow, but liquidity severely drained."
            },
            "Pay for Canal Water Turns": {
                "cash": -8000,
                "score_points": 30,
                "confidence": 10,
                "stress": -5,
                "__msg": "Secured two critical irrigation water rounds without balance-sheet debt."
            }
        }
    }

def farmer_equipment(p):
    return {
        "title": "Mechanization Choice",
        "npc": "FPO Chairman",
        "avatar": "🚜",
        "story": "Labor costs during peak weeding season have jumped to ₹400/day. You can finance a used 25HP tractor with an NBFC loan (₹3,00,000 @ 14% interest), or buy an equity membership in our Farmer Producer Company's Custom Hiring center for ₹15,000.",
        "thought": "Owning a tractor brings village prestige and immediate availability. But ₹3 Lakhs of debt at 14% means a heavy monthly EMI regardless of crop harvest.",
        "advisor": "Asset Utilization vs. Ownership Pride: On smallholdings under 5 acres, a tractor sits idle 280 days a year while interest accrues daily. Custom hiring delivers mechanization with near-zero capital depreciation.",
        "choices": {
            "Finance Used Tractor": {
                "loan": 300000,
                "score_points": -15,
                "stress": 25,
                "__msg": "Tractor parked in yard; heavy fixed monthly interest obligations activated."
            },
            "Cooperative Custom Hiring": {
                "cash": -15000,
                "score_points": 45,
                "confidence": 20,
                "stress": -10,
                "__msg": "FPO machinery membership acquired. Guaranteed priority booking at low rental rates."
            }
        }
    }

def farmer_wedding(p):
    return {
        "title": "Family Expectation",
        "npc": "Village Elder",
        "avatar": "🎉",
        "story": "Your niece's wedding is fixed. Family prestige demands a 400-guest community feast and 3 tolas of gold jewellery. A local builder offers to buy your 0.5-acre roadside plot for ₹4,00,000 in cash. Or you can host a simple mandap ceremony for ₹35,000.",
        "thought": "Selling that plot means permanent loss of my best road-facing land. But holding a modest wedding will invite village gossip for years.",
        "advisor": "Liquidating income-producing productive assets for irreversible one-day social consumption is the most common path to generational poverty. Reputational discomfort fades in months; lost land never returns.",
        "choices": {
            "Liquidate Roadside Half-Acre": {
                "cash": 400000,
                "add_flag": "sold_land",
                "score_points": -45,
                "stress": 20,
                "regret": 25,
                "__msg": "Roadside plot deed handed over; grand feast hosted at the cost of your asset base."
            },
            "Host Modest Ceremony": {
                "cash": -35000,
                "score_points": 40,
                "confidence": 15,
                "stress": 10,
                "__msg": "Ceremony solemnized respectfully within current operational cash reserves."
            }
        }
    }

def farmer_solar(p):
    return {
        "title": "Energy Transition",
        "npc": "Govt PM-KUSUM Officer",
        "avatar": "☀️",
        "story": "Your diesel generator costs ₹28,000 every single year in fuel and maintenance. Under PM-KUSUM, the government covers 60% of a 3HP solar irrigation pump. Your farmer-share contribution is ₹45,000 upfront.",
        "thought": "₹45,000 is a significant chunk of my remaining cash. But eliminating diesel bills would permanently reduce my operating expenses.",
        "advisor": "Payback Period Analysis: With annual fuel savings of ₹28,000, this ₹45,000 capital expenditure breaks even in less than 20 months. After year two, your marginal cost of irrigation water is ₹0.",
        "choices": {
            "Install PM-KUSUM Solar Pump": {
                "cash": -45000,
                "score_points": 50,
                "confidence": 20,
                "stress": -15,
                "__msg": "Solar pump installed. Zero recurring fuel costs for irrigation."
            },
            "Continue with Diesel Engine": {
                "cash": -5000,
                "score_points": -10,
                "stress": 5,
                "__msg": "Upfront capital saved, but farm remains vulnerable to diesel price inflation."
            }
        }
    }

def farmer_sustainable(p):
    has_sold_land = p["flags"].get("sold_land", False)
    if has_sold_land:
        return {
            "title": "Downstream Impact",
            "npc": "FPO Procurement Manager",
            "avatar": "🌱",
            "story": "Our organic export collective is offering ₹65/kg forward contracts for minimum 20-quintal consignments. But having sold your roadside half-acre, your remaining acreage cannot produce enough volume to meet the minimum contract threshold.",
            "thought": "That roadside plot was the reason my total volume was high enough for bulk contracts. Now I'm stuck selling small retail bags at the local market.",
            "advisor": "The compounding opportunity cost of asset loss: When you lose productive acreage, you lose access to high-value institutional contracts that demand minimum scale.",
            "choices": {
                "Sell Small Retail Bags": {
                    "cash": 22000,
                    "score_points": 10,
                    "stress": 15,
                    "__msg": "Limited volume sold to local brokers at retail baseline."
                },
                "Take Up Tenant Farming on Lease": {
                    "cash": -12000,
                    "score_points": 15,
                    "stress": 20,
                    "__msg": "Leased neighboring acreage to attempt hitting contract volume quotas."
                }
            }
        }

    return {
        "title": "Direct Institutional Tie-Up",
        "npc": "FPO Procurement Manager",
        "avatar": "🌱",
        "story": "With your intact acreage and reliable irrigation setup, our collective offers a 3-year direct supply contract to an organic retail chain in Pune. We guarantee 25% over Mandi MSP with direct bank settlement in 48 hours.",
        "thought": "No middleman cuts, no mandi auction volatility, and assured pricing.",
        "advisor": "Vertical integration: Connecting directly to value-added institutional supply chains shields smallholders from spot market crashes and eliminates middleman margins.",
        "choices": {
            "Sign 3-Year Institutional Contract": {
                "cash": 85000,
                "score_points": 50,
                "confidence": 25,
                "stress": -10,
                "__msg": "Secured high-margin institutional procurement contract with bank auto-credit."
            },
            "Remain on Spot Open Mandi": {
                "cash": 50000,
                "score_points": 15,
                "stress": 5,
                "__msg": "Produce liquidated on spot auction market."
            }
        }
    }

FARMER_EVENTS = [
    farmer_sowing, farmer_seeds, farmer_harvest, farmer_debt_payoff,
    farmer_education, farmer_equipment, farmer_wedding, farmer_solar, farmer_sustainable
]

# ==========================================
# 2. STUDENT SCENARIOS (AARAV)
# ==========================================
def stud_allowance(p):
    return {
        "title": "Monthly Allowance Split",
        "npc": "Hostel Senior",
        "avatar": "🎓",
        "story": "Your monthly allowance of ₹6,000 has arrived. Don't lock it away in fixed deposits! Keep it all liquid in your UPI wallet so you can split late-night café bills and join weekend trips with the senior coding club.",
        "thought": "If I spend freely on networking, I could run completely out of cash by the 20th. But if I lock it away, I might miss out on hostel circles.",
        "advisor": "The Pay Yourself First principle: Transferring 30% into a locked recurring deposit before discretionary spending starts guarantees savings compounding while keeping lifestyle expenses constrained.",
        "choices": {
            "Automate 30% Savings First": {
                "cash": 4200,
                "savings": 1800,
                "score_points": 40,
                "confidence": 10,
                "__msg": "Practiced 'Pay Yourself First': ₹1,800 safely locked away."
            },
            "Keep Full Cash in Wallet": {
                "cash": 6000,
                "score_points": -10,
                "stress": 10,
                "__msg": "Kept all cash loose; vulnerable to end-of-month starvation."
            }
        }
    }

def stud_hardware(p):
    return {
        "title": "Hardware Bottleneck",
        "npc": "Roommate",
        "avatar": "💻",
        "story": "Placement coding rounds start next semester and the college computer lab closes strictly at 6 PM. Buy a refurbished business laptop through a BNPL credit app with ₹0 down and ₹1,500/month installments, or share my machine during midnight slots?",
        "thought": "My own machine gives me unlimited practice hours. But BNPL penalties are brutal if I miss even a single monthly due date.",
        "advisor": "Evaluate productive debt vs. cash flow friction: An educational tool directly unlocks earning potential, but micro-lending apps charge punishing default fees if your allowance runs short.",
        "choices": {
            "Sign 6-Month BNPL Credit": {
                "loan": 8000,
                "score_points": 15,
                "add_flag": "laptop_bnpl",
                "stress": 10,
                "__msg": "Hardware secured; monthly microcredit repayment scheduled."
            },
            "Share Roommate's Machine": {
                "score_points": 20,
                "stress": 15,
                "__msg": "Preserved balance sheet; late-night coding sessions add fatigue."
            }
        }
    }

def stud_internship(p):
    return {
        "title": "Opportunity Cost of Time",
        "npc": "Agency Recruiter",
        "avatar": "📞",
        "story": "Why work for free? We have an overnight BPO data-entry shift paying ₹18,000/month in liquid cash right now. Stop chasing that unpaid 3-month open-source development fellowship!",
        "thought": "₹18,000 right now pays off all my expenses and sends money home. But working overnight shifts will destroy my grades and interview preparation.",
        "advisor": "Assess Opportunity Cost: Immediate entry-level wage shifts trade away finite hours needed to acquire deep technical capabilities that command 5x higher entry salaries at campus placements.",
        "choices": {
            "Accept Paid Night Shift": {
                "cash": 18000,
                "score_points": -20,
                "stress": 25,
                "add_flag": "night_shift_fatigue",
                "__msg": "Immediate cash earned; technical preparation and sleep severely disrupted."
            },
            "Take Unpaid Tech Fellowship": {
                "score_points": 45,
                "confidence": 20,
                "stress": 5,
                "__msg": "Built verified software portfolio for high-tier campus placement drives."
            }
        }
    }

def stud_peer_pressure(p):
    return {
        "title": "The Split Bill Trap",
        "npc": "Capstone Project Lead",
        "avatar": "☕",
        "story": "Our project group is holding sprint reviews at an upscale bistro and buying premium cloud API credits. Your split contribution is ₹1,500. Pay up so the team stays motivated!",
        "thought": "₹1,500 is over a quarter of my monthly budget. But if I refuse, they might push me to the margins of the project credits.",
        "advisor": "Social friction vs. Budget integrity: Standing firm on using free-tier open-source tools defends your budget without compromising actual engineering deliverables.",
        "choices": {
            "Pay the ₹1,500 Split": {
                "cash": -1500,
                "score_points": -10,
                "stress": 10,
                "__msg": "Paid café split to protect social comfort at the expense of savings."
            },
            "Propose Free Open-Source Stack": {
                "score_points": 35,
                "confidence": 15,
                "__msg": "Architected open-source setup; defended personal budget and proved initiative."
            }
        }
    }

def stud_shock(p):
    has_bnpl = p["flags"].get("laptop_bnpl", False)
    if has_bnpl and p["cash"] < 3000:
        return {
            "title": "BNPL Installment Crunch",
            "npc": "Lending App Notice",
            "avatar": "⚠️",
            "story": "Your monthly BNPL installment failed due to insufficient wallet funds! Late fee penalties and 36% annualized interest have been added to your ledger.",
            "thought": "I spent too loosely and missed the microloan installment. My credit score is getting damaged.",
            "advisor": "Debt acceleration: Micro-lending apps make default easy and recovery aggressive. Clear toxic revolving micro-credit before anything else.",
            "choices": {
                "Liquidate Emergency Savings": {
                    "savings": -2500,
                    "loan": -2500,
                    "score_points": 20,
                    "stress": -5,
                    "__msg": "Savings deployed to extinguish toxic overdue micro-credit."
                },
                "Defer with Penal Charges": {
                    "loan": 2000,
                    "score_points": -30,
                    "stress": 25,
                    "__msg": "Penalty compounding; credit rating penalized."
                }
            }
        }

    return {
        "title": "Hardware Breakdown",
        "npc": "Repair Center",
        "avatar": "🛠️",
        "story": "Your mobile screen shattered on the concrete walkway right before semester exams. Replacement costs ₹4,000 upfront.",
        "thought": "I need this device for attendance and online tests. Where do I pull ₹4,000 from right now?",
        "advisor": "Liquidity defenses: Emergency reserves exist specifically to absorb unpredicted operational shocks without borrowing at high rates.",
        "choices": {
            "Pay from Savings Balance": {
                "savings": -4000,
                "score_points": 25,
                "confidence": 10,
                "__msg": "Emergency savings absorbed hardware repair without borrowing."
            },
            "Take Instant Micro-Loan": {
                "loan": 5000,
                "score_points": -25,
                "stress": 20,
                "__msg": "Contracted instant short-term personal loan with high processing fees."
            }
        }
    }

def stud_speculation(p):
    return {
        "title": "Speculative Temptation",
        "npc": "Hostel Trading Enthusiast",
        "avatar": "📈",
        "story": "Bro! Why wait decades for wealth? Join our Telegram group. Put ₹3,000 into weekly F&O index expiry options and meme tokens to triple your money by Friday!",
        "thought": "Everyone in the wing is talking about quick returns... but derivatives have ruined seniors before.",
        "advisor": "Speculation vs. Investing: Derivatives (F&O) are zero-sum contracts with high transaction churn where over 90% of retail participants lose capital. Start a disciplined SIP instead.",
        "choices": {
            "Gamble on F&O Expiry": {
                "cash": -3000,
                "score_points": -40,
                "regret": 20,
                "stress": 15,
                "__msg": "Options expired out-of-the-money: Total loss of capital."
            },
            "Start Low-Cost Index SIP": {
                "cash": -1000,
                "investments": 1000,
                "score_points": 45,
                "confidence": 15,
                "__msg": "Disciplined systematic investment initiated in broad market index fund."
            }
        }
    }

def stud_attire(p):
    return {
        "title": "Executive Presentation",
        "npc": "Training & Placement Officer",
        "avatar": "👔",
        "story": "Marquee tier-1 corporate interviews start tomorrow morning. Professional business formals are strictly mandatory for entry. Tailored attire costs ₹3,500, or you can borrow an oversized suit from your roommate.",
        "thought": "A custom suit gives genuine confidence, but ₹3,500 is real money. Borrowing is free but fits poorly.",
        "advisor": "Interview conversions depend on presence and poise. Invest in professional tools if reserves allow, but never take high-interest debt for one-day appearance.",
        "choices": {
            "Purchase Tailored Formals": {
                "cash": -3500,
                "score_points": 35,
                "confidence": 20,
                "__msg": "Professional presentation secured; executive credibility projected."
            },
            "Borrow Roommate's Suit": {
                "score_points": 25,
                "stress": 5,
                "confidence": 5,
                "__msg": "Met interview dress criteria while preserving liquid capital."
            }
        }
    }

def stud_career_fork(p):
    return {
        "title": "The Career Fork",
        "npc": "Placement Committee",
        "avatar": "🏢",
        "story": "You hold two final job offers: A ₹3.6 LPA mass IT recruiter package with a 2-year mandatory service Bond Penalty, vs. a ₹25,000/month stipend at a fast-growing seed-stage AI startup with massive technical exposure.",
        "thought": "The mass recruiter offers guaranteed steady pay, but locks me down with a legal exit fine. The startup is higher risk, but offers rapid learning.",
        "advisor": "Early career compounding: Early professional years should optimize for skill acquisition velocity and technical slope rather than baseline starting salary.",
        "choices": {
            "Sign 2-Year Bond Contract": {
                "cash": 30000,
                "score_points": 20,
                "stress": 15,
                "__msg": "Stable corporate job locked; service bond contract signed."
            },
            "Join Seed-Stage Tech Team": {
                "cash": 25000,
                "score_points": 45,
                "confidence": 25,
                "stress": 5,
                "__msg": "High-velocity technical trajectory chosen; skills moat activated."
            }
        }
    }

STUDENT_EVENTS = [
    stud_allowance, stud_hardware, stud_internship, stud_peer_pressure,
    stud_shock, stud_speculation, stud_attire, stud_career_fork
]

# ==========================================
# 3. EMPLOYEE SCENARIOS (VIKRAM)
# ==========================================
def emp_ctc(p):
    return {
        "title": "CTC Structuring",
        "npc": "Corporate HR Operations",
        "avatar": "👔",
        "story": "Welcome to the corporate team! Choose your CTC structure: Maximize take-home cash in your monthly salary, or maximize your voluntary EPF and statutory retirement contributions?",
        "thought": "More cash in hand gives me flexibility for an upscale apartment. EPF locks funds away until retirement.",
        "advisor": "Forced compounding: EPF provides tax-free, sovereign-backed 8%+ compounding interest. Surplus cash in hand almost inevitably dissolves into lifestyle inflation.",
        "choices": {
            "Maximize Cash-in-Hand": {
                "cash": 50000,
                "score_points": 5,
                "stress": 5,
                "__msg": "High discretionary cash selected; long-term sovereign compound growth surrendered."
            },
            "Maximize EPF Allocation": {
                "cash": 38000,
                "savings": 12000,
                "score_points": 40,
                "confidence": 10,
                "__msg": "Automated retirement wealth creation initiated via statutory EPF deduction."
            }
        }
    }

def emp_transport(p):
    return {
        "title": "Commute & Status",
        "npc": "Extended Family",
        "avatar": "🚗",
        "story": "Riding the suburban railway is exhausting for a corporate manager. Finance a compact SUV on a 5-year bank auto loan (₹23,000 monthly EMI), or purchase a certified pre-owned hatchback outright in cash?",
        "thought": "An SUV gives immediate social respect outside my housing society. But an EMI of ₹23,000 eats a third of my take-home pay every single month.",
        "advisor": "The 20/4/10 Auto Rule: Pay at least 20% down, keep loan tenure under 4 years, and cap total transport costs (EMI, insurance, fuel) below 10% of gross income.",
        "choices": {
            "Finance the Compact SUV": {
                "cash": -200000,
                "loan": 900000,
                "score_points": -35,
                "add_flag": "suv_loan",
                "stress": 20,
                "__msg": "Contracted heavy 5-year auto debt; fixed monthly EMI committed."
            },
            "Certified Pre-Owned Hatchback": {
                "cash": -150000,
                "score_points": 35,
                "confidence": 15,
                "__msg": "Reliable vehicle acquired outright; zero monthly EMI drag on cash flow."
            }
        }
    }

def emp_insurance(p):
    return {
        "title": "The Healthcare Firewall",
        "npc": "Financial Planner",
        "avatar": "🏥",
        "story": "Your employer provides a basic ₹3 Lakh group mediclaim policy, but a single cardiac or oncology event costs ₹15 Lakhs+. Buy a family Super Top-Up policy with a ₹3 Lakh Deductible for ₹15,000/year, or rely on your company cover?",
        "thought": "I'm young and healthy. Why pay ₹15,000 every single year for private cover when the company already covers me?",
        "advisor": "Corporate insurance ends the day you leave or switch jobs. An independent Super Top-Up policy acts as a firewall protecting your equity portfolio against medical ruin.",
        "choices": {
            "Purchase Super Top-Up Policy": {
                "cash": -15000,
                "insurance": True,
                "score_points": 45,
                "confidence": 15,
                "__msg": "Comprehensive health firewall active; balance sheet insulated from medical shocks."
            },
            "Rely Strictly on Employer Cover": {
                "score_points": -20,
                "stress": 10,
                "__msg": "Carrying hidden catastrophic medical bankruptcy risk."
            }
        }
    }

def emp_medical_shock(p):
    has_insurance = p.get("insurance", False)
    if has_insurance:
        return {
            "title": "Medical Shock Absorbable",
            "npc": "Hospital Billing Desk",
            "avatar": "🏥",
            "story": "Your dependent parent required an emergency cardiac procedure costing ₹6,50,000. Your primary corporate insurance covered ₹3 Lakhs, and your Super Top-Up policy cleared the remaining balance without hassle.",
            "thought": "Thank goodness I purchased that top-up policy. Our investments are completely untouched.",
            "advisor": "Insurance in action: A minor upfront premium prevented an unpredictable crisis from wiping out years of accumulated household wealth.",
            "choices": {
                "Process Cashless Settlement": {
                    "score_points": 50,
                    "confidence": 20,
                    "stress": -10,
                    "__msg": "Hospital bill settled cashless; family investment portfolio fully preserved."
                }
            }
        }

    return {
        "title": "Catastrophic Medical Shock",
        "npc": "Hospital Billing Desk",
        "avatar": "⚠️",
        "story": "Your dependent parent required emergency cardiac surgery costing ₹6,50,000. The company cover paid ₹3 Lakhs and expired. The remaining ₹3,50,000 must be cleared immediately.",
        "thought": "Our family reserves are getting emptied. Do I break our mutual fund investments at a market low or take a 14% personal loan?",
        "advisor": "The cost of being underinsured: When health shocks hit without a firewall, households must liquidate compounding investments or contract high-interest personal debt.",
        "choices": {
            "Liquidate Mutual Fund Corpus": {
                "investments": -350000,
                "score_points": 10,
                "stress": 20,
                "__msg": "Long-term investment portfolio liquidated to settle emergency medical dues."
            },
            "Take 14% Bank Personal Loan": {
                "loan": 350000,
                "score_points": -30,
                "stress": 30,
                "__msg": "Unhedged medical debt contracted; added heavy monthly interest liability."
            }
        }
    }

def emp_housing(p):
    return {
        "title": "The Real Estate Anchor",
        "npc": "Property Consultant",
        "avatar": "🏢",
        "story": "Renting is throwing money into the gutter! Put your life savings of ₹12 Lakhs down as a 20% downpayment on a ₹60 Lakh suburban flat and lock in a 25-year home loan EMI, or continue renting and invest the surplus?",
        "thought": "Owning a home is the ultimate middle-class dream. But committing 45% of my monthly salary to a 25-year EMI locks down my career flexibility completely.",
        "advisor": "Real estate illiquidity vs. Financial flexibility: A heavy home loan EMI locks down geographic and career mobility. Renting while investing the EMI-rent differential into index funds often yields superior net worth.",
        "choices": {
            "Sign 25-Year Home Loan": {
                "savings": -200000,
                "loan": 4800000,
                "score_points": -25,
                "stress": 25,
                "__msg": "Purchased suburban flat; life savings committed and 25-year EMI activated."
            },
            "Rent & Invest Differential": {
                "investments": 100000,
                "score_points": 40,
                "confidence": 15,
                "stress": -5,
                "__msg": "Retained career mobility; routed housing surplus systematically into equities."
            }
        }
    }

def emp_career_pivot(p):
    return {
        "title": "Career Pivot",
        "npc": "Fintech Headhunter",
        "avatar": "🤝",
        "story": "We have two compelling offers: A legacy conglomerate offers a guaranteed 30% all-cash salary hike, vs. a high-growth fintech startup offering flat base pay plus ₹15 Lakhs in stock options.",
        "thought": "Guaranteed cash expands my monthly savings immediately. Startup equity has huge upside, but is completely illiquid until an exit.",
        "advisor": "Discounting illiquid equity: Paper options in unlisted startups should be heavily discounted against guaranteed cash unless the company's path to liquidity is transparent.",
        "choices": {
            "Accept Legacy MNC Cash Hike": {
                "cash": 40000,
                "score_points": 35,
                "confidence": 15,
                "__msg": "Guaranteed compensation increase secured; predictable balance sheet growth."
            },
            "Take Startup Equity Package": {
                "score_points": 25,
                "confidence": 10,
                "stress": 10,
                "__msg": "Illiquid equity allocation acquired; upside tied to future corporate liquidity event."
            }
        }
    }

def emp_tax_season(p):
    return {
        "title": "Section 80C Tax Crunch",
        "npc": "Bank Relationship Manager",
        "avatar": "📑",
        "story": "The March 31 tax deadline is here! Dump ₹50,000 into this guaranteed Endowment Plan pushed by our bank, or invest in market-linked ELSS equity mutual funds with a 3-year lock-in?",
        "thought": "The endowment plan claims guaranteed returns and life cover. ELSS has market volatility, but beats inflation over the long haul.",
        "advisor": "Never mix insurance and investment: Traditional endowment policies rarely deliver more than 4-5% annualized returns (losing to inflation). ELSS offers 80C tax rebates with true equity wealth growth.",
        "choices": {
            "Invest in ELSS Equity Funds": {
                "cash": -50000,
                "investments": 50000,
                "score_points": 45,
                "confidence": 15,
                "__msg": "Claimed 80C tax deduction while investing into diversified equity funds."
            },
            "Buy Guaranteed Endowment Plan": {
                "cash": -50000,
                "score_points": -20,
                "__msg": "Committed capital to low-yielding policy; funds locked at subpar returns."
            }
        }
    }

def emp_promotion_toll(p):
    return {
        "title": "Executive Toll",
        "npc": "Managing Director",
        "avatar": "💼",
        "story": "We are promoting you to Business Head. Compensation jumps 45%, but demands 75-hour workweeks across international time zones, heavy travel, and round-the-clock availability.",
        "thought": "The money and status are immense... but my health, family time, and mental stability will take a severe hit.",
        "advisor": "Calculate your true hourly compensation: A 45% pay hike that doubles your working hours actually lowers your effective hourly rate while accelerating physical burnout.",
        "choices": {
            "Accept Executive Promotion": {
                "cash": 120000,
                "score_points": 20,
                "stress": 30,
                "__msg": "Executive title ratified; remuneration unlocked alongside steep burnout pressure."
            },
            "Maintain Senior Specialist Role": {
                "score_points": 35,
                "confidence": 15,
                "stress": -10,
                "__msg": "Quality of life and health protected; high creative output sustained."
            }
        }
    }

EMPLOYEE_EVENTS = [
    emp_ctc, emp_transport, emp_insurance, emp_medical_shock,
    emp_housing, emp_career_pivot, emp_tax_season, emp_promotion_toll
]

# ==========================================
# 4. FOUNDER SCENARIOS (NEHA)
# ==========================================
def founder_leap(p):
    return {
        "title": "The Leap",
        "npc": "Startup Mentor",
        "avatar": "💡",
        "story": "Your AI logistics prototype has early enterprise interest. Resign from your comfortable corporate job now and burn your 8-month personal Runway, or moonlight nights and weekends until you secure paying customers?",
        "thought": "Going all-in gives me full focus, but starting the clock on personal runway is terrifying. Moonlighting is exhausting, but defends household reserves.",
        "advisor": "Personal Runway preservation: Founders need 12+ months of non-negotiable personal living expenses completely isolated from startup finances before quitting full-time employment.",
        "choices": {
            "Resign & Go All-In": {
                "cash": -30000,
                "score_points": 25,
                "confidence": 15,
                "stress": 15,
                "__msg": "Full-time dedication secured; clock starts ticking on cash runway."
            },
            "Moonlight & Validate First": {
                "score_points": 35,
                "confidence": 10,
                "stress": 20,
                "__msg": "Preserved primary salary while validating enterprise demand after hours."
            }
        }
    }

def founder_vesting(p):
    return {
        "title": "Cap Table Distribution",
        "npc": "Prospective Technical Co-founder",
        "avatar": "🧑‍💻",
        "story": "I am leaving my senior engineering role to join as CTO. Give me 45% flat equity on our Cap Table immediately, or I walk away. Don't insult me with a 4-year Vesting schedule and a 1-year Cliff!",
        "thought": "Without his technical expertise, building the platform will take twice as long. But giving away unvested equity means he can leave in six months and retain half the company.",
        "advisor": "Protect the Cap Table: Equity is the most expensive currency a founder owns. Never allocate unvested equity; a standard 4-year vesting schedule with a 1-year cliff ensures complete alignment.",
        "choices": {
            "Enforce 4-Year Vesting with Cliff": {
                "score_points": 45,
                "confidence": 15,
                "equity": -45,
                "__msg": "Enforced institutional 4-year vesting with 1-year cliff; cap table protected."
            },
            "Grant 45% Unvested Equity": {
                "score_points": -30,
                "equity": -45,
                "stress": 20,
                "__msg": "Surrendered unvested cap table shares; exposed venture to dead equity risk."
            }
        }
    }

def founder_mvp(p):
    return {
        "title": "Minimum Viable Product",
        "npc": "Early Beta Customers",
        "avatar": "🚀",
        "story": "The initial build has UX quirks and occasional crashes. Do you ship the imperfect MVP today to collect real customer feedback, or burn ₹1,50,000 and 3 more months refactoring code?",
        "thought": "Launching broken code is embarrassing. But delay burns vital cash runway every single month without validating willingness-to-pay.",
        "advisor": "Validate willingness-to-pay: Releasing early proves whether customers experience acute enough pain to tolerate software imperfections. Perfectionism before launch is disguised fear.",
        "choices": {
            "Ship Imperfect MVP Today": {
                "cash": 40000,
                "score_points": 40,
                "confidence": 10,
                "stress": 10,
                "__msg": "Beta released publicly; commercial validation and early revenue achieved."
            },
            "Delay 3 Months for Polish": {
                "cash": -150000,
                "score_points": -15,
                "stress": 20,
                "__msg": "Delayed launch; burnt operational cash runway on pre-mature code refactoring."
            }
        }
    }

def founder_bespoke_trap(p):
    return {
        "title": "The Custom Dev Trap",
        "npc": "Enterprise Conglomerate",
        "avatar": "🏢",
        "story": "We will sign an immediate ₹15 Lakh contract advance today, PROVIDED you pause your product roadmap and build proprietary custom ERP integrations built exclusively for our internal workflows.",
        "thought": "₹15 Lakhs extends our runway by six months! But becoming an outsourced IT services arm will destroy our scalable product vision.",
        "advisor": "Services trap vs. Product focus: Bespoke enterprise customization trades away scalable product velocity for one-time survival checks. Only accept advances if custom code directly enriches your core roadmap.",
        "choices": {
            "Accept Bespoke Advance Check": {
                "cash": 1500000,
                "score_points": 10,
                "add_flag": "services_shop",
                "stress": 15,
                "__msg": "Accepted bespoke check; engineering resources diverted to client IT integration."
            },
            "Decline & Preserve Product Core": {
                "score_points": 45,
                "confidence": 20,
                "stress": 15,
                "__msg": "Preserved product purity; engineering focused on scalable market platform."
            }
        }
    }

def founder_vc(p):
    return {
        "title": "Venture Capital Term Sheet",
        "npc": "Seed Fund Partner",
        "avatar": "💰",
        "story": "We are offering ₹1.5 Crore Seed investment in exchange for 25% preferred stock and a board seat. You must commit to 300% year-on-year growth or get replaced.",
        "thought": "₹1.5 Crores lets us hire aggressive engineering and sales talent. But taking institutional VC locks us onto the hypergrowth treadmill.",
        "advisor": "Venture Capital is rocket fuel: It accelerates viable distribution engines to orbit, but detonates companies with unproven unit economics. Accept only if your sales funnel is repeatable.",
        "choices": {
            "Accept ₹1.5 Cr Seed Term Sheet": {
                "cash": 15000000,
                "equity": -25,
                "score_points": 35,
                "stress": 15,
                "__msg": "Scale capital secured! Institutional reporting and hypergrowth expectations active."
            },
            "Bootstrap from Revenue": {
                "score_points": 40,
                "confidence": 20,
                "stress": 15,
                "__msg": "Independence retained; growth calibrated strictly to customer cash flow."
            }
        }
    }

def founder_unit_economics(p):
    return {
        "title": "Unit Economics Reality",
        "npc": "VP Growth Analytics",
        "avatar": "📊",
        "story": "Data reveals our CAC is ₹4,500 while customer LTV is only ₹3,100. We lose ₹1,400 on every customer acquisition! Do we subsidize consumer marketing to show top-line growth, or cut ads and pivot to B2B?",
        "thought": "Cutting ad spend will slow our user metrics ahead of fundraising. But spending money to acquire unprofitable customers leads directly to insolvency.",
        "advisor": "A business where CAC > LTV is a leaking bucket. Subsidizing unprofitable customer volume with treasury cash destroys equity value. Fix margins before scaling distribution.",
        "choices": {
            "Cut Ads & Pivot to B2B Contracts": {
                "cash": -50000,
                "score_points": 50,
                "confidence": 20,
                "__msg": "Eliminated unprofitable acquisition channels; shifted to high-margin enterprise accounts."
            },
            "Subsidize Consumer User Growth": {
                "cash": -250000,
                "score_points": -40,
                "stress": 25,
                "__msg": "Depleted treasury on vanity metrics; negative unit economics persisted."
            }
        }
    }

def founder_net90(p):
    return {
        "title": "Enterprise Net-90 Trap",
        "npc": "Fractional CFO",
        "avatar": "📉",
        "story": "Our marquee enterprise client signed a ₹25 Lakh contract, but their procurement policy enforces Net-90 payment terms. Developer payroll is due next week! Use Invoice Factoring at an 18% fee, or delay employee salaries?",
        "thought": "Factoring costs ₹3.5 Lakhs in fees! But delaying payroll will destroy team morale and trigger immediate engineer resignations.",
        "advisor": "Working capital financing: Profitable companies frequently go bankrupt because of cash collection timing mismatches. Factoring is expensive, but preserving payroll integrity is non-negotiable.",
        "choices": {
            "Discount via Invoice Factoring": {
                "cash": 2000000,
                "loan": 350000,
                "score_points": 35,
                "stress": 5,
                "__msg": "Immediate payroll cash unlocked via invoice factoring; team salaries honored."
            },
            "Defer Employee Payroll": {
                "score_points": -35,
                "confidence": -20,
                "stress": 35,
                "__msg": "Payroll deferred; top technical architects submitted immediate resignations."
            }
        }
    }

def founder_exit(p):
    return {
        "title": "Acquisition Liquidity",
        "npc": "Global Enterprise CorpDev",
        "avatar": "🏢",
        "story": "A multinational logistics conglomerate offers an all-cash acquisition of ₹8,00,00,000 (₹8 Crores) for our technology stack and client base. Take guaranteed financial independence today, or reject it and scale toward a public IPO?",
        "thought": "₹8 Crores is life-changing financial security for my family and team. Scaling to an IPO entails 7 more years of brutal competitive and dilution risk.",
        "advisor": "Bird-in-hand valuation vs. Execution hazard: A guaranteed multi-crore cash buyout de-risks personal wealth permanently, whereas scaling to IPO exposes you to severe dilution and market volatility.",
        "choices": {
            "Accept ₹8 Crore All-Cash Buyout": {
                "cash": 80000000,
                "score_points": 60,
                "confidence": 30,
                "__msg": "Successful multi-crore enterprise liquidity exit executed!"
            },
            "Reject & Scale for IPO": {
                "score_points": 30,
                "confidence": 20,
                "stress": 35,
                "__msg": "Committed to grueling multi-year public listing pathway."
            }
        }
    }

FOUNDER_EVENTS = [
    founder_leap, founder_vesting, founder_mvp, founder_bespoke_trap,
    founder_vc, founder_unit_economics, founder_net90, founder_exit
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
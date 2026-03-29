import string
import pickle
import streamlit as st

# ─── Page Config (MUST be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="ScamSHEILD – Job Scam Detector",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet">

<style>
/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Animated Mesh Background ── */
.stApp {
    background-color: #060a14;
    background-image:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(0, 212, 180, 0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 80% at 80% 80%, rgba(99, 67, 255, 0.15) 0%, transparent 60%),
        radial-gradient(ellipse 50% 50% at 50% 50%, rgba(255, 87, 51, 0.05) 0%, transparent 70%);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 3rem 2rem 4rem 2rem !important;
    max-width: 720px !important;
}

/* ── Hero Section ── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 0 2rem 0;
}
.hero-badge {
    display: inline-block;
    background: rgba(0, 212, 180, 0.08);
    border: 1px solid rgba(0, 212, 180, 0.25);
    color: #00d4b4;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.4rem, 6vw, 3.4rem);
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: #f1f5f9;
    margin: 0 0 0.5rem 0;
}
.hero-title span {
    background: linear-gradient(135deg, #00d4b4 0%, #6343ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1rem;
    color: #64748b;
    font-weight: 300;
    letter-spacing: 0.01em;
    margin-top: 0.5rem;
}

/* ── Divider ── */
.custom-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
    margin: 1.8rem 0;
}

/* ── Input Card ── */
.input-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.6rem;
}

/* Text area override */
.stTextArea textarea {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.65 !important;
    padding: 1rem 1.1rem !important;
    caret-color: #00d4b4;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: rgba(0, 212, 180, 0.45) !important;
    box-shadow: 0 0 0 3px rgba(0, 212, 180, 0.08) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #334155 !important; }

/* ── Analyze Button ── */
.stButton > button {
    background: linear-gradient(135deg, #00d4b4, #0099ff) !important;
    color: #060a14 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 12px !important;
    height: 3.2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.2s ease, transform 0.15s ease !important;
    box-shadow: 0 4px 24px rgba(0, 212, 180, 0.25) !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(0, 212, 180, 0.35) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Result Cards ── */
.result-card {
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-top: 1.5rem;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 16px;
    padding: 1px;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: destination-out;
    mask-composite: exclude;
}
.card-scam {
    background: rgba(239, 68, 68, 0.06);
}
.card-scam::before {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.5), rgba(255, 120, 50, 0.3));
}
.card-legit {
    background: rgba(0, 212, 180, 0.06);
}
.card-legit::before {
    background: linear-gradient(135deg, rgba(0, 212, 180, 0.5), rgba(99, 67, 255, 0.3));
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.25rem;
    margin: 0 0 0.4rem 0;
}
.card-title-scam { color: #f87171; }
.card-title-legit { color: #00d4b4; }
.card-body {
    font-size: 0.9rem;
    color: #94a3b8;
    line-height: 1.6;
    font-weight: 300;
}
.risk-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 1.2rem;
    margin-bottom: 0.5rem;
}
.risk-label-scam { color: #f87171; }
.risk-label-legit { color: #00d4b4; }

/* ── Big Percentage Display ── */
.risk-big-pct {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 3.8rem;
    line-height: 1;
    letter-spacing: -0.03em;
    margin: 0.6rem 0 0.2rem 0;
}
.risk-big-pct.scam  { color: #f87171; }
.risk-big-pct.legit { color: #00d4b4; }
.risk-big-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 400;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.risk-big-sub.scam  { color: #7f1d1d; }
.risk-big-sub.legit { color: #134e4a; }

/* ── Segmented Bar ── */
.seg-bar {
    display: flex;
    gap: 3px;
    margin: 0.5rem 0 0.4rem 0;
    height: 10px;
}
.seg-bar span {
    flex: 1;
    border-radius: 3px;
    background: rgba(255,255,255,0.06);
    transition: background 0.05s ease;
}
.seg-bar.scam  span.active { background: linear-gradient(90deg, #f59e0b, #ef4444); }
.seg-bar.legit span.active { background: linear-gradient(90deg, #0099ff, #00d4b4); }
.seg-pct-row {
    display: flex;
    justify-content: space-between;
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: #334155;
    margin-top: 0.25rem;
}

/* ── Indicators ── */
.indicators-section {
    margin-top: 1.6rem;
}
.ind-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.8rem;
}
.ind-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.ind-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.2);
    color: #fca5a5;
    font-family: 'DM Sans', monospace;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 0.3rem 0.75rem;
    border-radius: 8px;
}
.ind-chip::before { content: '⚑  '; font-size: 0.7rem; }

/* ── Golden Rules Card ── */
.golden-card {
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 1.3rem 1.6rem;
    margin-top: 1.6rem;
}
.golden-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #00d4b4;
    margin-bottom: 1rem;
}
.golden-row {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}
.golden-row:last-child { margin-bottom: 0; }
.golden-dot {
    width: 26px;
    height: 26px;
    min-width: 26px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    margin-top: 0.05rem;
}
.golden-dot.warn  { background: rgba(239,68,68,0.12); }
.golden-dot.info  { background: rgba(0,153,255,0.12); }
.golden-dot.check { background: rgba(0,212,180,0.10); }
.golden-text {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.875rem;
    color: #94a3b8;
    line-height: 1.55;
    font-weight: 400;
}
.golden-text strong { color: #cbd5e1; font-weight: 500; }

/* ── Footer ── */
.footer {
    text-align: center;
    margin-top: 3rem;
    font-size: 0.72rem;
    color: #1e293b;
    letter-spacing: 0.05em;
}

/* ── Warning override ── */
.stAlert {
    background: rgba(251, 191, 36, 0.06) !important;
    border: 1px solid rgba(251, 191, 36, 0.2) !important;
    border-radius: 10px !important;
    color: #fbbf24 !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #00d4b4 !important; }
</style>
""", unsafe_allow_html=True)


# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">AI-Powered Protection</div>
    <h1 class="hero-title">Scam<span>SHIELD</span> 🛡️</h1>
    <p class="hero-sub">Paste any job or internship message. We'll tell you if it's a trap.</p>
</div>
<hr class="custom-divider">
""", unsafe_allow_html=True)


# ─── Input ────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-label">📩 Message to analyze</div>', unsafe_allow_html=True)
user_input = st.text_area(
    label="",

    placeholder='Paste the suspicious job or internship message here…\ne.g. "Pay ₹500 to confirm your internship slot. Limited seats!"',
    label_visibility="collapsed",
)

st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)


# ─── Load Model ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
    return model, vectorizer

model, vectorizer = load_model()


# ─── Helpers ──────────────────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

SCAM_SIGNALS = [
    "fee", "payment", "pay", "deposit", "urgent", "limited",
    "no interview", "guaranteed", "work from home", "registration",
    "advance", "transfer", "verify", "confirm", "click here",
]


# ─── Analyze Button ───────────────────────────────────────────────────────────
analyze = st.button("🔍  Analyze Message", use_container_width=True)

if analyze:
    # ── Scroll to top immediately ──
    st.markdown("""
<script>
(function() {
    // Try both common Streamlit scroll containers
    const targets = [
        document.querySelector('.main'),
        document.querySelector('.block-container'),
        window
    ];
    targets.forEach(t => { if (t && t.scrollTo) t.scrollTo({ top: 0, behavior: 'smooth' }); });
})();
</script>
""", unsafe_allow_html=True)

    if user_input.strip() == "":
        st.warning("Please paste a message before analyzing.")
    else:
        with st.spinner("Scanning message patterns…"):
            cleaned = clean_text(user_input)
            vectorized = vectorizer.transform([cleaned])
            prediction = model.predict(vectorized)[0]
            probability = float(model.predict_proba(vectorized)[0][1])

        found_signals = [w for w in SCAM_SIGNALS if w in cleaned]
        risk_pct = int(probability * 100)
        safe_pct  = 100 - risk_pct

        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

        # ── Build segmented bar (20 segments) ──
        TOTAL_SEGS = 20
        def seg_bar(pct: int, kind: str) -> str:
            filled = round(pct / 100 * TOTAL_SEGS)
            segs = "".join(
                f'<span class="active"></span>' if i < filled else '<span></span>'
                for i in range(TOTAL_SEGS)
            )
            return f'<div class="seg-bar {kind}">{segs}</div>'

        if prediction == 1:
            bar_html = seg_bar(risk_pct, "scam")
            st.markdown(f"""
<div class="result-card card-scam">
    <p class="card-title card-title-scam">⚠️ Suspicious Message Detected</p>
    <p class="card-body">
        This message matches patterns commonly found in fraudulent job offers.
        Do <strong style="color:#f87171">not</strong> share personal details, pay any fee,
        or click unknown links until you verify the sender independently.
    </p>
    <p class="risk-label risk-label-scam">Scam Probability</p>
    <div class="risk-big-pct scam">{risk_pct}<span style="font-size:1.6rem;opacity:0.6">%</span></div>
    <div class="risk-big-sub scam">risk score</div>
    {bar_html}
    <div class="seg-pct-row"><span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span></div>
</div>
""", unsafe_allow_html=True)
        else:
            bar_html = seg_bar(safe_pct, "legit")
            st.markdown(f"""
<div class="result-card card-legit">
    <p class="card-title card-title-legit">✅ Message Looks Legitimate</p>
    <p class="card-body">
        No strong scam indicators were detected. The language and structure align with
        genuine job opportunities. Still, verify the company and contact details
        through official channels before proceeding.
    </p>
    <p class="risk-label risk-label-legit">Confidence Score</p>
    <div class="risk-big-pct legit">{safe_pct}<span style="font-size:1.6rem;opacity:0.6">%</span></div>
    <div class="risk-big-sub legit">legitimate confidence</div>
    {bar_html}
    <div class="seg-pct-row"><span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span></div>
</div>
""", unsafe_allow_html=True)

        # ── Detected Signals ──
        if found_signals:
            chips_html = "".join(f'<span class="ind-chip">{w}</span>' for w in found_signals)
            st.markdown(f"""
<div class="indicators-section">
    <div class="ind-title">🔎 Flagged Keywords</div>
    <div class="ind-chips">{chips_html}</div>
</div>
""", unsafe_allow_html=True)

        # ── Golden Rules Card ──
        if prediction == 1:
            rules = [
                ("warn",  "🚫", "<strong>Never pay upfront.</strong> Legitimate employers do not charge registration, training, or security deposit fees."),
                ("info", "🔍", "<strong>Search before you trust.</strong> Google the company name + \"scam\" and check their official website domain."),
                ("check", "✉️", "<strong>Verify the sender's email.</strong> HR email should match the company's official domain — not Gmail or Yahoo."),
            ]
        else:
            rules = [
                ("check", "🔗", "<strong>Cross-check on LinkedIn.</strong> Confirm the recruiter's profile is real and connected to the company."),
                ("info",  "🏢", "<strong>Visit the official website.</strong> Ensure the role is listed on their careers page before proceeding."),
                ("warn",  "📄", "<strong>Guard your documents.</strong> Never share Aadhaar, PAN, or bank details until a formal offer is signed."),
            ]

        rows_html = "".join(f"""
<div class="golden-row">
    <div class="golden-dot {cls}">{icon}</div>
    <div class="golden-text">{text}</div>
</div>""" for cls, icon, text in rules)

        st.markdown(f"""
<div class="golden-card">
    <div class="golden-header">💡 Golden Rules</div>
    {rows_html}
</div>
""", unsafe_allow_html=True)


# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">ScamSHEILD · Protect yourself, always verify independently</div>
""", unsafe_allow_html=True)

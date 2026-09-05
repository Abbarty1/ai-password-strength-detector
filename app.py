import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import random


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="AI Password Strength Detector",
    page_icon="🔐",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f5f7fc;
}

.block-container {
    max-width: 1250px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* HERO */

.hero {
    background:
        radial-gradient(circle at 82% 50%, rgba(139,92,246,0.35), transparent 25%),
        linear-gradient(135deg, #050a2d, #11164b 55%, #25105a);

    border-radius: 0 0 32px 32px;
    padding: 45px 55px;
    color: white;
    min-height: 390px;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: "";
    position: absolute;
    width: 420px;
    height: 420px;
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 50%;
    right: 80px;
    top: 20px;
}

.hero-brand {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 50px;
}

.hero-title {
    font-size: 52px;
    line-height: 1.05;
    font-weight: 800;
    margin-bottom: 20px;
    position: relative;
    z-index: 2;
}

.hero-title span {
    color: #a855f7;
}

.hero-text {
    color: #cbd5e1;
    font-size: 17px;
    line-height: 1.6;
    max-width: 560px;
}

.ai-badge {
    position: absolute;
    right: 45px;
    top: 35px;
    border: 1px solid #8b5cf6;
    background: rgba(139,92,246,0.12);
    padding: 10px 18px;
    border-radius: 30px;
    color: #d8b4fe;
    font-weight: 600;
}

.lock {
    position: absolute;
    right: 140px;
    top: 115px;
    font-size: 145px;
    filter: drop-shadow(0 0 35px #8b5cf6);
}

/* CARDS */

.card {
    background: white;
    border: 1px solid #e7ebf3;
    border-radius: 22px;
    padding: 26px;
    margin-top: 22px;
    box-shadow: 0 10px 35px rgba(15,23,42,0.06);
}

.card-title {
    color: #111827;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 18px;
}

/* RESULT */

.result-card {
    background: white;
    border: 1px solid #e7ebf3;
    border-radius: 22px;
    padding: 28px;
    margin-top: 22px;
    box-shadow: 0 10px 35px rgba(15,23,42,0.06);
}

.result-title {
    font-size: 17px;
    font-weight: 700;
    color: #17203a;
    margin-bottom: 15px;
}

.weak {
    color: #dc2626;
    font-size: 35px;
    font-weight: 800;
}

.medium {
    color: #d97706;
    font-size: 35px;
    font-weight: 800;
}

.strong {
    color: #16a34a;
    font-size: 35px;
    font-weight: 800;
}

.confidence {
    font-size: 42px;
    font-weight: 800;
    color: #17203a;
}

.description {
    color: #64748b;
    line-height: 1.6;
}

/* METRICS */

.metric {
    background: white;
    border: 1px solid #e7ebf3;
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    min-height: 125px;
    box-shadow: 0 5px 20px rgba(15,23,42,0.04);
}

.metric-icon {
    font-size: 25px;
}

.metric-number {
    font-size: 27px;
    font-weight: 800;
    color: #17203a;
    margin-top: 5px;
}

.metric-label {
    color: #64748b;
    font-size: 13px;
}

/* INFORMATION */

.info-card {
    background: white;
    border: 1px solid #e7ebf3;
    border-radius: 22px;
    padding: 25px;
    margin-top: 22px;
    box-shadow: 0 10px 35px rgba(15,23,42,0.05);
}

.info-title {
    color: #17203a;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 15px;
}

.info-item {
    padding: 10px 0;
    border-bottom: 1px solid #eef1f5;
    color: #334155;
}

.info-item:last-child {
    border-bottom: none;
}

/* FOOTER */

.footer {
    margin-top: 30px;
    padding: 25px;
    border-radius: 20px;
    background: #070d2c;
    color: white;
    text-align: center;
}

.footer-small {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 7px;
}

/* STREAMLIT BUTTON */

.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(90deg, #8b5cf6, #3b82f6);
    color: white;
    font-weight: 700;
    font-size: 16px;
}

.stButton > button:hover {
    border: none;
    color: white;
    background: linear-gradient(90deg, #7c3aed, #2563eb);
}

/* MOBILE */

@media (max-width: 800px) {

    .hero {
        padding: 30px 25px;
        min-height: 420px;
    }

    .hero-title {
        font-size: 38px;
    }

    .hero-text {
        font-size: 15px;
    }

    .ai-badge {
        position: static;
        display: inline-block;
        margin-bottom: 25px;
    }

    .hero-brand {
        margin-bottom: 25px;
    }

    .lock {
        right: 25px;
        bottom: 20px;
        top: auto;
        font-size: 90px;
    }
}

</style>
""")


# =========================================================
# HERO SECTION
# =========================================================

st.html("""
<div class="hero">

    <div class="hero-brand">
        🔐 &nbsp; AI Password Strength Detector
    </div>

    <div class="ai-badge">
        🤖 Powered by Machine Learning
    </div>

    <div class="hero-title">
        AI Password<br>
        <span>Strength Detector</span>
    </div>

    <div class="hero-text">
        Our machine learning model analyzes password
        characteristics and predicts their strength.
    </div>

    <div class="lock">
        🔒
    </div>

</div>
""")


# =========================================================
# MACHINE LEARNING TRAINING DATA
# =========================================================

random.seed(42)

training_data = []

for _ in range(1500):

    length = random.randint(4, 20)
    uppercase = random.randint(0, min(5, length))
    lowercase = random.randint(0, min(10, length))
    numbers = random.randint(0, min(5, length))
    special = random.randint(0, min(4, length))

    # Calculate a training score
    score = 0

    if length >= 8:
        score += 1

    if length >= 12:
        score += 2

    if uppercase > 0:
        score += 1

    if lowercase > 0:
        score += 1

    if numbers > 0:
        score += 1

    if special > 0:
        score += 2

    # Create the training label
    if score <= 3:
        strength = "Weak"

    elif score <= 6:
        strength = "Medium"

    else:
        strength = "Strong"

    training_data.append([
        length,
        uppercase,
        lowercase,
        numbers,
        special,
        strength
    ])


training_df = pd.DataFrame(
    training_data,
    columns=[
        "length",
        "uppercase",
        "lowercase",
        "numbers",
        "special",
        "strength"
    ]
)


# =========================================================
# TRAIN MACHINE LEARNING MODEL
# =========================================================

X = training_df[
    [
        "length",
        "uppercase",
        "lowercase",
        "numbers",
        "special"
    ]
]

y = training_df["strength"]


model = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    random_state=42
)

model.fit(X, y)


# =========================================================
# FEATURE EXTRACTION
# =========================================================

def analyze_password(password):

    length = len(password)

    uppercase = sum(
        1 for c in password if c.isupper()
    )

    lowercase = sum(
        1 for c in password if c.islower()
    )

    numbers = sum(
        1 for c in password if c.isdigit()
    )

    special = sum(
        1 for c in password if not c.isalnum()
    )

    return [
        length,
        uppercase,
        lowercase,
        numbers,
        special
    ]


# =========================================================
# PASSWORD INPUT CARD
# =========================================================

st.html("""
<div class="card">
    <div class="card-title">
        🔑 Check Your Password
    </div>
</div>
""")


password = st.text_input(
    "Enter a test password:",
    type="password",
    placeholder="Enter your password here..."
)

st.caption(
    "⚠️ For demonstration only. Do not enter your real password."
)

check = st.button("🔍 Check Password")


# =========================================================
# PREDICTION
# =========================================================

if check:

    if not password:

        st.warning("Please enter a password.")

    else:

        features = analyze_password(password)

        prediction = model.predict([features])[0]

        probabilities = model.predict_proba([features])[0]

        confidence = max(probabilities) * 100


        # ================================================
        # RESULT
        # ================================================

        if prediction == "Weak":

            result_class = "weak"
            icon = "🔴"
            message = "This password needs improvement."

        elif prediction == "Medium":

            result_class = "medium"
            icon = "🟡"
            message = "This password has moderate strength."

        else:

            result_class = "strong"
            icon = "🟢"
            message = "This password has a strong combination of characters."


        st.html(f"""
        <div class="result-card">

            <div class="result-title">
                🛡️ Overall Strength
            </div>

            <div class="{result_class}">
                {icon} {prediction.upper()}
            </div>

            <p class="description">
                {message}
            </p>

            <hr>

            <div class="result-title">
                🤖 AI Prediction Confidence
            </div>

            <div class="confidence">
                {confidence:.1f}%
            </div>

            <p class="description">
                Confidence calculated from the machine-learning model.
            </p>

        </div>
        """)


        # ================================================
        # PASSWORD ANALYSIS
        # ================================================

        st.html("""
        <div class="card-title" style="margin-top:30px;">
            📊 Password Analysis
        </div>
        """)


        metric_html = f"""
        <div style="
            display:grid;
            grid-template-columns:repeat(5, 1fr);
            gap:15px;
        ">

            <div class="metric">
                <div class="metric-icon">🔢</div>
                <div class="metric-number">{features[0]}</div>
                <div class="metric-label">Length</div>
            </div>

            <div class="metric">
                <div class="metric-icon">⬆️</div>
                <div class="metric-number">{features[1]}</div>
                <div class="metric-label">Uppercase</div>
            </div>

            <div class="metric">
                <div class="metric-icon">🔤</div>
                <div class="metric-number">{features[2]}</div>
                <div class="metric-label">Lowercase</div>
            </div>

            <div class="metric">
                <div class="metric-icon">123</div>
                <div class="metric-number">{features[3]}</div>
                <div class="metric-label">Numbers</div>
            </div>

            <div class="metric">
                <div class="metric-icon">@#</div>
                <div class="metric-number">{features[4]}</div>
                <div class="metric-label">Special Characters</div>
            </div>

        </div>
        """

        st.html(metric_html)


        # ================================================
        # RECOMMENDATIONS
        # ================================================

        recommendations = []

        if features[0] >= 8:
            recommendations.append(
                "✅ Password length is good."
            )
        else:
            recommendations.append(
                "❌ Use at least 8 characters."
            )

        if features[1] > 0:
            recommendations.append(
                "✅ Contains uppercase letters."
            )
        else:
            recommendations.append(
                "❌ Add uppercase letters."
            )

        if features[2] > 0:
            recommendations.append(
                "✅ Contains lowercase letters."
            )
        else:
            recommendations.append(
                "❌ Add lowercase letters."
            )

        if features[3] > 0:
            recommendations.append(
                "✅ Contains numbers."
            )
        else:
            recommendations.append(
                "❌ Add numbers."
            )

        if features[4] > 0:
            recommendations.append(
                "✅ Contains special characters."
            )
        else:
            recommendations.append(
                "❌ Add special characters."
            )


        recommendation_html = ""

        for item in recommendations:

            recommendation_html += f"""
            <div class="info-item">
                {item}
            </div>
            """


        # ================================================
        # TIPS
        # ================================================

        tips_html = """
        <div class="info-card">

            <div class="info-title">
                💡 Tips for Strong Passwords
            </div>

            <div class="info-item">
                🔐 <b>Use longer passwords</b><br>
                Use 12 or more characters when possible.
            </div>

            <div class="info-item">
                🔢 <b>Mix character types</b><br>
                Combine uppercase, lowercase, numbers and symbols.
            </div>

            <div class="info-item">
                ⚠️ <b>Avoid common patterns</b><br>
                Avoid simple words, names and repeated sequences.
            </div>

            <div class="info-item">
                ✨ <b>Make it unique</b><br>
                Avoid reusing the same password on different accounts.
            </div>

        </div>
        """


        left_column = f"""
        <div class="info-card">

            <div class="info-title">
                🛡️ Security Recommendations
            </div>

            {recommendation_html}

        </div>
        """

        st.html(left_column)

        st.html(tips_html)


# =========================================================
# FOOTER
# =========================================================

st.html("""
<div class="footer">

    🔐 <b>AI Password Strength Detector</b>

    <div class="footer-small">
        Built with Python • Streamlit • Scikit-learn
    </div>

    <div class="footer-small">
        Educational Cybersecurity Project
    </div>

</div>
""")

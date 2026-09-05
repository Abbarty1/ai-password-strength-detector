import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Password Strength Detector",
    page_icon="🔐",
    layout="wide"
)


# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #f5f7fb;
    }

    /* Remove default top spacing */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* HERO SECTION */
    .hero {
        background: linear-gradient(
            135deg,
            #050b2c 0%,
            #11154d 50%,
            #24105a 100%
        );

        padding: 45px 45px 50px 45px;
        border-radius: 0 0 30px 30px;
        color: white;
        margin-bottom: 30px;
    }

    .brand {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 45px;
    }

    .brand-icon {
        font-size: 30px;
        vertical-align: middle;
        margin-right: 10px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 18px;
    }

    .hero-title span {
        color: #a855f7;
    }

    .hero-description {
        font-size: 18px;
        color: #d8dcf0;
        max-width: 600px;
        line-height: 1.6;
    }

    .ai-badge {
        background: rgba(168, 85, 247, 0.12);
        border: 1px solid #8b5cf6;
        border-radius: 20px;
        padding: 10px 18px;
        display: inline-block;
        color: #d8b4fe;
        font-weight: 600;
        margin-bottom: 25px;
    }

    /* Cards */
    .card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 30px rgba(15, 23, 42, 0.06);
        border: 1px solid #e9edf5;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #17203a;
        margin-bottom: 18px;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        border: 1px solid #e8ecf4;
        min-height: 145px;
    }

    .metric-icon {
        font-size: 28px;
        margin-bottom: 10px;
    }

    .metric-number {
        font-size: 30px;
        font-weight: 800;
        color: #17203a;
    }

    .metric-label {
        color: #64748b;
        font-size: 14px;
    }

    /* Security tips */
    .tip {
        padding: 13px 0;
        border-bottom: 1px solid #edf0f5;
        color: #334155;
    }

    .tip:last-child {
        border-bottom: none;
    }

    /* Footer */
    .footer {
        background: #070d2c;
        color: white;
        padding: 25px;
        border-radius: 20px;
        margin-top: 25px;
        text-align: center;
    }

    .footer-small {
        color: #9ca8c5;
        font-size: 13px;
        margin-top: 5px;
    }

    /* Streamlit input */
    div[data-baseweb="input"] {
        border-radius: 12px;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 52px;
        font-size: 17px;
        font-weight: 700;
        background: linear-gradient(
            90deg,
            #8b5cf6,
            #3b82f6
        );
        color: white;
        border: none;
    }

    .stButton > button:hover {
        opacity: 0.9;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# TRAINING DATA
# =========================================================

data = {
    "length": [
        4, 5, 6, 6, 7, 7, 8, 8,
        8, 9, 9, 10, 10, 10, 11, 11,
        12, 12, 13, 14, 15, 16, 17, 18
    ],

    "uppercase": [
        0, 0, 0, 0, 0, 0, 0, 1,
        0, 1, 1, 1, 1, 1, 1, 1,
        1, 2, 2, 2, 2, 2, 3, 3
    ],

    "lowercase": [
        4, 5, 6, 6, 7, 7, 8, 7,
        8, 7, 8, 7, 8, 6, 8, 7,
        7, 7, 8, 8, 8, 9, 9, 10
    ],

    "numbers": [
        0, 0, 0, 0, 0, 1, 0, 0,
        1, 1, 1, 2, 2, 3, 2, 3,
        3, 3, 3, 3, 4, 4, 4, 4
    ],

    "special": [
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 2, 2, 2
    ],

    "strength": [
        "Weak", "Weak", "Weak", "Weak",
        "Weak", "Weak", "Weak", "Medium",
        "Medium", "Medium", "Medium", "Medium",
        "Medium", "Medium", "Medium", "Medium",
        "Strong", "Strong", "Strong", "Strong",
        "Strong", "Strong", "Strong", "Strong"
    ]
}

df = pd.DataFrame(data)


# =========================================================
# MACHINE LEARNING MODEL
# =========================================================

X = df[
    [
        "length",
        "uppercase",
        "lowercase",
        "numbers",
        "special"
    ]
]

y = df["strength"]

model = DecisionTreeClassifier(
    max_depth=5,
    random_state=42
)

model.fit(X, y)


# =========================================================
# PASSWORD FEATURE EXTRACTION
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
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero">

    <div class="brand">
        <span class="brand-icon">🔐</span>
        AI Password Strength Detector
    </div>

    <div class="ai-badge">
        🤖 Powered by Machine Learning
    </div>

    <div class="hero-title">
        AI Password<br>
        <span>Strength Detector</span>
    </div>

    <div class="hero-description">
        Our machine learning model analyzes password
        characteristics and predicts their strength.
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# PASSWORD INPUT
# =========================================================

st.markdown("""
<div class="card">
    <div class="section-title">
        🔑 Check Your Password
    </div>
</div>
""", unsafe_allow_html=True)

password = st.text_input(
    "Enter a test password:",
    type="password",
    placeholder="Enter your password here..."
)

show_password = st.checkbox("Show password")

if show_password:
    password = st.text_input(
        "Password",
        value=password,
        type="default"
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


        # =================================================
        # RESULT
        # =================================================

        st.markdown(
            '<div class="card"><div class="section-title">'
            '📊 Overall Strength</div>',
            unsafe_allow_html=True
        )

        if prediction == "Weak":

            st.error("🔴 WEAK PASSWORD")
            message = (
                "This password needs improvement."
            )

        elif prediction == "Medium":

            st.warning("🟡 MEDIUM PASSWORD")
            message = (
                "This password has moderate strength."
            )

        else:

            st.success("🟢 STRONG PASSWORD")
            message = (
                "This password has a strong combination "
                "of characters."
            )

        st.write(message)

        st.progress(min(confidence / 100, 1.0))

        st.write(
            f"**AI Prediction Confidence: "
            f"{confidence:.1f}%**"
        )

        st.markdown("</div>", unsafe_allow_html=True)


        # =================================================
        # PASSWORD ANALYSIS
        # =================================================

        st.markdown(
            '<div class="card"><div class="section-title">'
            '📈 Password Analysis</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        metrics = [
            ("🔢", features[0], "Length"),
            ("⬆️", features[1], "Uppercase"),
            ("🔤", features[2], "Lowercase"),
            ("🔢", features[3], "Numbers"),
            ("@#", features[4], "Special Characters")
        ]

        columns = [
            col1, col2, col3, col4, col5
        ]

        for column, metric in zip(columns, metrics):

            icon, number, label = metric

            with column:

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-icon">
                            {icon}
                        </div>

                        <div class="metric-number">
                            {number}
                        </div>

                        <div class="metric-label">
                            {label}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("</div>", unsafe_allow_html=True)


        # =================================================
        # RECOMMENDATIONS
        # =================================================

        col1, col2 = st.columns(2)


        with col1:

            st.markdown(
                '<div class="card">'
                '<div class="section-title">'
                '🛡️ Security Recommendations'
                '</div>',
                unsafe_allow_html=True
            )

            recommendations = []

            if features[0] < 8:
                recommendations.append(
                    "❌ Use at least 8 characters."
                )
            else:
                recommendations.append(
                    "✅ Password length is good."
                )

            if features[1] == 0:
                recommendations.append(
                    "❌ Add uppercase letters."
                )
            else:
                recommendations.append(
                    "✅ Contains uppercase letters."
                )

            if features[2] == 0:
                recommendations.append(
                    "❌ Add lowercase letters."
                )
            else:
                recommendations.append(
                    "✅ Contains lowercase letters."
                )

            if features[3] == 0:
                recommendations.append(
                    "❌ Add numbers."
                )
            else:
                recommendations.append(
                    "✅ Contains numbers."
                )

            if features[4] == 0:
                recommendations.append(
                    "❌ Add special characters."
                )
            else:
                recommendations.append(
                    "✅ Contains special characters."
                )

            for item in recommendations:

                st.markdown(
                    f'<div class="tip">{item}</div>',
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)


        # =================================================
        # PASSWORD TIPS
        # =================================================

        with col2:

            st.markdown(
                '<div class="card">'
                '<div class="section-title">'
                '💡 Tips for Strong Passwords'
                '</div>',
                unsafe_allow_html=True
            )

            tips = [
                (
                    "🔐",
                    "Use longer passwords",
                    "Aim for 12 or more characters."
                ),
                (
                    "🔢",
                    "Mix character types",
                    "Use letters, numbers and symbols."
                ),
                (
                    "⚠️",
                    "Avoid common patterns",
                    "Avoid simple words and sequences."
                ),
                (
                    "✨",
                    "Make it unique",
                    "Don't reuse the same password."
                )
            ]

            for icon, title, description in tips:

                st.markdown(
                    f"""
                    <div class="tip">
                        <b>{icon} {title}</b><br>
                        <span style="color:#64748b;">
                        {description}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

    🔐 <b>AI Password Strength Detector</b>

    <div class="footer-small">
        Built with Python • Streamlit • Scikit-learn
    </div>

    <div class="footer-small">
        Educational cybersecurity project
    </div>

</div>
""", unsafe_allow_html=True)

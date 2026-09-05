import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="AI Password Strength Detector",
    page_icon="🔐",
    layout="centered"
)


# ==========================================
# TRAINING DATA
# ==========================================

data = {
    "length": [
        4, 5, 6, 6, 7, 7, 8, 8, 8, 9,
        9, 10, 10, 10, 11, 11, 12, 12, 13, 14,
        15, 16, 17, 18
    ],

    "uppercase": [
        0, 0, 0, 0, 0, 0, 0, 1, 0, 1,
        1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
        2, 2, 3, 3
    ],

    "lowercase": [
        4, 5, 6, 6, 7, 7, 8, 7, 8, 7,
        8, 7, 8, 6, 8, 7, 7, 7, 8, 8,
        8, 9, 9, 10
    ],

    "numbers": [
        0, 0, 0, 0, 0, 1, 0, 0, 1, 1,
        1, 2, 2, 3, 2, 3, 3, 3, 3, 3,
        4, 4, 4, 4
    ],

    "special": [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
        1, 2, 2, 2
    ],

    "strength": [
        "Weak", "Weak", "Weak", "Weak", "Weak", "Weak",
        "Weak", "Medium", "Medium", "Medium", "Medium",
        "Medium", "Medium", "Medium", "Medium", "Medium",
        "Strong", "Strong", "Strong", "Strong", "Strong",
        "Strong", "Strong", "Strong"
    ]
}

df = pd.DataFrame(data)


# ==========================================
# TRAIN THE MACHINE LEARNING MODEL
# ==========================================

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


# ==========================================
# PASSWORD ANALYSIS
# ==========================================

def analyze_password(password):

    length = len(password)

    uppercase = sum(
        1 for character in password
        if character.isupper()
    )

    lowercase = sum(
        1 for character in password
        if character.islower()
    )

    numbers = sum(
        1 for character in password
        if character.isdigit()
    )

    special = sum(
        1 for character in password
        if not character.isalnum()
    )

    return [
        length,
        uppercase,
        lowercase,
        numbers,
        special
    ]


# ==========================================
# APPLICATION TITLE
# ==========================================

st.title("🔐 AI Password Strength Detector")

st.write(
    "Check the strength of a password using "
    "a machine-learning model."
)

st.info(
    "For demonstration purposes, please use a "
    "test password rather than your real password."
)


# ==========================================
# PASSWORD INPUT
# ==========================================

password = st.text_input(
    "Enter a test password:",
    type="password"
)


# ==========================================
# CHECK PASSWORD
# ==========================================

if st.button("🔍 Check Password"):

    if password == "":

        st.warning("Please enter a password.")

    else:

        features = analyze_password(password)

        prediction = model.predict([features])[0]

        probabilities = model.predict_proba([features])[0]

        confidence = max(probabilities) * 100


        # ==================================
        # DISPLAY RESULT
        # ==================================

        st.subheader("Result")

        if prediction == "Weak":

            st.error("🔴 WEAK PASSWORD")

        elif prediction == "Medium":

            st.warning("🟡 MEDIUM PASSWORD")

        else:

            st.success("🟢 STRONG PASSWORD")


        st.write(
            f"**AI Prediction Confidence:** "
            f"{confidence:.1f}%"
        )


        # ==================================
        # PASSWORD FEATURES
        # ==================================

        st.subheader("Password Analysis")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Length",
                features[0]
            )

            st.metric(
                "Uppercase",
                features[1]
            )

            st.metric(
                "Lowercase",
                features[2]
            )

        with col2:

            st.metric(
                "Numbers",
                features[3]
            )

            st.metric(
                "Special Characters",
                features[4]
            )


        # ==================================
        # RECOMMENDATIONS
        # ==================================

        st.subheader("Security Recommendations")

        recommendations = []

        if features[0] < 8:

            recommendations.append(
                "Use at least 8 characters."
            )

        if features[1] == 0:

            recommendations.append(
                "Add uppercase letters."
            )

        if features[2] == 0:

            recommendations.append(
                "Add lowercase letters."
            )

        if features[3] == 0:

            recommendations.append(
                "Add numbers."
            )

        if features[4] == 0:

            recommendations.append(
                "Add special characters such as @, #, or !."
            )

        if recommendations:

            for item in recommendations:

                st.write("• " + item)

        else:

            st.success(
                "✅ Your password contains a good "
                "combination of characters."
            )


# ==========================================
# ABOUT THE PROJECT
# ==========================================

st.divider()

st.caption(
    "This educational application uses a "
    "Decision Tree machine-learning classifier "
    "to predict password strength."
)

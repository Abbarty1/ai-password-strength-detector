import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


# ---------------------------------------------------
# 1. CREATE A SMALL TRAINING DATASET
# ---------------------------------------------------

data = {
    "length": [
        4, 6, 6, 7, 8,
        8, 9, 10, 10, 11,
        12, 12, 13, 14, 15
    ],

    "uppercase": [
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1
    ],

    "lowercase": [
        4, 6, 3, 7, 8,
        6, 7, 7, 6, 7,
        6, 7, 8, 9, 10
    ],

    "numbers": [
        0, 0, 3, 0, 0,
        1, 1, 2, 3, 2,
        3, 3, 3, 3, 3
    ],

    "special": [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        1, 1, 2, 2, 2
    ],

    "strength": [
        "Weak", "Weak", "Weak", "Weak", "Weak",
        "Medium", "Medium", "Medium", "Medium", "Medium",
        "Strong", "Strong", "Strong", "Strong", "Strong"
    ]
}

df = pd.DataFrame(data)


# ---------------------------------------------------
# 2. TRAIN THE AI MODEL
# ---------------------------------------------------

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

model = DecisionTreeClassifier(random_state=42)

model.fit(X, y)


# ---------------------------------------------------
# 3. PASSWORD FEATURE EXTRACTION
# ---------------------------------------------------

def analyze_password(password):

    length = len(password)

    uppercase = sum(1 for char in password if char.isupper())

    lowercase = sum(1 for char in password if char.islower())

    numbers = sum(1 for char in password if char.isdigit())

    special = sum(
        1 for char in password
        if not char.isalnum()
    )

    return [
        length,
        uppercase,
        lowercase,
        numbers,
        special
    ]


# ---------------------------------------------------
# 4. WEBSITE DESIGN
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Password Strength Detector",
    page_icon="🔐"
)

st.title("🔐 AI Password Strength Detector")

st.write(
    "Enter a password and our machine-learning model "
    "will predict its strength."
)

password = st.text_input(
    "Enter your password:",
    type="password"
)


# ---------------------------------------------------
# 5. PREDICTION
# ---------------------------------------------------

if st.button("Check Password"):

    if password == "":
        st.warning("Please enter a password.")

    else:

        features = analyze_password(password)

        prediction = model.predict([features])[0]

        st.subheader("Prediction")

        if prediction == "Weak":

            st.error("🔴 Password Strength: WEAK")

        elif prediction == "Medium":

            st.warning("🟡 Password Strength: MEDIUM")

        else:

            st.success("🟢 Password Strength: STRONG")


        # Show password characteristics

        st.subheader("Password Analysis")

        st.write(
            f"**Length:** {features[0]} characters"
        )

        st.write(
            f"**Uppercase letters:** {features[1]}"
        )

        st.write(
            f"**Lowercase letters:** {features[2]}"
        )

        st.write(
            f"**Numbers:** {features[3]}"
        )

        st.write(
            f"**Special characters:** {features[4]}"
        )

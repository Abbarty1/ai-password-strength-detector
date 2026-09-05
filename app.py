import streamlit as st
import re

st.set_page_config(
    page_title="AI Password Strength Detector",
    page_icon="🔐"
)

st.title("🔐 AI Password Strength Detector")

st.write(
    "Enter a password to check its strength and receive "
    "security recommendations."
)


def check_password(password):
    score = 0
    suggestions = []

    # Password length
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    # Lowercase letters
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    # Uppercase letters
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    # Numbers
    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    # Special characters
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        suggestions.append(
            "Add a special character such as @, #, or !."
        )

    # Determine password strength
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, suggestions


password = st.text_input(
    "Enter your password:",
    type="password"
)


if st.button("Check Password"):

    if not password:
        st.warning("Please enter a password.")

    else:
        strength, suggestions = check_password(password)

        st.subheader("Result")

        if strength == "Weak":
            st.error("🔴 Password Strength: WEAK")

        elif strength == "Medium":
            st.warning("🟡 Password Strength: MEDIUM")

        else:
            st.success("🟢 Password Strength: STRONG")

        if suggestions:
            st.subheader("How to improve your password")

            for suggestion in suggestions:
                st.write("• " + suggestion)

        else:
            st.success(
                "✅ Your password meets all the basic requirements."
            )

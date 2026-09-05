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

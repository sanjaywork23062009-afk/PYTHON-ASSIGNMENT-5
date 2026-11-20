POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirt", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}

def score(text):
    words = text.lower().replace(".", " ").replace(",", " ").split()
    total = 0
    negated = False
    for i, word in enumerate(words):
        if word in NEGATORS:
            negated = True
            continue
        val = 0
        if word in POSITIVE:
            val = 1
        elif word in NEGATIVE:
            val = -1
        
        if val != 0:
            if negated:
                val = -val
            total += val
            negated = False
        else:
            if word not in NEGATORS:
                negated = False
    return total

def label(text):
    s = score(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"

for c in ["Roads are clean and the bus was fast.",
"Smoke from the factory, air is bad.",
"The staff were not helpful.",
"Not bad, service improved."]:
    print(f"{label(c):8} | {c}")
```[cite: 13, 14]

import re

# 1:
text = "John Doe: 28, Alice Smith: 34, Bob: 19, Charlie Brown: 45"

matches = re.findall(r"([A-Za-z ]+):\s*(\d+)", text)

for name, age in matches:
    print(f"{name.strip()} - {age}")
print("\n")

# 2:
codes = [
    "AB-1234",
    "XYZ-9876A",
    "A-1234",
    "ABCD-1234",
    "XY-12A",
    "PQ-4567B"
]

pattern = r"^[A-Z]{2,3}-\d{4}[A-Z]?$"

for code in codes:
    if re.fullmatch(pattern, code):
        print("Valid")
    else:
        print("Invalid")
print("\n")

# 3:
text = "Contact us at 9876543210 or 987-654-3210. You can also call (987) 654-3210 or 987 654 3210 for support."

pattern = r"(?:\(\d{3}\)|\d{3})[- ]?\d{3}[- ]?\d{4}"

def mask_phone(match):
    phone = match.group()

    digits = re.sub(r"\D", "", phone)

    return "******" + digits[-4:]

result = re.sub(pattern, mask_phone, text)

print(f"{result}\n")

#4:
text = """Great session today! Thanks @john_doe and @alice_smith for the insights.
#Python #Regex #CodingLife Let's meet again @bob_92 #Learning"""

hashtags = re.findall(r"#[A-Za-z0-9_]+", text)
mentions = re.findall(r"@[A-Za-z0-9_]+", text)

print("Hashtags:", ", ".join(hashtags))
print("Mentions:", ", ".join(mentions))
from redaction_config import SENSITIVE
import re

with open("report.txt", "r") as file:
    redacted_text = file.read()
    counts = {}
    for word in SENSITIVE:
        redacted_text, count = re.subn(word, "[REDACTED]", redacted_text, flags=re.IGNORECASE)
        counts[word] = count

    with open("report_redacted.txt", "w") as f:
        f.write(redacted_text)

    print("Redaction complete.")
    for word, count in counts.items():
        print(f"{word} -> {count} occurrences redacted")
    print("Output saved to report_redacted.txt")
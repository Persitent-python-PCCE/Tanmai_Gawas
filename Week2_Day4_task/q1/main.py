from collections import Counter
from log_utils import read_logs

logs = read_logs("app.log")

counts = Counter(level for level, message in logs)

levels = ["INFO", "WARNING", "ERROR", "DEBUG"]

errors = [message for level, message in logs if level == "ERROR"]

print("=== Log Summary ===")
for level in levels:
    print(f"{level} : {counts[level]}")

print("Errors found:")
for error in errors:
    print(f"- {error}")

with open("log_summary.txt", "w") as file:
    file.write("=== Log Summary ===\n")

    for level in levels:
        file.write(f"{level} : {counts[level]}\n")

    file.write("Errors found:\n")
    for error in errors:
        file.write(f"- {error}\n")
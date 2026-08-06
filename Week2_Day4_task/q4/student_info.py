import csv
from grading import get_grade

report = {}

passed = 0
failed = 0

with open("students_result.csv", "w") as file:
    file.write("roll_no,name,maths,physics,chemistry,total,average,grade\n")

with open("students.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        student_name = row["name"]

        maths = int(row["maths"])
        physics = int(row["physics"])
        chemistry = int(row["chemistry"])

        student_total = maths + physics + chemistry

        report[student_name] = student_total / 3

        result = (row["roll_no"], student_name, maths, physics, chemistry, student_total, round(report[student_name],2), get_grade(report[student_name]))

        with open("students_result.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(result)
        if report[student_name] >= 40:
            passed += 1
        else:
            failed += 1

topper = max(report, key=lambda name: report[name])

print(f"Processed {len(report)} students -> students_result.csv")
print(f"Class Topper : {topper} (avg {report[topper]:.2f})")
print(f"Passed : {passed} | Failed : {failed}")
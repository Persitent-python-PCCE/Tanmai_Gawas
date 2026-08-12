import datetime
import json
import random

def generate_unique_id(data):
    existing_ids = {item["student_id"] for item in data}

    while True:
        new_id = random.randint(1, 100)
        if new_id not in existing_ids:
            return new_id
    
def generate_unique_name(available_names, used_names):
    remaining_names = [name for name in available_names if name not in used_names]

    if not remaining_names:
        raise ValueError("No unique names available")

    return random.choice(remaining_names)

def check_if_pass(data):
    ifpass = True
    for key, value in data.items():
        if value < 40:
            ifpass = False
    return "Pass" if ifpass else "Fail"

def get_exam_date():
    year = 2026

    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)

    random_date = start_date + datetime.timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )

    return random_date.strftime("%Y-%m-%d")

def generate_student_list():
    stud_names = ["Aarav", "Sofia", "Daniel", "Maya", "Ethan", "Ananya", "Lucas", "Priya", "Noah", "Kiara"]
    departments = ["Computer Science","Information Technology","Electronics","Mechanical"]
    n = int(input("Enter number of students: "))
    stud_list = []
    used_names = []

    for i in range(n):
        student = {}

        stud_marks = {
            "Python": random.randint(0, 100),
            "Database": random.randint(0, 100),
            "Computer Networks": random.randint(0, 100)
        }

        total = sum(stud_marks.values())
        avg = total / 3

        student["student_id"] = generate_unique_id(stud_list)
        student["name"] = generate_unique_name(stud_names, used_names)
        student["age"] = random.randint(18, 25)
        student["department"] = random.choice(departments)
        student["marks"] = stud_marks
        student["total"] = total
        student["average"] = round(avg,2)
        student["result"] = check_if_pass(stud_marks)
        student["exam_date"] = get_exam_date()

        stud_list.append(student)
        used_names.append(student["name"])

    with open("q1/students.json", "w") as file:
        json.dump(stud_list, file, indent=4)

def main():
    generate_student_list()
    
if __name__ == "__main__":
    main()

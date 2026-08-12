import random
import datetime
import xml.etree.ElementTree as ET
import json

def generate_employee_id(employees):
    existing_ids = {employee["employee_id"] for employee in employees}

    while True:
        employee_id = random.randint(1000, 9999)

        if employee_id not in existing_ids:
            return employee_id

def generate_employee_name():
    names = [
        "Arun Kumar",
        "Priya Sharma",
        "Rahul Mehta",
        "Sneha Patil",
        "Amit Singh",
        "Neha Desai",
        "Rohan Nair",
        "Ananya Rao"
    ]

    return random.choice(names)

def generate_department():
    departments = [
        "IT",
        "HR",
        "Finance",
        "Sales",
        "Operations"
    ]

    return random.choice(departments)


def generate_joining_date():
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2025, 12, 31)

    random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

    return random_date.strftime("%Y-%m-%d")


def generate_attendance(year, month):
    attendance = []

    start_date = datetime.date(year, month, 1)

    if month == 12:
        next_month = datetime.date(year + 1, 1, 1)
    else:
        next_month = datetime.date(year, month + 1, 1)

    current_date = start_date

    while current_date < next_month:

        status = random.choices(
            ["Present", "Absent", "Leave"],
            weights=[80, 10, 10]
        )[0]

        attendance.append({"date": current_date.strftime("%Y-%m-%d"), "status": status})

        current_date += datetime.timedelta(days=1)

    return attendance


def generate_employees(number_of_employees, year, month):

    employees = []

    for i in range(number_of_employees):

        employee = {}

        employee["employee_id"] = generate_employee_id(
            employees
        )

        employee["name"] = generate_employee_name()

        employee["department"] = generate_department()

        employee["joining_date"] = generate_joining_date()

        employee["attendance"] = generate_attendance(
            year,
            month
        )

        employees.append(employee)

    return employees


def save_to_xml(employees):

    root = ET.Element("employees")

    for employee in employees:

        employee_element = ET.SubElement(root,"employee")

        id_element = ET.SubElement(employee_element, "id")
        id_element.text = str(employee["employee_id"])

        name_element = ET.SubElement(employee_element,"name")
        name_element.text = employee["name"]

        department_element = ET.SubElement(employee_element, "department")
        department_element.text = employee["department"]

        joining_date_element = ET.SubElement(employee_element,"joining_date")
        joining_date_element.text = employee["joining_date"]

        attendance_element = ET.SubElement(employee_element,"attendance")

        for record in employee["attendance"]:

            day_element = ET.SubElement(attendance_element,"day")

            day_element.set("date",record["date"])

            day_element.text = record["status"]

    tree = ET.ElementTree(root)

    ET.indent(tree, space="    ", level=0)

    tree.write("employees.xml")

def generate_report():

    tree = ET.parse("employees.xml")

    root = tree.getroot()

    report = []

    for employee in root.findall("employee"):

        employee_id = int(employee.find("id").text)

        name = employee.find("name").text

        department = employee.find("department").text

        attendance = employee.find("attendance")

        total_working_days = 0
        present_days = 0
        absent_days = 0
        leave_days = 0

        for day in attendance.findall("day"):

            total_working_days += 1

            status = day.text

            if status == "Present":
                present_days += 1

            elif status == "Absent":
                absent_days += 1

            elif status == "Leave":
                leave_days += 1

        attendance_percentage = round((present_days / total_working_days) * 100,2)

        employee_report = {
            "employee_id": employee_id,
            "name": name,
            "department": department,
            "total_working_days": total_working_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "leave_days": leave_days,
            "attendance_percentage": attendance_percentage
        }

        report.append(employee_report)

    return report


def save_report(report):

    with open("attendance_report.json","w") as file:

        json.dump(report,file,indent=4)


def display_report(report):

    print("\n========================================")
    print("       Employee Attendance Report")
    print("========================================")

    for employee in report:

        print(f"Employee ID : {employee['employee_id']}")

        print(f"Name : {employee['name']}")

        print(f"Department : {employee['department']}")

        print(f"Working Days : {employee['total_working_days']}")

        print(f"Present : {employee['present_days']}")

        print(f"Absent : {employee['absent_days']}")

        print(f"Leave : {employee['leave_days']}")

        print(f"Attendance : {employee['attendance_percentage']:.2f}%")

        print("----------------------------------------")


def main():

    try:
        number_of_employees = int(input("Enter number of employees: "))

        if number_of_employees <= 0:
            print("Number of employees must be greater than 0.")
            return

        year = int(input("Enter year: "))

        month = int(input("Enter month: "))

        if month < 1 or month > 12:
            print("Month must be between 1 and 12.")
            return

    except ValueError:
        print("Please enter valid numbers.")
        return

    employees = generate_employees(number_of_employees,year,month)

    save_to_xml(employees)

    report = generate_report()

    save_report(report)

    display_report(report)

    print("\nAttendance report generated successfully.")

    print("XML File : employees.xml")
    print("JSON File: attendance_report.json")


if __name__ == "__main__":
    main()
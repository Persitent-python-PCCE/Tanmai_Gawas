class Employee{
    String id;
    String name;
    double baseSalary;

    Employee(){
        this.id = "E000";
        this.name = "Unknown";
    }

    Employee(String id, String name){
        this.id = id;
        this.name = name;
        this.baseSalary = 15000.0;
    }

    Employee(String id, String name, double baseSalary){
        this.id = id;
        this.name = name;
        this.baseSalary = baseSalary;
    }

    public void displayInfo(){
        System.out.println("ID: "+ this.id+"  | Name: "+this.name+" | Base Salary: "+this.baseSalary);
    }
}

class FullTimeEmployee extends Employee{
    double bonus;

    FullTimeEmployee(String id, String name, double baseSalary){
        super(id, name, baseSalary);
        this.bonus = 5000.0;
    }

    FullTimeEmployee(String id, String name, double baseSalary, double bonus){
        super(id, name, baseSalary);
        this.bonus = bonus;
    }

    public void displayInfo() {
        System.out.println("ID: " + this.id + "  | Name: " + this.name + " | Base Salary: " + this.baseSalary + " | Bonus: "+ this.bonus + " | Total Salary: "+ (this.baseSalary + this.bonus));
    }
}

class InternEmployee extends Employee{
    double stipend;
    int durationMonths;

    InternEmployee(String id, String name){
        super(id, name);
        this.stipend = 8000.0;
        this.durationMonths = 3;
    }

    InternEmployee(String id, String name, double stipend, int duration){
        super(id, name);
        this.stipend = stipend;
        this.durationMonths = duration;
    }

    public void displayInfo() {
        System.out.println("ID: " + this.id + "  | Name: " + this.name + " | Stipend: " + this.stipend+ " | Duration in Months: " + this.durationMonths);
    }
}

public class CompanyDemo{
    public static void main(String[] args) {
        // -- calls Employee no-arg constructor
        Employee e1 = new Employee();
        e1.displayInfo();

        // -- calls Employee(id, name) — baseSalary defaults to 15000
        Employee e2 = new Employee("E101", "Ravi");
        e2.displayInfo();

        // -- calls FullTimeEmployee(id, name, baseSalary) — bonus defaults to 5000
        FullTimeEmployee f1 = new FullTimeEmployee("E201", "Meena", 40000);
        f1.displayInfo();

        // -- calls FullTimeEmployee(id, name, baseSalary, bonus)
        FullTimeEmployee f2 = new FullTimeEmployee("E202", "Karthik", 50000, 8000);
        f2.displayInfo();

        // -- calls InternEmployee(id, name) — stipend & duration default
        InternEmployee i1 = new InternEmployee("E301", "Divya");
        i1.displayInfo();

        // -- calls InternEmployee(id, name, stipend, duration)
        InternEmployee i2 = new InternEmployee("E302", "Suresh", 12000, 6);
        i2.displayInfo();
    }
}
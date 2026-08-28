package q2;

public class BankDemo {
    public static void main(String[] args) {
        // TODO:
        // 1. Create one SavingsAccount and one CurrentAccount.
        // 2. Call all three overloaded deposit() forms.
        // 3. Trigger a failing withdraw() on Savings and a
        // successful (overdraft) one on Current.
        // 4. Store both in an Account[] and loop — call
        // calculateInterest() and displayDetails() on
        // Account references (runtime polymorphism).

        SavingsAccount s = new SavingsAccount("SB001", "Arul", 5000);
        CurrentAccount c = new CurrentAccount("CA001", "Priya", 20000);

        s.deposit(2000);                                 //on SB001
        c.deposit(5000, "UPI");                          //on CA001
        s.deposit(3000, "Cheque", "CHQ12345");          // on SB001

        s.withdraw(9500);  // on SB001   // FAILS — breaks minimum balance rule
        c.withdraw(30000);  //on CA001   // PASSES — overdraft used

        s.calculateInterest(); //on both
        c.calculateInterest();
        s.displayDetails();    //on both
        c.displayDetails();

    }
}

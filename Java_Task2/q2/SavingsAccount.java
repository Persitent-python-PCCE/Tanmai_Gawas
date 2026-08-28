package q2;

public class SavingsAccount extends Account {
    private double minBalance;
    private double interestRate;

    public SavingsAccount(String accountNumber, String holderName, double balance) {
        // TODO: super(...); minBalance = 1000; interestRate = 4.0;
        super(accountNumber, holderName, balance);
        this.minBalance = 1000.0;
        this.interestRate = 4.0;
    }

    @Override
    public boolean withdraw(double amount) {
        // TODO: allow only if (balance - amount) >= minBalance
        // else print "Withdrawal denied. Minimum balance of <min> must be maintained."
        if((this.balance - amount) >= this.minBalance){
            this.balance = this.balance - amount;
            System.out.println("Withdrawal successful."+ this.accountNumber + " balance: " + this.balance);
            return true;
        }
        System.out.println("Withdrawal denied. Minimum balance of 1000.0 must be maintained.");
        return false;
    }

    @Override
    public double calculateInterest() {
        // TODO: return balance * interestRate / 100
        return this.balance * interestRate / 100;
    }

    @Override
    public void displayDetails() {
        // TODO: print with Type=Savings and minBalance
        System.out.println("Account: " + this.accountNumber + " | Holder: " + this.holderName + "  | Balance: "+ this.balance +" | Type: Savings | Min Balance: "+ this.minBalance);

    }
}

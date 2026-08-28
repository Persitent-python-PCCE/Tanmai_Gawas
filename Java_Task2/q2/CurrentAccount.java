package q2;

public class CurrentAccount extends Account {
    private double overdraftLimit;

    public CurrentAccount(String accountNumber, String holderName, double balance) {
        // TODO: super(...); overdraftLimit = 10000;
        super(accountNumber, holderName, balance);
        this.overdraftLimit = 10000.0;
    }

    @Override
    public boolean withdraw(double amount) {
        // TODO: allow if (balance - amount) >= -overdraftLimit
        // print "Withdrawal successful (overdraft used)." when balance goes negative
        if((balance - amount) >= -overdraftLimit){
            this.balance = this.balance - amount;
            System.out.println("Withdrawal successful (overdraft used). CA001 balance: " + this.balance);
            return true;
        }
        System.out.println("Withdrawal denied.");
        return false;
    }

    @Override
    public double calculateInterest() {
        // TODO: print "Interest not applicable ..." and return 0
        System.out.println("Interest not applicable for Current Account " + this.accountNumber);
        return 0;
    }

    @Override
    public void displayDetails() {
        // TODO: print with Type=Current and overdraftLimit
        System.out.println("Account: "+this.accountNumber+" | Holder: "+this.holderName+" | Balance: "+this.balance+" | Type: Current | Overdraft Limit: "+this.overdraftLimit);
    }
}

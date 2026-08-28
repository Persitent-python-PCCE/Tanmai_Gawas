package q2;

public class Account {
    protected String accountNumber;
    protected String holderName;
    protected double balance;

    public Account(String accountNumber, String holderName, double balance) {
        // TODO: initialize fields
        this.accountNumber = accountNumber;
        this.holderName = holderName;
        this.balance = balance;
    }

    // ---- Overloaded deposit methods ----
    public void deposit(double amount) {
        // TODO: delegate to deposit(amount, "Cash")
        this.balance = this.balance + amount;
        System.out.println("Deposit successful. "+ this.accountNumber + "balance: " + this.balance);
    }

    public void deposit(double amount, String mode) {
        // TODO: validate amount > 0, add to balance,
        // print "Deposit via <mode> successful. <accNo> balance: <bal>"
        if(amount > 0){
        this.balance = this.balance + amount;
        System.out.println("Deposit via " + mode + " successful. " + this.accountNumber + " balance: "+ this.balance);
        }else{
            System.out.println("Cannot deposit amount less than 0.");
        }
    }

    public void deposit(double amount, String mode, String reference) {
        // TODO: validate amount > 0, add to balance,
        // print "Deposit via <mode> (Ref: <ref>) successful. ..."
        if (amount > 0) {
            this.balance = this.balance + amount;
            System.out.println(
                    "Deposit via " + mode + " (Ref:"+ reference +") successful. " + this.accountNumber + " balance: " + this.balance);
        } else {
            System.out.println("Cannot deposit amount less than 0.");
        }
    }

    // ---- Methods intended to be overridden ----
    public boolean withdraw(double amount) {
        // TODO: default deducts if balance >= amount; return success
        return false;
    }

    public double calculateInterest() {
        return 0;
    }

    public void displayDetails() {
        // TODO: print base details (accNo, holder, balance)
        System.out.println(this.accountNumber+" | Holder: " + this.holderName + " | Balance: " + this.balance);
    }
}

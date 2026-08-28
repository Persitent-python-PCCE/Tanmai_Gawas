package q3;

public class Electronics extends Product {

    private static final double GST_RATE = 18.0;

    private int warrantyMonths;

    public Electronics(
            String productId,
            String name,
            double basePrice,
            int quantity,
            int warrantyMonths) {

        super(productId, name, basePrice, quantity);
        this.warrantyMonths = warrantyMonths;
    }

    @Override
    public double calculateFinalPrice() {

        double gross = basePrice * quantity;

        gross = gross * (1 + GST_RATE / 100);

        return gross;
    }

    @Override
    public String getCategory() {
        return "Electronics";
    }

    public int getWarrantyMonths() {
        return warrantyMonths;
    }

    @Override
    public void display() {

        System.out.printf(
                "%s | %s | %s | Qty: %d | Base: %.1f | Final: %.2f (18%% GST, Warranty: %d months)%n",
                productId,
                name,
                getCategory(),
                quantity,
                basePrice * quantity,
                calculateFinalPrice(),
                warrantyMonths);
    }
}
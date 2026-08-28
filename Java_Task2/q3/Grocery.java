package q3;

public class Grocery extends Product {

    private static final double GST_RATE = 5.0;
    private static final int BULK_QTY = 10;
    private static final double BULK_DISCOUNT = 5.0;

    public Grocery(String productId, String name, double basePrice, int quantity) {
        super(productId, name, basePrice, quantity);
    }

    @Override
    public double calculateFinalPrice() {

        double gross = basePrice * quantity;

        if (quantity > BULK_QTY) {
            gross = gross * (1 - BULK_DISCOUNT / 100);
        }

        gross = gross * (1 + GST_RATE / 100);

        return gross;
    }

    @Override
    public String getCategory() {
        return "Grocery";
    }
}
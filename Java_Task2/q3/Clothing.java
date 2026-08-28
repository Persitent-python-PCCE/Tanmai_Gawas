package q3;

public class Clothing extends Product {

    private static final double GST_RATE = 12.0;
    private static final double SEASONAL_DISCOUNT = 20.0;

    public Clothing(
            String productId,
            String name,
            double basePrice,
            int quantity) {

        super(productId, name, basePrice, quantity);
    }

    @Override
    public double calculateFinalPrice() {

        double gross = basePrice * quantity;

        // 20% discount
        gross = gross * (1 - SEASONAL_DISCOUNT / 100);

        // 12% GST
        gross = gross * (1 + GST_RATE / 100);

        return gross;
    }

    @Override
    public String getCategory() {
        return "Clothing";
    }

    @Override
    public void display() {

        System.out.printf(
                "%s | %s | %s | Qty: %d | Base: %.1f | Final: %.2f (20%% discount, 12%% GST)%n",
                productId,
                name,
                getCategory(),
                quantity,
                basePrice * quantity,
                calculateFinalPrice());
    }
}
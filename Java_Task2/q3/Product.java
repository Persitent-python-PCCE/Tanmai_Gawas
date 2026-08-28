package q3;

public abstract class Product {

    protected String productId;
    protected String name;
    protected double basePrice;
    protected int quantity;

    public Product(String productId, String name, double basePrice, int quantity) {
        this.productId = productId;
        this.name = name;
        this.basePrice = basePrice;
        this.quantity = quantity;
    }

    public abstract double calculateFinalPrice();

    public abstract String getCategory();

    public void display() {
        System.out.printf(
                "%s | %s | %s | Qty: %d | Base: %.1f | Final: %.2f%n",
                productId,
                name,
                getCategory(),
                quantity,
                basePrice * quantity,
                calculateFinalPrice());
    }
}
package q3;

import java.util.ArrayList;
import java.util.List;

public class Bill {

    private List<Product> products = new ArrayList<>();

    public void addProduct(Product p) {
        products.add(p);
    }

    public void generateBill() {

        System.out.println("===== SUPERMARKET BILL =====");

        double grandTotal = 0;

        for (Product p : products) {

            p.display();

            grandTotal += p.calculateFinalPrice();
        }

        System.out.println("============================");
        System.out.println("Total Items: " + products.size());

        System.out.printf("Grand Total: %.2f%n", grandTotal);
    }

    public static void main(String[] args) {

        Grocery g1 = new Grocery(
                "G001",
                "Rice 5kg",
                300,
                3);

        Electronics e1 = new Electronics(
                "E001",
                "Headphones",
                2000,
                1,
                12);

        Clothing c1 = new Clothing(
                "C001",
                "T-Shirt",
                800,
                2);

        Grocery g2 = new Grocery(
                "G002",
                "Sugar 1kg",
                50,
                15);

        Bill bill = new Bill();

        bill.addProduct(g1);
        bill.addProduct(e1);
        bill.addProduct(c1);
        bill.addProduct(g2);

        bill.generateBill();
    }
}
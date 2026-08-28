package Java_task1.Q2;

import java.util.Scanner;

public class CompressString {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        String str = sc.nextLine();

        for (int i = 0; i < str.length(); i++) {

            int count = 1;

            while (i + 1 < str.length() && str.charAt(i) == str.charAt(i + 1)) {
                count++;
                i++;
            }

            System.out.print(str.charAt(i) + "" + count);
        }
        sc.close();
    }
}

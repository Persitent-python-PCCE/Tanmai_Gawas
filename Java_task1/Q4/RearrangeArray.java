package Java_task1.Q4;

import java.util.Scanner;

public class RearrangeArray {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter Size of array: ");
        int n = sc.nextInt();

        int[] arr = new int[n];

        
        for (int i = 0; i < n; i++) {
            System.out.print("Enter element at "+i+": ");
            arr[i] = sc.nextInt();
        }

        System.out.print("\nEnter String:");
        String str = sc.next();
        System.out.println();

        int[] result = new int[n];
        int index = 0;

        for (int i = 0; i < n; i++) {
            if (str.charAt(i) == 'A') {
                result[index] = arr[i];
                index++;
            }
        }


        for (int i = 0; i < n; i++) {
            if (str.charAt(i) == 'D') {
                result[index] = arr[i];
                index++;
            }
        }

        for (int i = 0; i < n; i++) {
            System.out.print(result[i] + " ");
        }
        sc.close();
    }
}

package Java_task1.Q1;

import java.util.Arrays;
import java.util.Scanner;

public class LongestConsecutive {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int[] arr = new int[n];

        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        Arrays.sort(arr);

        int count = 1;
        int max = 1;

        for (int i = 1; i < n; i++) {

            if (arr[i] == arr[i - 1]) {
                continue;
            }

            if (arr[i] == arr[i - 1] + 1) {
                count++;
            } else {
                count = 1;
            }

            if (count > max) {
                max = count;
            }
        }

        System.out.println(max);
        sc.close();
    }
}

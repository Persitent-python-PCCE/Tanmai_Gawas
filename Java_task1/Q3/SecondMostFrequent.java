package Java_task1.Q3;

import java.util.Scanner;

public class SecondMostFrequent {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        String str = sc.nextLine();

        int[] freq = new int[26];

        for (int i = 0; i < str.length(); i++) {
            char ch = str.charAt(i);
            freq[ch - 'a']++;
        }

        int highest = 0;
        int secondHighest = 0;

        for (int i = 0; i < 26; i++) {

            if (freq[i] > highest) {
                secondHighest = highest;
                highest = freq[i];
            } else if (freq[i] > secondHighest && freq[i] < highest) {
                secondHighest = freq[i];
            }
        }

        for (int i = 0; i < str.length(); i++) {
            char ch = str.charAt(i);

            if (freq[ch - 'a'] == secondHighest) {
                System.out.println(ch);
                break;
            }
        }

        sc.close();
    }
}
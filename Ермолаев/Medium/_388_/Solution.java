package Medium._388_;

class Solution {
    private int maxLen = 0;
    private int[] depthLevels;
    public int lengthLongestPath(String input) {
        String[] tokens = input.split("\n");
        depthLevels = new int[tokens.length + 1];

        for (String token : tokens) {
            int currentLevel = 1;
            while (token.startsWith("\t")) {
                token = token.substring(1);
                currentLevel++;
            }

            int newLength = depthLevels[currentLevel - 1] + token.length() + 1;
            if (token.contains("."))    maxLen = Math.max(maxLen, newLength);
            else                        depthLevels[currentLevel] = newLength;
        }
        return maxLen == 0 ? 0 : maxLen - 1;
    }


    public static void main(String[] args) {
        Solution sol = new Solution();
        String input = "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext";
        System.out.println(sol.lengthLongestPath(input));
    }
}

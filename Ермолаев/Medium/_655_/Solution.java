package Medium._655_;

import java.util.ArrayList;
import java.util.List;
import static java.lang.Math.max;
import static java.lang.Math.pow;

class Solution {
    private int height(TreeNode root, int level) {
        if (root == null)
            return level;
        return max(height(root.left, level + 1), height(root.right, level + 1));
    }
    private List<List<String>> init(int cols, int rows) {
        List<List<String>> result = new ArrayList<>(rows);
        for (int i = 0; i < rows; i++) {
            List<String> line = new ArrayList<>(cols);
            for (int j = 0; j < cols; j++)
                line.add("");
            result.add(line);
        }
        return result;
    }
    private void fill(List<List<String>> result, TreeNode root, int row, int col, int width) {
        if (root == null)
            return;
        result.get(row).set(col, Integer.toString(root.val));
        fill(result, root.left, row + 1, col - width / 2 - 1, width / 2);
        fill(result, root.right, row + 1, col + width / 2 + 1, width / 2);
    }

    public List<List<String>> printTree(TreeNode root) {
        int rows = height(root, 0);
        int cols = (int) pow(2, rows) - 1;

        List<List<String>> result = init(cols, rows);
        fill(result, root, 0, cols / 2, cols / 2);

        return result;
    }
}

package Medium._2476_;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

class Solution {
    private LinkedList<Integer> makeList(List<Integer> array, int query, int mid) {
        LinkedList<Integer> result = new LinkedList<>();

        if (array.get(mid) == query) {
            result.add(query);
            result.add(query);
        }
        else if (array.get(mid) > query) {
            result.add(mid == 0 ? -1 : array.get(mid - 1));
            result.add(array.get(mid));
        }
        else {
            result.add(array.get(mid));
            result.add(mid == array.size() - 1 ? -1 : array.get(mid + 1));
        }

        return result;
    }
    private LinkedList<Integer> find(List<Integer> array, int query) {
        if (array.size() == 0) {
            LinkedList<Integer> result = new LinkedList<>();
            result.add(-1);
            result.add(-1);
            return result;
        }

        int left = 0, right = array.size() - 1, mid = (left + right) / 2;
        while (left < right && array.get(mid) != query) {
            if (query < array.get(mid))     right = mid - 1;
            else                            left = mid + 1;
            mid = (left + right) / 2;
        }

        return makeList(array, query, mid);
    }

    private void toArray(TreeNode root, ArrayList<Integer> array) {
        if (root == null)   return;
        toArray(root.left, array);
        array.add(root.val);
        toArray(root.right, array);
    }

    public List<List<Integer>> closestNodes(TreeNode root, List<Integer> queries) {
        List<List<Integer>> result = new LinkedList<>();

        ArrayList<Integer> array = new ArrayList<>();
        toArray(root, array);

        for (int query : queries)
            result.add(find(array, query));

        return result;
    }
}

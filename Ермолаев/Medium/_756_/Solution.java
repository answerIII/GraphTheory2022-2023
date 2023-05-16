package Medium._756_;

import java.util.*;
class Solution {
    public boolean pyramidTransition(String bottom, List<String> allowed) {
        Map<String, Set<Character>> allowedMap = new HashMap<>();
        for (String triangle : allowed) {
            String base = triangle.substring(0, 2);
            char top = triangle.charAt(2);
            allowedMap.putIfAbsent(base, new HashSet<>());
            allowedMap.get(base).add(top);
        }
        return buildNextLevel(bottom, "", allowedMap, 1);
    }

    private boolean buildNextLevel(String currentRow, String nextRow,
                                   Map<String, Set<Character>> allowedMap, int position) {
        if (currentRow.length() == 1)
            return true;
        if (nextRow.length() + 1 == currentRow.length())
            return buildNextLevel(nextRow, "", allowedMap, 1);

        String base = currentRow.substring(position - 1, position + 1);
        if (allowedMap.containsKey(base)) {
            for (Character topSymbol : allowedMap.get(base)) {
                if (buildNextLevel(currentRow, nextRow + topSymbol, allowedMap, position + 1))
                    return true;
            }
        }
        return false;
    }
}

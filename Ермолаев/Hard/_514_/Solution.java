package Hard._514_;

import java.util.HashMap;
import java.util.Map;

public class Solution {
    Map<String, Map<Integer, Integer>> results = new HashMap<>();;
    public int findRotateSteps(String ring, String key) {
        return dfs(ring, key, 0);
    }
    private int positionClockwise(String ring, char symbol) {
        return ring.indexOf(symbol);
    }
    private int positionAntiClockwise(String ring, char symbol){
        if (ring.charAt(0) == symbol)
            return 0;
        return ring.lastIndexOf(symbol);
    }
    private String rotate(String ring, int position) {
        return ring.substring(position) + ring.substring(0, position);
    }
    private void record(String ring, int position, int result) {
        Map<Integer, Integer> answers = results.getOrDefault(ring, new HashMap<>());
        answers.put(position, result);
        results.put(ring, answers);
    }
    private int dfs(String ring, String key, int position){
        if (position == key.length())
            return 0;

        char symbol = key.charAt(position);
        if (results.containsKey(ring) && results.get(ring).containsKey(position))
            return results.get(ring).get(position);

        int forwardIdx = positionClockwise(ring, symbol);
        int backwardIdx = positionAntiClockwise(ring, symbol);
        forwardIdx = forwardIdx + dfs(rotate(ring, forwardIdx), key, position + 1) + 1;
        backwardIdx = ring.length() - backwardIdx + dfs(rotate(ring, backwardIdx), key, position + 1) + 1;

        int result = Math.min(forwardIdx, backwardIdx);
        record(ring, position, result);
        return result;
    }
}

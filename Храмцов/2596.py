class Solution(object):
    def checkValidGrid(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: bool
        """
        n = len(grid)
        possible_moves = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                          (2, 1), (2, -1), (-2, 1), (-2, -1)]
        current_position = (0, 0)

        if (grid[current_position[0]][current_position[1]]) != 0:
            return False

        def check(next_move):
            for move in possible_moves:
                possible_move = (current_position[0] + move[0],
                                 current_position[1] + move[1])
                if possible_move[0] >= n or possible_move[1] >= n or possible_move[0] < 0 or possible_move[1] < 0:
                    continue
                if (grid[possible_move[0]][possible_move[1]] == next_move):
                    return (True, possible_move)
            return (False, current_position)

        for i in range(n * n - 1):
            current_move = grid[current_position[0]][current_position[1]]
            next_move = current_move + 1
            (checked, current_position) = check(next_move)
            if not checked:
                return False
        return True

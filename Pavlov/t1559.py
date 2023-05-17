class Solution:
    def containsCycle(self, grid):
        num_rows = len(grid)
        num_cols = len(grid[0])
        visited = set()

        def is_valid_coordinate(row, col):
            return 0 <= row < num_rows and 0 <= col < num_cols

        def is_cycle_detected(row, col, prev):
            current_value = grid[row][col]
            queue = [(row, col, prev)]
            visited.add((row, col))

            while queue:
                current_row, current_col, prev_coordinate = queue.pop(0)

                for row_offset, col_offset in [[-1, 0], [1, 0], [0, 1], [0, -1]]:
                    new_row = current_row + row_offset
                    new_col = current_col + col_offset
                    if (
                        is_valid_coordinate(new_row, new_col)
                        and grid[new_row][new_col] == current_value
                        and (new_row, new_col) not in visited
                    ):
                        queue.append((new_row, new_col, (current_row, current_col)))
                        visited.add((new_row, new_col))
                    elif (
                        (new_row, new_col) in visited
                        and grid[new_row][new_col] == current_value
                        and prev_coordinate != (new_row, new_col)
                    ):
                        return True

        def process_grid():
            for row in range(num_rows):
                for col in range(num_cols):
                    if (row, col) not in visited:
                        if is_cycle_detected(row, col, -1):
                            return True
            return False

        return process_grid()

class Solution:
    def crackSafe(self, num_digits, num_symbols):
        initial_pattern = self.generate_initial_pattern(
            num_digits, num_symbols)
        visited_patterns = set()
        self.generate_all_patterns(
            initial_pattern, visited_patterns, num_digits, num_symbols
        )

        return "".join(initial_pattern)

    def generate_initial_pattern(self, num_digits, num_symbols):
        initial_pattern = [str(num_symbols - 1)] * (num_digits - 1)
        return initial_pattern

    def get_next_symbol(self, current_node, visited_patterns, num_symbols):
        for i in range(num_symbols):
            neighbor = "".join(current_node) + str(i)
            if neighbor not in visited_patterns:
                return i
        return num_symbols - 1

    def generate_all_patterns(self, pattern, visited_patterns, num_digits, num_symbols):
        total_num_patterns = num_symbols**num_digits
        while len(visited_patterns) < total_num_patterns:
            current_node = pattern[len(pattern) - num_digits + 1:]
            next_symbol = self.get_next_symbol(
                current_node, visited_patterns, num_symbols
            )
            visited_patterns.add("".join(current_node) + str(next_symbol))
            pattern.append(str(next_symbol))

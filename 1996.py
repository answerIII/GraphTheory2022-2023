class Solution:
    def numberOfWeakCharacters(self, properties: List[List[int]]) -> int:
        properties.sort(key=lambda x: (-x[0], x[1]))
            
        max_defense = 0
        count_of_weak = 0

        for item in properties:
            if item[1] < max_defense:
                count_of_weak += 1
            else:
                max_defense = item[1]
                
        return count_of_weak

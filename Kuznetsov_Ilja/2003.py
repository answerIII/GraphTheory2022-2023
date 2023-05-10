from typing import List

class Solution:
    def smallestMissingValueSubtree(self, parents: List[int], nums: List[int]) -> List[int]:
        missing_values = [1] * len(parents)
        if 1 not in nums:
            return missing_values
        
        attached_to = {}
        path_to_one = []
        parent = nums.index(1)
        
        while parent != -1:
            attached_to[nums[parent]] = len(path_to_one)
            path_to_one.append(parent)
            parent = parents[parent]
        
        
        for node_idx in range(len(parents)):
            parent = node_idx
            path_to_node = []
            
            while nums[parent] not in attached_to:
                path_to_node.append(parent)
                parent = parents[parent]
            attachment = attached_to[nums[parent]]
            
            for path_node_idx in path_to_node:
                attached_to[nums[path_node_idx]] = attachment
        
        step = 0
        for gen_val in range(1, len(parents) + 2):
            attachment = attached_to.get(gen_val, len(path_to_one))
            if attachment > step:
                for path_step in path_to_one[step : attachment]:
                    missing_values[path_step] = gen_val
                step = attachment
                
                if attachment == len(path_to_one):
                    break
        
        return missing_values

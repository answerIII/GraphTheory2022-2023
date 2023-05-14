class Solution:

    def lengthLongestPath(self, input: str) -> int: 
    
        def is_file(name : str) -> bool:
            lst = name.split('.')
            if len(lst) < 2:
                return False
            for i in lst:
                if i.replace(" ", "").isalnum() == False:
                    return False
            return True

        def search_files( paths: dict[int, int], list_number: int, system : list[str], files: dict[str, int] ) -> None:
            item = system[list_number].replace('\t', '')
            current_height = system[list_number].count("\t")

            if is_file(item):
                if current_height == 0:
                    files[item] = len(item)
                else:    
                    files[item] = paths[current_height - 1] + len(item) + 1
            elif current_height == 0:
                paths[current_height] = len(item)
            else:
                paths[current_height] = paths[current_height - 1] + len(item) + 1
            
            if list_number != len(system) - 1:
                search_files(paths, list_number + 1, system, files)


        files = dict()
        files_system = input.split('\n')
        paths = dict()

        search_files(paths, 0, files_system, files)
        if len(files) == 0:
            return 0
        max_val = max(files.values())

        return max_val

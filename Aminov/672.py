class Solution:
    def flipLights(self, n: int, presses: int) -> int:
        if presses == 0:
            return 1

        match n:
            case 1:
                return 2
            case 2:
                return [4, 3][presses == 1]
            case _:
                match presses:
                    case 1:
                        return 4
                    case 2:
                        return 7
                    case _:
                        return 8

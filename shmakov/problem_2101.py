import math
class Solution(object):
    
    def maximumDetonation(self, bombs):
        # фукнция взрыва бомбы, с учетом цепной реакции
        def detonate(target, bombs, counter = 1):
            detonated = []
            for bomb in bombs:
                # Если бомба из остаточного списка в зоне поражения целевой бомбы
                if math.sqrt(abs(target[0] - bomb[0])**2 + abs(target[1] - bomb[1])**2) <= target[2]:
                    # добавляем в список сдетонированных бомб
                    detonated.append(bomb)
            if detonated:
                counter += len(detonated) # количество задетых бомб учитываем

                for bomb in detonated:
                    bombs.remove(bomb) # задетые бомбы больше не взрываем

                for bomb in detonated:
                    counter = detonate(bomb, bombs, counter) # продолжаем цепную реакцию
            return counter
        
        origin = bombs[:]
        detonations = [] # найдем количество взорванных бомб, для каждой бомбы, если выбирать ту для старта
        for bomb in origin:
            bombs.remove(bomb)
            detonations.append(detonate(bomb, bombs))
            bombs = origin[:]
        return max(detonations)

class Solution(object):
    def watchedVideosByFriends(self, watchedVideos, friends, id, level):
        """
        :type watchedVideos: List[List[str]]
        :type friends: List[List[int]]
        :type id: int
        :type level: int
        :rtype: List[str]
        """

        freq_v = {} # словарь частот
        visited = set([id]) # множество посещенных неповторяющихся пользователей
        r_level = level # текущий уровень
        running_list = deque([id]) # активный список
        while r_level > 0:
            r_level -= 1
            # на момент захода в цикл, текущий уровень больше нуля
            # значит running_list - список пользователей для дальнейшего спуска
            # в ином случае это список друзей, чьи фильмы будем анализировать
            for _ in range(len(running_list)):
                target = running_list.popleft() # текущая цель для спуска
                for friend in friends[target]: # просмотр друзей цели
                    if not friend in visited:
                        running_list.append(friend) # если друг не был посещен, добавляем его в running_list
                        visited.add(friend)
                    # и так до того момента, как мы окажемся на 0 уровне
                    # в этот момент в running_list будут находится друзья, находящиеся на заданном уровне от изначального пользователя
        # Далее подсчитываем частоту фильмов
        for friend in running_list:
            for video in watchedVideos[friend]:
                if not video in freq_v:
                    freq_v[video] = 1
                else: 
                    freq_v[video] += 1
                    
        return sorted(list(freq_v.keys()), key = lambda k: (freq_v[k], k))

class Solution:
    def watchedVideosByFriends(self, watchedVideos: List[List[str]], friends: List[List[int]], id: int, level: int) -> List[str]:
        
        def find_level_friends_BFS(id,level,friends):
            friends = [set(friends_list) for friends_list in friends] # для удобства операций с множествами
            last_level_friends = friends[id] # друзья на пред уровне
            prev_friends = {id} # все друзья на пред уровнях
            for _ in range(1, level):

                prev_friends.update(last_level_friends)
                next_level_friends = set()

                for friend in last_level_friends:
                    next_level_friends.update(friends[friend]) # собираем друзей для уровня

                last_level_friends = next_level_friends - prev_friends # убираем друзей с более ранних уровней
            return last_level_friends
        
        level_friends = find_level_friends_BFS(id,level,friends)
        videos = {}
        for friend in level_friends:
            for video in watchedVideos[friend]:
                if video in list(videos.keys()):
                    videos[video] += 1
                else:
                    videos[video] = 1
       
      
        return [name for _, name in sorted((freq, name) for name, freq in videos.items())]

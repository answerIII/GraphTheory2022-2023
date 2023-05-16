func findAllPeople(n int, meetings [][]int, firstPerson int) []int {
    infected := make([]int, n)
    answer := make([]int, 0)
    sort.Slice(meetings, func(i, j int) bool {
        return meetings[i][2] < meetings[j][2]
    })

    for i:=0; i<n; i++ {
        MakeSet(i, infected)
    }
    startTime := meetings[0][2]
    stroka:= 0
    infected[0] = 0
    infected[firstPerson] = 0

    for i:=1; i<len(meetings); i++ {
        meet := make([]int, 0)

        
        if i == len(meetings)-1 {
            for j:=stroka; j<i+1; j++ {
                meet = append(meet, meetings[j][0])
                meet = append(meet, meetings[j][1])
                Unite(meetings[j][0], meetings[j][1], infected)
            }
        }

        if meetings[i][2] != startTime {
            for j:=stroka; j<i; j++ {
                meet = append(meet, meetings[j][0])
                meet = append(meet, meetings[j][1])
                Unite(meetings[j][0], meetings[j][1], infected)
            }
            startTime = meetings[i][2]
            stroka = i
        } 
        
        for _, j := range meet {
			if Find(0, infected) != Find(j, infected) {
				infected[j] = j
			}
		}
    }

    if len(meetings) == 1 {
        meet := make([]int, 0)
            meet = append(meet, meetings[0][0])
            meet = append(meet, meetings[0][1])
            Unite(meetings[0][0], meetings[0][1], infected)

            for _, j := range meet {
			if Find(0, infected) != Find(j, infected) {
				infected[j] = j
			}
		}
    }

    for i := range infected {
            if Find(0, infected) == Find(i, infected) {
            answer = append(answer, i)
        }
    }
   
    return answer
}

func MakeSet(x int, p []int) {
    p[x] = x
}

func Find(x int, p []int) int { //поиск корня и замена значений множества на значение корня 
    if p[x] != x {
        p[x] = Find(p[x], p)
	}
    return p[x]
}

func Unite(x int, y int, p []int) { // объединение 2 множеств при различных корнях
    x = Find(x, p)
    y = Find(y, p)
    if x != y {
        p[x] = y
    }
}

//https://habr.com/ru/articles/104772/
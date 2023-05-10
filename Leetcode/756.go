func DFS(m map[string][]string, iteration int, row string, next_row string) bool {
    //Если мы достигли вершины, то значит пирамида построена
	if len(row) == 1 {
		return true
	}
    //Если мы смогли заполнить ряд сверху
	if len(row) == len(next_row)+1 {
		return DFS(m, 0, next_row, "")
	}
    //Если мы всё же дошли до конца строки, но не смогли заполнить ряд сверху
	if iteration == len(row)-1 {
		return false
	}
    //Пробегаемся циклом по возможным буквам, добавляемых на следующий ряд
    list := m[row[iteration:iteration+1]+row[iteration+1:iteration+2]]
	for i := range list {
		if DFS(m, iteration+1, row, next_row+list[i]) {
			return true
		}
	}
	return false
}

func pyramidTransition(bottom string, allowed []string) bool {
    //Введём словари для ускорения работы алгоритма, в котором ключи - две первые буквы из i элемента массива allowed, а значение - последняя
    m := map[string][]string{}
	for i := range allowed {
		next := allowed[i]
		m[next[:2]] = append(m[next[:2]], next[2:])
	}
    //Решаем DFS методом, увеличивая значение iteration
    return DFS(m, 0, bottom, "")
}
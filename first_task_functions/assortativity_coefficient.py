# Функция для вычисления коэффициента ассортативности
def calculate_assortativity_coefficient(data, AllVertex, countVertex):
    multiply_m = 0
    summary_m = 0
    square_summary_m = 0
    cube_summary_m = 0
    visited_pairs = set()
    
    for index, row in data.iterrows():
        pair = (row['in'], row['out'])
        if pair in visited_pairs or pair[::-1] in visited_pairs:
            continue
        j = len(AllVertex.get(row['in'], []))
        k = len(AllVertex.get(row['out'], []))
        multiply_m += j * k
        summary_m += j + k
        square_summary_m += j * j + k * k
        visited_pairs.add(pair)
    
    M = len(visited_pairs)
    M_reverse = 1 / M
    r = (multiply_m - M_reverse * ((0.5 * summary_m) ** 2)) / (0.5 * square_summary_m - M_reverse * ((0.5 * summary_m) ** 2))
    
    return r
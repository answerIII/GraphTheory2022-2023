def table_str(heading, values, table_len) -> str:
    col_number = len(heading)
    col_len = int((table_len - (col_number - 1) * 3) / col_number)

    format_str = ''
    for _ in range(col_number - 1):
        format_str += f'%{col_len}s | '
    format_str += f'%{col_len}s\n'

    table = '_' * table_len + '\n'
    table += format_str % __to_str_tuple(heading, col_len)
    table += format_str % __to_str_tuple(values, col_len)
    table += '_' * table_len + '\n'
    return table

def __to_str_tuple(values : tuple, col_len : int = 20) -> tuple:
    formated = []

    for value in values:
        value_str = str(value)
        if (len(value_str) > col_len):
            value_str = value_str[0:col_len]
        formated.append(value_str)

    print(formated)

    return tuple(formated)
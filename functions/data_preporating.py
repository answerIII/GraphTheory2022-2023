import pandas as pd
import math

#Обработка файла с графом и сохранение в нужном нам виде
def prep(file):
    if file[-4:] == "prep":
        return file
    else:
        file_path = 'datasets/' + file + '.csv'
        data = pd.read_csv(file_path, delim_whitespace=True, header=None, names=['in', 'out', 'weight', 'time'])
        df = {'in': [], 'out': [], 'weight': [], 'time': []}
        
        for index, row in data.iterrows():
            df['in'].append(row['in'])
            df['out'].append(row['out'])
            df['weight'].append(row['weight'])
            df['time'].append(row['time'])

        new_data = pd.DataFrame(df, columns=['in', 'out', 'weight', 'time'])
        new_name = 'datasets/' + file + '_' + '0' + 'prep.csv'
        new_data.to_csv(new_name, sep='\t', header=True, index=False)
        return file + '_' + '0' + 'prep'



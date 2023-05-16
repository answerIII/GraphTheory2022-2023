import pandas as pd
import math
def prep(file):
    if file[-4:] == "prep":
        return file
    else:
        file_path = 'datasets/' + file + '.tsv'
        dvudol = ""
        while True:
            print('Если граф двудольный - введите 1, иначе - 0: ')
            dvudol = input()
            if dvudol == '1' or dvudol == '0':
                break
        data = pd.read_csv(file_path, sep="[ ]{1,}", header=None, names=['in', 'out', 'weight', 'time'])
        #if math.isnan(data.iloc[1]['out']):
        #    data = pd.read_csv(file_path, sep=" ", header=None, names=['in', 'out', 'weight', 'time'])
        df = {'in': [], 'out': [], 'weight': [], 'time': []}
        if dvudol == '1':
            for index, row in data.iterrows():
                df['in'].append(row['in'])
                df['out'].append(row['out']*(-1))
                df['weight'].append(row['weight'])
                df['time'].append(row['time'])
        else:
            for index, row in data.iterrows():
                df['in'].append(row['in'])
                df['out'].append(row['out'])
                df['weight'].append(row['weight'])
                df['time'].append(row['time'])
        new_data = pd.DataFrame(df, columns=['in', 'out', 'weight', 'time'])
        new_name = 'datasets/' + file + '_' + dvudol + 'prep.csv'
        new_data.to_csv(new_name, sep='\t', header=True, index=False)
        return file + '_' + dvudol + 'prep'



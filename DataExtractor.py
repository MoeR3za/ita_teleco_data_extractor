import pandas as pd
import os
from sys import argv
from tqdm.auto import tqdm

COL_NAMES = ['sqr_id', 'interval', 'country_code', 'rec_sms', 'sent_sms', 'inc_call', 'out_call', 'internet']

def save_extract(extract: pd.DataFrame, sqr_id:int):
    if len(extract.columns) == 1:
        extract_name = f'{extract.columns[0]}_extract_sqr_id_{sqr_id}'
    else:
        extract_name = f'multi_extract_sqr_id_{sqr_id}'

    while True:
        if os.path.isfile(extract_name+'.csv'):
            extract_name = extract_name+'(new)'
        else:
            break
    extract_name = extract_name+'.csv'

    print(f'Saving file as: {extract_name}')
    extract.to_csv(extract_name)

def extract_traffic(sqr_id, columns):
    columns = set([c for c in COL_NAMES]) if columns == 'all' else set([c for c in columns])
    columns.add('interval')
    columns = list(columns)

    files = []
    print('Locating dataset files..')
    for f in tqdm(os.listdir(os.curdir)):
        if f.startswith('sms-call-internet-mi-') and (f.endswith('.txt') or f.endswith('.csv')):
            files.append(f)

    print('Extracting data..')
    extract = pd.DataFrame()
    for f in tqdm(files):
        df = pd.read_csv(f, sep='\t', names=COL_NAMES)

        sqr_filtered = df[(df.sqr_id == sqr_id)]
        sqr_filtered = sqr_filtered.filter(columns)
        sqr_filtered['interval'] = pd.to_datetime(sqr_filtered.interval, unit='ms')

        data = (sqr_filtered.groupby(['interval'])).sum()
        extract = pd.concat([extract, data])

    extract = extract.drop_duplicates()
    
    return extract




if __name__ == '__main__':
    script = __file__.split(os.path.sep)[-1]

    if len(argv) < 2 or 'help' in argv:
        print(f"""Usage:
    python {script} square_id column (default: internet)
    python {script} square_id all (all columns)""")
    
    else:
        sqr_id = int(argv[1])
        columns = ['internet']
        if len(argv) > 2:
            columns = 'all' if argv[2] == 'all' else argv[2:]
            if columns != 'all':
                for c in columns:
                    if c not in COL_NAMES:
                        print(f'Incorrect column name: {c}\nAvailable columns: {", ".join(COL_NAMES)}')
                        exit()
        
        extract = extract_traffic(sqr_id, columns)
        save_extract(extract, sqr_id)
        print('Done..!')

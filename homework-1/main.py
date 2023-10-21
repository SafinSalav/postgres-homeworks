import psycopg2
from csv import DictReader

conn = psycopg2.connect(host='localhost', database='north', user='postgres', password='12346')
paths = {'customers': 3, 'employees': 6, 'orders': 5}

with conn:
    for path, columns in paths.items():
        values_list = []
        with open(f'north_data/{path}_data.csv', encoding='utf-8', newline='') as csvfile:
            reader = DictReader(csvfile)
            for dic in reader:
                values_ = []
                for i in dic.values():
                    values_.append(i)
                values_list.append(tuple(values_))
        with conn.cursor() as cur:
            cur.executemany(f'INSERT INTO {path} VALUES (%s{", %s" * (columns - 1)})', values_list)
            conn.commit()
conn.close()

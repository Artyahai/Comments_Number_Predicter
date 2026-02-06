import psycopg2
conn = psycopg2.connect(host='localhost', port=5432, database='dataset', user='postgres', password='postgres')
cur = conn.cursor()

conn.close()
cur.close()
import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Loads data from S3 bucket to the two staging tables (logs_staging_tables, songs_statging_tables)
    """
    try:
        for query in copy_table_queries:
            cur.execute(query)
            conn.commit()
        
        print('Staging tables loaded from S3 bucket successfully :)')
    
    except psycopg2.Error as e:
        print(e)

def insert_tables(cur, conn):
    """
    Loads data from the two staging tables to the database tables
    """
    try:
        for query in insert_table_queries:
            cur.execute(query)
            conn.commit()
        
        print('Data loaded from staging tables into Database tables successfully :)')

    except psycopg2.Error as e:
        print(e)


def main():
    """
    Loads data from S3 bucket to staging tables,
    and then loads data from staging tables to Database tables.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    try:
        conn = psycopg2.connect("""host={} 
                                   dbname={} 
                                   user={} 
                                   password={} 
                                   port={}""".format(*config['CLUSTER'].values()))

        print('Connected to Database successfully :)')

    except psycopg2.Error as e:
        print(e)
    
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
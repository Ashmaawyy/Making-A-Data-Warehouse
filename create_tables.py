import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops tables if they exist
    """
    try:
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()

        print('Dropped tables successfully :)')

    except psycopg2.Error as e:
        print(e)


def create_tables(cur, conn):
    """
    Creates tables if they don't exist
    """
    try:
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()
        
        print('Created tables scuccessfuly :)')
    
    except psycopg2.Error as e:
        print(e)


def main():
    """
    Drops existing tables and then creates new tables
    """
    try:
        config = configparser.ConfigParser()
        config.read('dwh.cfg')

        conn = psycopg2.connect("""host={} 
                                   dbname={} 
                                   user={} 
                                   password={} 
                                   port={}""".format(*config['CLUSTER'].values()))
        
        print('Connected to Database successfully :)')
        cur = conn.cursor()
        drop_tables(cur, conn)
        create_tables(cur, conn)

        conn.close()
        print('Dropped existing Database tables and re-created them successfully :)')

    except psycopg2.Error as e:
        print(e)


if __name__ == "__main__":
    main()
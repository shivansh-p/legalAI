import psycopg2
from config import config_psql

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config_psql()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error


if __name__ == '__main__':
    connect()


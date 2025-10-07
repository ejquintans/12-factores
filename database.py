import psycopg2
def get_db_connection(db_url: str):
    return psycopg2.connect(db_url)
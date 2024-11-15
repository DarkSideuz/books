import psycopg2

def connect_to_database():
    try:
        connection = psycopg2.connect(database='books', user='postgres', password='25082009', host='localhost')
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database:", error)

def create_books_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        publication_year INTEGER NOT NULL
    );
    """)
    connection.commit()
    connection.close()
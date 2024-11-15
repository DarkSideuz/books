import psycopg2

def connect_to_database():
    try:
        connection = psycopg2.connect(
            database='books',
            user='postgres',
            password='25082009',
            host='localhost'
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database:", error)
        return None

def create_books_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            pages INT NOT NULL,
            price INT NOT NULL
        );
        """)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error creating table:", error)
    finally:
        cursor.close()

def insert_book(connection, book_name, book_description, book_pages, book_price):
    try:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO books (name, description, pages, price)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """, (book_name, book_description, book_pages, book_price))
        book_id = cursor.fetchone()[0]
        connection.commit()
        return book_id
    except (Exception, psycopg2.Error) as error:
        print("Error inserting book:", error)
        return None
    finally:
        cursor.close()

def insert_multiple_books(connection, books):
    book_ids = []
    for book in books:
        book_id = insert_book(connection, *book)
        if book_id:
            book_ids.append(book_id)
    return book_ids

if __name__ == "__main__":
    conn = connect_to_database()
    if conn:
        create_books_table(conn)
        books_to_add = [
            ("Book One", "A fascinating first book", 300, 25),
            ("Book Two", "The sequel everyone loves", 250, 20),
            ("Book Three", "An epic conclusion", 400, 30)
        ]
        inserted_ids = insert_multiple_books(conn, books_to_add)
        print(f"Inserted book IDs: {inserted_ids}")
        conn.close()

from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database
    create_tables()

    # Get user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the author is already in the database
    cursor.execute('SELECT id FROM authors WHERE name = ?', (author_name,))
    author_information = cursor.fetchone()

    if author_information:
        author_id = author_information[0]
    else:
        # Insert the author into the database
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
        author_id = cursor.lastrowid

    # Check if the magazine is already in the database
    cursor.execute('SELECT id FROM magazines WHERE name = ?', (magazine_name,))
    magazine_info = cursor.fetchone()

    if magazine_info:
        magazine_id = magazine_info[0]
    else:
        # Insert the magazine into the database
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (magazine_name, magazine_category))
        magazine_id = cursor.lastrowid

    # Insert the article into the database
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                   (article_title, article_content, author_id, magazine_id))
    conn.commit()
    conn.close()

    # Call the show_latest function
    show_latest()

def show_latest():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the latest author from db
    cursor.execute('SELECT * FROM authors ORDER BY id DESC LIMIT 1')
    author = cursor.fetchone()

    # Fetch the latest article from db
    cursor.execute('SELECT * FROM articles ORDER BY id DESC LIMIT 1')
    article = cursor.fetchone()

    # Fetch the latest magazine from db
    cursor.execute('SELECT * FROM magazines ORDER BY id DESC LIMIT 1')
    magazine = cursor.fetchone()

    conn.close()

    print("\nLatest Magazine:")
    if magazine:
        print(Magazine(magazine["id"], magazine["name"], magazine["category"]))

    print("\nLatest Author:")
    if author:
        print(Author(author["id"], author["name"]))

    print("\nLatest Article:")
    if article:
        print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))

if __name__ == "__main__":
    main()

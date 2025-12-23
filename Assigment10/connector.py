import mysql.connector

host = "localhost"
user = "root"
password = "Alate@99"   
database = "test_db"

try:
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    print("Connected to MySQL database!")

    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Tables in database:", tables)

    cursor.execute("SELECT * FROM employees LIMIT 5")
    rows = cursor.fetchall()

    print("\nEmployee records:")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()
    print("\nConnection closed.")

except mysql.connector.Error as err:
    print("Error:", err)

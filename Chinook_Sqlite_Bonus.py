import sqlite3
import pandas as pd
import os


def get_top_n_invoices(db_path, n, a, b):
    """
    Hàm trả về TOP N danh sách các Invoice có tổng trị giá từ a đến b, sắp xếp giảm dần theo Total.
    """
    if not os.path.exists(db_path):
        print(f'Lỗi: File database "{db_path}" không tồn tại! Kiểm tra đường dẫn nhé.')
        return None

    sqliteConnection = None
    df = None
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        print('DB Init thành công!')
        query = """
        SELECT * FROM Invoice 
        WHERE Total BETWEEN ? AND ? 
        ORDER BY Total DESC 
        LIMIT ?
        """
        cursor.execute(query, (a, b, n))
        results = cursor.fetchall()
        # Lấy tên columns từ cursor để tự động
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        print(df)
        cursor.close()
    except sqlite3.Error as error:
        print('Error occurred -', error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')
    return df


def get_top_n_customers_by_invoice_count(db_path, n):
    """
    Hàm lọc ra TOP N khách hàng có nhiều Invoice nhất.
    """
    if not os.path.exists(db_path):
        print(f'Lỗi: File database "{db_path}" không tồn tại! Kiểm tra đường dẫn nhé.')
        return None

    sqliteConnection = None
    df = None
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        print('DB Init thành công!')
        query = """
        SELECT 
            c.CustomerId, 
            c.FirstName, 
            c.LastName, 
            COUNT(i.InvoiceId) as InvoiceCount
        FROM Customer c
        LEFT JOIN Invoice i ON c.CustomerId = i.CustomerId
        GROUP BY c.CustomerId
        ORDER BY InvoiceCount DESC
        LIMIT ?
        """
        cursor.execute(query, (n,))
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        print(df)
        cursor.close()
    except sqlite3.Error as error:
        print('Error occurred -', error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')
    return df


def get_top_n_customers_by_total_value(db_path, n):
    """
    Hàm lọc ra TOP N khách hàng có tổng giá trị Invoice cao nhất.
    """
    if not os.path.exists(db_path):
        print(f'Lỗi: File database "{db_path}" không tồn tại! Kiểm tra đường dẫn nhé.')
        return None

    sqliteConnection = None
    df = None
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        print('DB Init thành công!')
        query = """
        SELECT 
            c.CustomerId, 
            c.FirstName, 
            c.LastName, 
            SUM(i.Total) as TotalSpent
        FROM Customer c
        LEFT JOIN Invoice i ON c.CustomerId = i.CustomerId
        GROUP BY c.CustomerId
        ORDER BY TotalSpent DESC
        LIMIT ?
        """
        cursor.execute(query, (n,))
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        print(df)
        cursor.close()
    except sqlite3.Error as error:
        print('Error occurred -', error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')
    return df

db_path = 'databases/Chinook_Sqlite.sqlite'
get_top_n_invoices(db_path, 5, 1.0, 10.0)
get_top_n_customers_by_invoice_count(db_path, 5)
get_top_n_customers_by_total_value(db_path, 5)
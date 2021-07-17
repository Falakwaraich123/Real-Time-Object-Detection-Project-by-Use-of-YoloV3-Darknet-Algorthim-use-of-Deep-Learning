import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def makeTables(database):

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        email text,
                                        pass text
                                    ); """

    sql_create_logs_table = """CREATE TABLE IF NOT EXISTS logs (
                                    id integer PRIMARY KEY,
                                    file_name text,
                                    label text,
                                    confidance text,
                                    fps text,
                                    timestamp text
                                );"""
    
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_users_table)

        # create tasks table
        create_table(conn, sql_create_logs_table)
        #close the connection
        conn.close()
    else:
        print("Error! cannot create the database connection.")
        #close the connection
        conn.close()


def writeUsers_Table(database, user_info):
    # create a database connection
    conn = create_connection(database)
        # create tables
    if conn is not None:
        c = conn.cursor()
        sql = '''INSERT INTO users(email,pass) VALUES(?,?);''' 
        c.execute(sql, user_info)
        #commit the changes to db			
        conn.commit()
        #close the connection
        conn.close()
        print("Success! data added to the database")
    else:
        print("Error! cannot create the database connection.")

def writeLogs_Table(database, log_info):
    # create a database connection
    conn = create_connection(database)
        # create tables
    if conn is not None:
        c = conn.cursor()
        sql = '''INSERT INTO logs(file_name,label,confidance,fps,timestamp) VALUES(?,?,?,?,?);'''   
        c.execute(sql, log_info)
        #commit the changes to db			
        conn.commit()
        #close the connection
        conn.close()
        print("Success! data added to the database")
    else:
        print("Error! cannot create the database connection.")


def userExists(database, user_info):
    # create a database connection
    conn = create_connection(database)
        # create tables
    if conn is not None:
        c = conn.cursor()
        sql = '''SELECT email,pass FROM users WHERE email=? AND pass=?;'''
        c.execute(sql,user_info)
        rows = c.fetchone()
        if rows:
            return True
        else:
            return False
    else:
        print("Error! cannot create the database connection.")
        return False

def get_logs_data(database):
    # create a database connection
    logsList = []
    conn = create_connection(database)
        # create tables
    if conn is not None:
        c = conn.cursor()
        sql = '''SELECT * FROM logs;'''
        c.execute(sql)
        rows = c.fetchall()
        for log in rows:
            tempDict = {"Image":log[1], "Label":log[2], "Confidance":log[3], "FPS":log[4], "Time":log[5]}
            logsList.append(tempDict)
        return logsList
    else:
        print("Error! cannot create the database connection.")
        return []
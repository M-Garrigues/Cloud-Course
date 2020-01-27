import mysql
from datetime import datetime

def date_to_string(date):
    return datetime.strftime(date,'%d/%m/%Y')

def string_to_mysql(string):
    date = datetime.strptime(string, '%d/%m/%Y')
    return datetime.strftime(date,'%Y-%m-%d %H:%M:%S')

class Persistence:

    def __init__(self, cnx):
        self.cnx = cnx
        self.page_size = 100

    def get_offset(self, page):
        return str(page * self.page_size)

    def fetch_users_from_query(self, query):
        cursor = self.cnx.cursor()
        cursor.execute(query)
        users = []
        for (id, firstName, lastName, birthday) in cursor:
            u = {"id": id,
                 "firstName": firstName,
                 "lastName": lastName,
                 "birthDay": date_to_string(birthday)}
            users.append(u)
        return users

    def get_users(self, page):
        query = "SELECT * FROM Users ORDER BY ID LIMIT "+self.get_offset(page)+","+str(self.page_size)+";"
        return self.fetch_users_from_query(query)

    def get_users_age_greater(self, age_limit, page):
        query = "SELECT * FROM Users WHERE ORDER BY ID LIMIT "+self.get_offset(page)+"," + str(self.page_size) + ";"
        return self.fetch_users_from_query(query)

    def get_users_age_equal(self, age, page):
        query = "SELECT * FROM Users WHERE ORDER BY ID LIMIT "+self.get_offset(page)+"," + str(self.page_size) + ";"
        return self.fetch_users_from_query(query)

    def delete_users(self):
        cursor = self.cnx.cursor()
        query = "DELETE FROM Users" # TODO : TRUNCATE MAY BE FASTER
        cursor.execute(query)
        self.cnx.commit()
        cursor.execute(query)
        return True

    def put_users(self, users):
        self.delete_users()
        try:
            query = """INSERT INTO Users (id, firstName, lastName, birthDay) 
                                      VALUES (%s, %s, %s, STR_TO_DATE(%s,'%d/%m/%Y')) """
            cursor = self.cnx.cursor()
            cursor.executemany(query, users)
            self.cnx.commit()
            if cursor.rowcount == len(users):
                return True
            else:
                return False

        except mysql.connector.Error as error:
            print("Failed to insert record into table {}".format(error))
            return False

    def get_user(self, id):
        query = "SELECT * FROM Users WHERE id = %s"
        cursor = self.cnx.cursor()
        cursor.execute(query, (id,))
        users = []
        for (id, firstName, lastName, birthday) in cursor:
            u = {"id": id,
                 "firstName": firstName,
                 "lastName": lastName,
                 "birthDay": birthday}
            users.append(u)
        return users

    def post_user(self, user):
        query = """INSERT INTO Users (id, firstName, lastName, birthDay) 
                                              VALUES (%s, %s, %s, STR_TO_DATE(%s,'%d/%m/%Y')) """
        cursor = self.cnx.cursor()
        user_tuple = (user['id'], user['firstName'], user['lastName'], user['birthDay'])
        cursor.execute(query, user_tuple)
        self.cnx.commit()
        if cursor.rowcount == 1:
            return True
        else:
            return False

    def put_user(self,user):
        try:
            cursor = self.cnx.cursor()
            query = """Update Laptop set Name = %s, Price = %s where id = %s"""
            user_tuple = (user['id'], user['firstName'], user['lastName'], user['birthDay'])
            cursor.execute(query, user_tuple)
            self.cnx.commit()
            return True
        except mysql.connector.Error as error:
            print("Failed to update record to database: {}".format(error))
            return False

    def delete_user(self, id):
        query = "DELETE FROM Users WHERE id = %s"
        cursor = self.cnx.cursor()
        cursor.execute(query, (id,))
        self.cnx.commit()
        cursor.execute(query)
        records = cursor.fetchall()
        if len(records) == 0:
            return True
        return False
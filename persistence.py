import mysql


class Persistence:

    def __init__(self, cnx):
        self.cnx = cnx

    def get_users(self):
        query = "SELECT * FROM Users"
        cursor = self.cnx.cursor()
        cursor.execute(query)
        users = []
        for (id, firstName, lastName, birthday) in cursor:
            u = {"id": id,
                 "firstName": firstName,
                 "lastName": lastName,
                 "birthDay": birthday}
            users.append(u)
        return users

    def delete_users(self):
        cursor = self.cnx.cursor()
        query = "DELETE FROM Users" # TODO : TRUNCATE MAY BE FASTER
        cursor.execute(query)
        self.cnx.commit()
        cursor.execute(query)
        records = cursor.fetchall()
        if len(records) == 0:
            return True
        return False

    def put_users(self, users):
        self.delete_user()
        try:
            query = """INSERT INTO Users (id, firstName, lastName, birthDay) 
                                      VALUES (%s, %s, %s, %s) """
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
                                              VALUES (%s, %s, %s, %s) """
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

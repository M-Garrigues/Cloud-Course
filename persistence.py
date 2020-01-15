import mysql


class Persistence:

    def __init__(self, cnx):
        self.cnx = cnx

    def get_users(self):
        query = "SELECT * FROM Users"
        cursor = self.cnx.cursor()
        cursor.execute(query)
        users = []
        for (id, firstname, lastname, birthday) in cursor:
            u = {"id" : id,
                 "firstName" : firstname,
                 "lastName" : lastname,
                 "birthDay" : birthday}
            users.append(u)
        return users

    def delete_user(self):
        return

    def put_user(self):
        return




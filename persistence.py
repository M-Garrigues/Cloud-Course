import mysql


class Persistence:

    def __init__(self, cnx):
        self.cnx = cnx
        self.page_size = 100

    def get_users(self, page):

        offset = page * self.page_size
        query = "SELECT * FROM Users ORDER BY ID LIMIT "+ str(offset)+ ","+str(self.page_size)+";"
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

    def delete_user(self):
        return

    def put_user(self):
        return




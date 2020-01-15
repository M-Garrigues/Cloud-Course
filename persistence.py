import mysql


class Persistence:

    def __init__(self, cnx):
        self.cnx = cnx

    def get_user(self):
        query = "SELECT * FROM users"
        return self.cnx.cursor().execute(query)

    def delete_user(self):
        return

    def put_user(self):
        return




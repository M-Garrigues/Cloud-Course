import mysql
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random as rd


def date_to_string(date):
    return datetime.strftime(date, '%m/%d/%Y')

def date_to_mysql_string(date):
    return datetime.strftime(date, '%Y-%m-%d')

def string_to_mysql(string):
    date = datetime.strptime(string, '%m/%d/%Y')
    return datetime.strftime(date, '%Y-%m-%d %H:%M:%S')


class Persistence:

    def __init__(self, cnx):
        self.cnx = cnx
        self.page_size = 100

    def get_offset(self, page):
        return str(page * self.page_size)

    def fetch_users_from_query(self, query):
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query)
        users = []
        for (id, firstName, lastName, birthday, lat, lon) in cursor:
            u = {"id": id,
                 "firstName": firstName,
                 "lastName": lastName,
                 "birthDay": birthday,
                 "position": {"lat": float(lat), "lon": float(lon)}}
            users.append(u)
        return users

    def get_users(self, page):
        query = "SELECT id, firstName, lastName, DATE_FORMAT(birthDay,'%m/%d/%Y'), lat, lon FROM Users ORDER BY ID LIMIT "+self.get_offset(page)+","+str(self.page_size)+";"
        return self.fetch_users_from_query(query)

    def get_users_age_greater(self, age_limit, page):
        date_limit = datetime.now() - relativedelta(years=age_limit)
        query = "SELECT id, firstName, lastName, DATE_FORMAT(birthDay,'%m/%d/%Y'), lat, lon FROM Users WHERE date(birthDay) < date '"+date_to_mysql_string(date_limit)+"' ORDER BY ID LIMIT "+self.get_offset(page)+"," + str(self.page_size) + ";"
        print(query)
        return self.fetch_users_from_query(query)

    def get_users_age_equal(self, age, page):
        min_date = datetime.now() - relativedelta(years=age+1)
        max_date = datetime.now() - relativedelta(years=age) - relativedelta(days=1)
        query = "SELECT id, firstName, lastName, DATE_FORMAT(birthDay,'%m/%d/%Y'), lat, lon FROM Users WHERE  date(birthDay) < '"+date_to_mysql_string(max_date)+"' AND birthDay > '"+date_to_mysql_string(min_date)+"' ORDER BY ID LIMIT "+self.get_offset(page)+"," + str(self.page_size) + ";"
        return self.fetch_users_from_query(query)


    def get_users_search(self, filter, page):
        query = "SELECT id, firstName, lastName, DATE_FORMAT(birthDay,'%m/%d/%Y'), lat, lon FROM Users WHERE  lastName = '"+filter+"' ORDER BY ID LIMIT "+self.get_offset(page)+"," + str(self.page_size) + ";"
        return self.fetch_users_from_query(query)

    def delete_users(self):
        cursor = self.cnx.cursor(buffered=True)
        query = "DELETE FROM Users" # TODO : TRUNCATE MAY BE FASTER
        cursor.execute(query)
        self.cnx.commit()
        cursor.execute(query)
        return True

    def put_users(self, users):
        self.delete_users()
        try:
            _ = users[0]['id']
        except KeyError:
            for i in range(len(users)):
                users[i]['id'] = str(i)
        try:
            query = """INSERT INTO Users (id, firstName, lastName, birthDay, lat, lon) 
                                      VALUES (%s, %s, %s, STR_TO_DATE(%s,'%m/%d/%Y'),%s,%s) """

            cursor = self.cnx.cursor(buffered=True)
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
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, (id,))
        users = []
        for (id, firstName, lastName, birthday, lat, lon) in cursor:
            u = {"id": id,
                 "firstName": firstName,
                 "lastName": lastName,
                 "birthDay": birthday,
                 "position": {"lat": float(lat), "lon": float(lon)}}
            users.append(u)
        return users

    def post_user(self, user):
        query = """INSERT INTO Users (id, firstName, lastName, birthDay, lat, lon) 
                                              VALUES (%s, %s, %s, STR_TO_DATE(%s,'%m/%d/%Y'), %s, %s) """
        cursor = self.cnx.cursor(buffered=True)
        new_id = self.create_id()
        user_tuple = (new_id, user['firstName'], user['lastName'], user['birthDay'], user['position']['lat'], user['position']['lon'])
        cursor.execute(query, user_tuple)
        self.cnx.commit()
        if cursor.rowcount == 1:
            return new_id
        else:
            return False

    def put_user(self, user):
        try:
            cursor = self.cnx.cursor(buffered=True)
            query = """Update LUsers set id = %s, firstName = %s, lastName = %s, birthDay = %s, lat = %s, lon = %s where id = %s"""
            user_tuple = (user['id'], user['firstName'], user['lastName'], user['birthDay'], user['position']['lat'], user['position']['lon'])
            cursor.execute(query, user_tuple)
            self.cnx.commit()
            return True
        except mysql.connector.Error as error:
            print("Failed to update record to database: {}".format(error))
            return False

    def delete_user(self, id):
        query = "SELECT * FROM Users WHERE id = %s"
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, (id,))
        if cursor.rowcount == 0:
            return False
        query = "DELETE FROM Users WHERE id = %s"
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, (id,))
        self.cnx.commit()
        return True

    def create_id(self):
        query = """SELECT id FROM Users"""
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query)
        found = True
        while found:
            found = False
            new_id = str(rd.randint(0, 1000000))
            for (id) in cursor:
                if id == new_id:
                    found = True
        return new_id

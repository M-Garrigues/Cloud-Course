import mysql.connector
import os

try:
    assert os.environ['ENV'] == 'test' or os.environ['ENV'] == 'prod'
    # Config test and prod (they use similar ENV variables)
    user = os.environ['MYSQL_ADDON_USER']
    password = os.environ['MYSQL_ADDON_PASSWORD']
    host = os.environ['MYSQL_ADDON_HOST']
    database = os.environ['MYSQL_ADDON_DB']
    port = os.environ['MYSQL_ADDON_PORT']
except (KeyError, AssertionError):
    # Config dev
    user = 'uxmafubcms8efnkd'
    password = 'uKyZrSTyH2NCsjaqxq7U'
    host = 'bwku7xxv8kkyfmuzbjf9-mysql.services.clever-cloud.com'
    database = 'bwku7xxv8kkyfmuzbjf9'
    port = 3306

connexion = mysql.connector.connect(user=user,
                                    password=password,
                                    host=host,
                                    database=database,
                                    port=port)

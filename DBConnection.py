import mysql.connector

class TestDAO(object):

    def __init__(self):
        config = {
            'user': 'duntory',
            'password': '123',
            'host': '192.168.56.1',
            'database': 'duntory',
            'port': '3306'
        }
        self.conn = mysql.connector.connect(**config)
        pass

    def insertData(self, tuple):
        try :
            cursor = self.conn.cursor()

            sql = 'insert into Original_CrwalData (pid, platform, title, contents, newDT, nouns) values (%s, %s, %s, %s, %s, %s)'
            cursor.executemany(sql ,tuple)

            # for row in tuple :
            #     cursor.execute(sql,(row[0], row[1]))

        except mysql.connector.Error as err:
            print(err)
            print('롤백')

    def selectData(self, pid):
        try :
            cursor = self.conn.cursor()
            sql = 'select * from Original_CrwalData where pid = {0}'.format(pid)
            cursor.execute(sql)

            return cursor.fetchall()
        except :
            print('롤백')
            return ''

    def Commit(self):
        self.conn.commit()

    def Rollback(self):
        self.conn.rollback()
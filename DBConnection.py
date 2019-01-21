import mysql.connector

class TestDAO(object):

    def __init__(self):
        config = {
            'user': 'duntory',
            'password': 'sky950!!',
            'host': '35.231.50.242',
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

    def selectLastPid(self, site):
        try :
            cursor = self.conn.cursor()
            sql = 'select pid from Original_CrwalData where platform = \'{0}\' order by pid desc LIMIT 1'.format(site)
            cursor.execute(sql)
            return cursor.fetchall()[0][0]
        except Exception as err:
            print(err)
            return '0'

    def Commit(self):
        self.conn.commit()

    def Rollback(self):
        self.conn.rollback()
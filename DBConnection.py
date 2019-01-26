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

    # 크롤링 데이터 삽입
    def insertData(self, tuple, log):
        try :
            cursor = self.conn.cursor()

            sql = 'insert into Original_CrwalData (pid, platform, title, contents, newDT, nouns) values (%s, %s, %s, %s, %s, %s)'
            cursor.executemany(sql ,tuple)

        except mysql.connector.Error as err:
            log.error('Fail insertData - ErrorMessage : {0}'.format(err))

    # 크롤링을 위한 DB에서 마지막 pid 조회
    def selectLastPid(self, site, log):
        try :
            cursor = self.conn.cursor()
            sql = 'select pid from Original_CrwalData where platform = \'{0}\' order by pid desc LIMIT 1'.format(site)
            cursor.execute(sql)
            return cursor.fetchall()[0][0]
        except mysql.connector.Error as err:
            log.error('Fail selectLastPid - ErrorMessage : {0}'.format(err))

    def getConn(self):
        return self.conn

    def Commit(self):
        self.conn.commit()

    def Rollback(self):
        self.conn.rollback()

    def closeDB(self):
        self.conn.close()
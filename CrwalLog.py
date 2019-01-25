import logging
import time

class CrwalLog(logging.Handler) :

    def __init__(self, sql_conn, sql_cursor):
        logging.Handler.__init__(self)

        self.sql_conn = sql_conn
        self.sql_cursor = sql_cursor

    def emit(self, record):

        tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))

        sql = 'INSERT INTO CrwalLog (loggername, loglevel, loginfo, pathname, logDT)' + \
            'VALUES (%s, %s, %s, %s, %s)'

        try :
            self.sql_cursor.execute(sql, [record.name, record.levelname, record.msg, record.pathname, tm])
            self.sql_conn.commit()

        except Exception as err :
            print('디비 넣을때 에러남 ', err)
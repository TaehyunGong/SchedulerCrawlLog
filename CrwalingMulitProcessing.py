import requests
from bs4 import BeautifulSoup as bs
from multiprocessing import Process, current_process, Value, Manager
import DBConnection
import random

class CrwalingMulitProcessing(object) :

    def __init__(self):
        self.DBconn = DBConnection.TestDAO()
        pass

    def processMethod(self, low, high, list):
        for i in range(low, high) :
            self.openBrower(i,list)

    def openBrower(self, n, list):
        try :
            # url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query={0}'.format(n)
            url = 'http://df.gamechosun.co.kr/board/view.php?bid=tip&num={0}'.format(n)
            req = requests.get(url)
            html = req.text
            soup = bs(html, 'html.parser')
            title = soup.find('h1', {'id': 'bbs_title'})
            contents = soup.find('div',{'id':'NewsAdContent'})
            newDT = soup.find('span', {'class','f12'})

            if len(contents.text) > 4000 :
                contents.text = ''

            list.append([n, 'DFchosun',title.text, contents.text, newDT.text])

        except AttributeError as err :
            print(n, ' 번호는 존재 않함')

    def startMain(self):
        manager = Manager().list();

        procs = []
        # for i in range(1,500) :
        #     print(' '*50,i)
        #     self.openBrower(random.randrange(2970000,2987778),manager)

        low  = 2950000
        high = 2950010

        plus = high-low
        division = int(plus / 5)

        pageList = [low+(division*x) for x in range(5)]
        pageList.append(high)


        #프로세스 시작
        for i in range(0, 5):
            proc = Process(target=self.processMethod, args=(pageList[i], pageList[i+1] ,manager,))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        self.DBconn.insertData(manager)

        self.DBconn.Commit()

        print(pageList)
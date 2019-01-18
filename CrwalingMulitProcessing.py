import requests
from bs4 import BeautifulSoup as bs
from multiprocessing import Process, Manager
import DBConnection
from TestFile import createNouns
from datetime import datetime

class CrwalingMulitProcessing(object) :

    def __init__(self):
        self.DBconn = DBConnection.TestDAO()
        pass

    def siteLastPid(self, site):
        if site == 'DFchosun' :
            url = 'http://df.gamechosun.co.kr/board/list.php?bid=tip'
            css = '.rec_subject > a'

            req = requests.get(url)
            soup = bs(req.text, 'html.parser')

            a = soup.select(css)[0]['href']
            return a[-7:]

        elif site == 'DCinside' :
            url = 'http://gall.dcinside.com/board/lists?id=d_fighter_new1'
            css = '.gall_num'

            req = requests.get(url)
            soup = bs(req.text, 'html.parser')

            for row in soup.select(css) :
                if row.text != '공지' :
                    pid = row.text
                    break

            return pid

    def processMethod(self, low, high, list, site):
        if site == 'DFchosun' :
            for i in range(low, high) :
                self.openBrowerDFchosun(i, list)
        elif site == 'DCinside' :
            for i in range(low, high) :
                self.openBrowerDFinside(i, list)

    def openBrowerDFchosun(self, n, list):
        try :
            url = 'http://df.gamechosun.co.kr/board/view.php?bid=tip&num={0}'.format(n)
            req = requests.get(url)
            soup = bs(req.text, 'html.parser')
            title = (soup.find('h1', {'id': 'bbs_title'}).text)[4:]
            contents = soup.find('div',{'id':'NewsAdContent'}).text
            newDT = soup.find('span', {'class','f12'}).text

            if len(contents) > 4000 :
                contents = ''

            list.append([n, 'DFchosun',title, contents, newDT, ''])

        except AttributeError as err :
            # print(n, ' 번호는 존재 않함 site : DFchosun')
            pass

        except requests.ConnectionError as err :
            print('connect problem - err : ', err)
            pass

    def openBrowerDFinside(self, n, list):
        try :
            url = 'http://gall.dcinside.com/board/view/?id=d_fighter_new1&no={0}'.format(n)
            req = requests.get(url)
            soup = bs(req.text, 'html.parser')
            title = soup.find('span', {'class': 'title_subject'}).text
            contents = soup.find('div',{'class':'writing_view_box'}).text
            newDT = soup.find('span', {'class','gall_date'}).text       # 01-18 08:13:00 포맷해야함

            newDT = '-'.join([str(datetime.now().year),newDT[:5]])
            if len(contents) > 4000 :
                contents = ''

            list.append([n, 'DCinside',title, contents, newDT, ''])

        except AttributeError as err :
            # print(n, ' 번호는 존재 않함 stie : DFinside')
            pass

        except requests.ConnectionError as err :
            print('connect problem - err : ', err)
            pass

    def startMain(self):
        newNouns = createNouns()
        # newNouns.newNouns('')
        # return
        manager = Manager().list();

        platformSite = ['DFchosun','DCinside']
        # platformSite = ['DCinside']   #테스트용 던조만

        for site in platformSite :

            # low는 DB에서 가장 최근껏 에서 +1
            low = int(self.DBconn.selectLastPid(site)) + 1
            # high는 크롤링으로 해당사이트에서 가장 최신글 pid
            high = int(self.siteLastPid(site))
            print('low : ', low)
            print('high : ', high)
            plus = high-low

            #프로세스 시작 ! 다만 게시글이 최소 5개 이상이어야함
            if plus > 5 :
                division = int(plus / 5)

                pageList = [low+(division*x) for x in range(5)]
                pageList.append(high)

                procs = []
                for i in range(0, 5):
                    proc = Process(target=self.processMethod, args=(pageList[i], pageList[i+1] ,manager, site, ))
                    procs.append(proc)
                    proc.start()

                for proc in procs:
                    proc.join()
            else :
                print(site, '의 게시글이 5개 미만이므로 패스')

        #결과 계산산
        m_list = list(manager)
        for i in range(len(m_list)) :
            nouns_list = newNouns.newNouns(m_list[i][3])
            nouns_list.extend(newNouns.newNouns(m_list[i][2]))
            nouns_set = set(nouns_list) #중복값 제거
            m_list[i][5] = ' '.join(nouns_set)

        self.DBconn.insertData(m_list)
        self.DBconn.Commit()
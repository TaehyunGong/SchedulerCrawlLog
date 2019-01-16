from CrwalingMulitProcessing import CrwalingMulitProcessing
import time
import TestFile

from DBConnection import TestDAO

#2019-01-15
if __name__ == '__main__' :

    startTime = time.time()

    # CrwalingMulitProcessing().startMain()

    nobj = TestFile.createNouns()
    DBc = TestDAO()

    for n in range(2950000, 2950010) :
        str = DBc.selectData(n)

        print('A : ', str)
        str = str[0][2]
        print('C : ', str)
        print(nobj.newNouns(str))

    print('경과시간 : ', time.time() - startTime)
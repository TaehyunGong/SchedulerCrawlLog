from CrwalingMulitProcessing import CrwalingMulitProcessing
import time
import logging

#2019-01-15
if __name__ == '__main__' :

    startTime = time.time()

    CrwalingMulitProcessing().startMain()

    print('경과시간 : ', time.time() - startTime)
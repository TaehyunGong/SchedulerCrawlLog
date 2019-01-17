from CrwalingMulitProcessing import CrwalingMulitProcessing
import time
import TestFile
from TestFile import createNouns

#2019-01-15
if __name__ == '__main__' :

    startTime = time.time()
    newNouns = createNouns()

    CrwalingMulitProcessing().startMain(newNouns)

    nobj = TestFile.createNouns()

    print('경과시간 : ', time.time() - startTime)
# -*- coding: utf-8 -*-
from konlpy.tag import Okt
import konlpy

class createNouns(object) :

    def __init__(self):
        konlpy.jvm.init_jvm(jvmpath=None, max_heap_size=1024)
        self.twitter = Okt()
        pass

    def newNouns(self, doc):
        result = ''
        try :
            result = self.twitter.nouns(doc)
        except :
            result = 'false'

        return result

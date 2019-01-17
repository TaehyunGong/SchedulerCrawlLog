# -*- coding: utf-8 -*-
from konlpy.tag import Okt

class createNouns(object) :

    def __init__(self):
        self.okt = Okt()
        pass

    def newNouns(self, doc):
        try :
            result = self.okt.nouns(doc)
        except :
            result = 'false'
        finally:
            return result

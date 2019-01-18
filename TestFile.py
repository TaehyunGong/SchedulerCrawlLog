# -*- coding: utf-8 -*-
from konlpy.tag import Okt

class createNouns(object) :

    def __init__(self):
        self.kkma = Okt()
        pass

    def newNouns(self, doc):
        try :
            result = self.kkma.nouns(doc)
        except Exception as err:
            print(err)
            result = 'false'
        finally:
            return result

# -*- coding: utf-8 -*-
import collections
import konlpy
import DBConnection

db = DBConnection.TestDAO()
doc = db.selectData('2950000')[0][3]
komor = konlpy.tag.Hannanum().nouns(doc)
print(komor)

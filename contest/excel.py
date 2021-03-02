import thulac
import xlrd
import xlwt
import jieba
from xlutils.copy import copy
import numpy as np
import pandas as pd
from gensim.models.word2vec import Word2Vec

import gensim
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC


def writeExcel(row, col, str, file):
    rb = xlrd.open_workbook(file, formatting_info=True)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    ws.write(row, col, str)
    wb.save(file)


style = xlwt.easyxf('font:height 240, color-index red, bold on;align: wrap on, vert centre, horiz center')
writeExcel(1, 12, 10, 'Excel_test.xls')
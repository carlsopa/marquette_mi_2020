import tabula
import pandas as pd
import PyPDF2

pd.set_option('display.max_colwidth',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
result = []
#top=.70*72
#left = 3.05*72
#bottom = 1.71*72
# #right = 8.21*72




data = tabula.read_pdf('marquette_mi_result.pdf',guess=True,lattice=False,stream=True,pages=('3'))
for x in data:
    df = x
    df.dropna(axis='rows',how='all',inplace=True)
    df.dropna(axis='columns',how='all',inplace=True)
    df = df.reset_index(drop=True)
    print('-----------')
    print(df)
    result.append(df)
    pd.concat(result).to_csv('a.csv')
import tabula
import pandas as pd
import PyPDF2
import pdfplumber

pd.set_option('display.max_colwidth',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
result = []

#found a way to extract column headers that are vertical
# with pdfplumber.open(r'marquette_mi_result.pdf') as pdf:
#     # print(pdf.pages[2])
#     page = pdf.pages[2]
#     text = page.extract_text()
#     lines = text.split('\n')
#     for x in lines:
#         if 'Voters' in x:
#             print(x.split('  ')[6:])

# data = tabula.read_pdf('marquette_mi_result.pdf',multiple_tables=True,lattice=True,stream=True,pages=('36'))
# for x in data:
#     df = x
#     df.dropna(axis='rows',how='all',inplace=True)
#     df.dropna(axis='columns',how='all',inplace=True)
#     df = df.reset_index(drop=True)
#     # print('-----------')
#     # print(df)
#     result.append(df)
#     pd.concat(result).to_csv('a.csv')
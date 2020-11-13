import tabula
import pandas as pd
import PyPDF2
import pdfplumber



pd.set_option('display.max_colwidth',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
page = 1
result = []
continuation = False
race =''
columns = ['Precinct','Times Cast','Registered Voters','A','B','C','D','E','F','G','H','I','J','K','L','M']
def header_split(page):
    with pdfplumber.open(r'marquette_mi_result.pdf') as pdf: 
        page = pdf.pages[page]
        text = page.extract_text()
    lines = text.split('\n')
    return(lines[3])
    #future use- work to determine column headers
    # for x in lines:
    #     if 'Voters' in x:
    #         print(x.split('  ')[6:])


# with pdfplumber.open(r'marquette_mi_result.pdf') as pdf: 
#         page = pdf.pages[6]
#         text = page.extract_text()
#         # print(text[3])
# lines = text.split('\n')
# print(lines[3])
# for x in lines:
#     if 'Voters' in x:
#         print(x.split('  ')[6:])


#found a way to extract column headers that are vertical

def drop_empty(dataframe):
    dataframe.dropna(axis='rows',how='all',inplace=True)
    df.dropna(axis='columns',how='all',inplace=True)

data = tabula.read_pdf('marquette_mi_result.pdf',multiple_tables=True,lattice=True,stream=True,pages=('1-20'))
for x in data:
    # print('for')
    # continuation = False
    df = x
    # print('-----------')
    # print(df)
    df.dropna(axis='rows',how='all',inplace=True)
    df.dropna(axis='columns',how='all',inplace=True)
    df = df.reset_index(drop=True)
    if not df.empty:
        if continuation == False:
            for index, row in df.iterrows():
                if df.index.isin([index]).any() and isinstance(df.iloc[index,0],str):
                    if df.iloc[index,0] == 'County':
                        result=[]
                        continuation = True
                        race = header_split(page-1)
                        df.drop(df.index[0:index+2],inplace=True)
                        df.dropna(axis='columns',how='all',inplace=True)
                        # df.columns = columns
                        df = df.reset_index(drop=True)
                        print(df.count(axis='columns'))
                        result.append(df)
        else:
            # df.drop(df.columns[3],axis=1,inplace=True)
            # df.columns = columns
            # print(df)
            result.append(df)
            continuation = False

        page = page+1
        race.replace('  ','_')
        # print('-------------------')
        # print(race)
        save = race + '.csv'
        print(save)
        pd.concat(result).to_csv(save)

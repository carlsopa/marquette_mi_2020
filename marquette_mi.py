import tabula
import pandas as pd
import PyPDF2
import pdfplumber
import numpy as np



pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
page = 3
result = []
row_drop=[]
race=''
continuation = False

def header_split(page):
    with pdfplumber.open(r'marquette_mi_result.pdf') as pdf: 
        page = pdf.pages[page]
        text = page.extract_text()
    lines = text.split('\n')
    pdf.close()
    return(lines[3])

#12/8/2020 - attempt at spliting the races from the header
def race_split(page):
    str = ''
    with pdfplumber.open(r'marquette_mi_result.pdf') as pdf: 
        page = pdf.pages[page]
        text = page.extract_text()
    lines = text.split('\n')
    for x in lines:
        if 'Voters' in x:
            string = x
    # print(string)
    result_string = string.split('  ')[6:]
    # print(result_string)
    print(str.join(result_string).replace(' ',''))
    # result_string.replace('  ',' ')
    # print(result_string.replace(' (','('))


def duplicate_column_removal(dataframe):
    for i in dataframe.index:
                if dataframe.iloc[i,0] == dataframe.iloc[i,3]:
                    dataframe.at[i,dataframe.columns[3]] = pd.NA
    dataframe.dropna(axis='columns',how='all',inplace=True)
    return(dataframe)

def removal(dataframe):
    row_drop=[]
    dataframe = duplicate_column_removal(dataframe)
    for index, row in dataframe.iterrows():
                if pd.isna(row[0]):
                    for label, content in row.items():
                        if pd.isna(content) == False:
                            row_drop.append(index)
                            try:
                                dataframe.loc[[index+1],[label]] = content
                            except:
                                pass
    dataframe.drop(dataframe.index[row_drop],inplace=True)
    dataframe.dropna(axis='columns',how='all',inplace=True)
    dataframe.dropna(axis='rows',how='all',inplace=True)
    dataframe = dataframe.reset_index(drop=True)
    row_drop=[]
    return(dataframe)


data = tabula.read_pdf('marquette_mi_result.pdf',multiple_tables=True,lattice=True,stream=True,pages=('3-4'))
for x in data:
    df = x
    df.dropna(axis='rows',how='all',inplace=True)
    df.dropna(axis='columns',how='all',inplace=True)
    df = df.reset_index(drop=True)
    if not df.empty:
        if continuation == False:
            for index, row in df.iterrows():
                if df.index.isin([index]).any() and str(df.iloc[index,0]) == 'County':
                    result=[]
                    continuation = True
                    race = header_split(page-1) 
                    df.drop(df.index[0:index+2],inplace=True)
                    df.dropna(axis='rows',how='all',inplace=True)
                    df.dropna(axis='columns',how='all',inplace=True)
                    df = df.reset_index(drop=True)
            df = removal(df)
            for x in range(len(df.columns)):
                df.rename({df.columns[x]:x},axis=1,inplace=True)
            result.append(df)
        else:
            df.drop(df.tail(4).index,inplace=True)
            df = removal(df)
            
            for x in range(len(df.columns)):
                df.rename({df.columns[x]:x},axis=1,inplace=True)
            result.append(df)
            continuation = False
        #test stuff
        try:
            final = pd.concat(result)
            final = final.reset_index(drop=True)
        except:
            final = df
row_index = []
if pd.isna(final.iloc[0,1]):
    final = final[1:]
final = final.reset_index(drop=True)
# print(final)
for index, row in final.iterrows():
    if row[0] == 'Cumulative':
        row_index.append(index)

final.drop(row_index,inplace=True)
final = final.reset_index(drop=True)
row_index = []
if final[0].equals(final[3]):
    final.drop(final.columns[3],axis=1,inplace=True)
for index,row in final.iterrows():
    if pd.isna(row[1]):
        final.loc[index-1,0] = final.loc[index-1,0]+' '+final.loc[index,0]
        row_index.append(index)
final.drop(row_index,inplace=True)
final = final.reset_index(drop=True)

race_split(page-1)

# precinct = []
# party = []
# votes = []
# race_name = []
# for index, row in final.iterrows():
#     for x in range(1,len(row)):
#         precinct.append(row[0])
#         party.append('party')
#         votes.append(row[x])
#         race_name.append(race)
# final_result = {'precinct':precinct,'race':race,'party':party,'votes':votes}
# new = pd.DataFrame(final_result)

race.replace('  ','_')
save = race+'.csv'
final.to_csv(save)
# new.to_csv('new.csv')
page = page+1
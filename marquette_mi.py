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
    return(lines[3])
    #future use- work to determine column headers
    # for x in lines:
    #     if 'Voters' in x:
    #         print(x.split('  ')[6:])

#replacement of NaN values with corresponding data.

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
# print(final)
precinct = []
party = []
votes = []
race_name = []
for index, row in final.iterrows():
    for x in range(1,len(row)):
        precinct.append(row[0])
        party.append('party')
        votes.append(row[x])
        race_name.append(race)
final_result = {'precinct':precinct,'race':race,'party':party,'votes':votes}
new = pd.DataFrame(final_result)
# print(new)
race.replace('  ','_')
save = race+'.csv'
# final.to_csv(save)
new.to_csv('new.csv')
page = page+1
# print(final)
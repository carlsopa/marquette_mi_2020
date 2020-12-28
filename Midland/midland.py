import tabula
import pandas as pd
import numpy as np

# pd.set_option('display.max_columns',None)
# pd.set_option('display.max_rows',None)
new = True
pdf_file = 'Midland MI Results per Precinct Data report.pdf'
#unable to get the race from the first page, so we have to manually add it in
race_name = 'United States Senator'
precinct = []
candidate = []
votes = []
race = []
# skip_rows = []
start_page = 1
end_page = 2
while start_page <= end_page:
    data = tabula.read_pdf(pdf_file,multiple_tables=True,lattice=False,stream=False,pages=(start_page))
    new = False
    for x in data:
        df = x
        #since the first page has the candidates in the headers, we need to handle this page differently then the rest.  Here we need to strip out the header data to add to the candidate list
        if start_page == 1:
            df.drop(df.columns[0],axis=1,inplace=True)
            for index, row in df.iterrows():
                for i in range(len(df.columns.values)):
                    if i > 1:
                        candidate.append(df.columns.values[i])
                        votes.append(df.iloc[index,i])
                        precinct.append(df.iloc[index,0])
                        race.append(race_name)
        else:
            df.drop(df.columns[0],axis=1,inplace=True)
            print(df)
            skip_rows = []
            for index, rows in df.iterrows():
                #check to see if the first value is 'Precinct'.  If it is, then this will add the values of that row into candidatelist array.
                if rows[0] == 'Precinct':
                    skip_rows.append(index)
                    count = 1
                    candidateList = []
                    while count < len(df.columns.values):
                        candidateList.append(rows[count])
                        count = count + 1
                    #single case issue, where the names of the candidates are broken across two lines.  This combines the lines in the candidatelist array.
                    if not pd.notnull(df.iloc[index+1,0]):
                        skip_rows.append(index+1)
                        count = 0
                        while count < len(df.columns.values)-1:
                            if pd.notnull(df.iloc[index+1,count+1]):
                                candidateList[count] = candidateList[count]+' '+df.iloc[index+1,count+1]
                            count = count + 1
                if rows[0] == 'Total':
                    skip_rows.append(index+1)
                    new = True
                if index not in skip_rows:
                    for i in range(len(df.columns.values)):
                        if i >= 1:
                            votes.append(df.iloc[index,i])
                            candidate.append(candidateList[i-1])
                            precinct.append(df.iloc[index,0])
    start_page = start_page+1

final = {'precinct':precinct,'candidate':candidate,'votes':votes}
new = pd.DataFrame(final)
new.to_csv('midland.csv')
print(new)
import tabula
import pandas as pd

pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

pdf_file = 'Midland MI Results per Precinct Data report.pdf'
precinct = []
candidate = []
votes = []
start_page = 1
end_page = 1
page_range = str(start_page)+'-'+str(end_page)
while start_page <= end_page:
    data = tabula.read_pdf(pdf_file,multiple_tables=True,lattice=False,stream=False,pages=(start_page))
    for x in data:
        df = x
        if start_page == 1:
            
            df.drop(df.columns[0],axis=1,inplace=True)
            for index, row in df.iterrows():
                for i in range(len(df.columns.values)):
                        candidate.append(df.columns.values[i])
                        votes.append(df.iloc[index,i])
                        precinct.append(df.iloc[index,0])
        else:
            pass
    start_page = start_page+1

final_result = {'precinct':precinct,'candidate':candidate,'votes':votes}
new = pd.DataFrame(final_result)
print(new)
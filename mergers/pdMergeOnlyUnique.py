# pdMerge_onlyUnique.py - script which merges csv sheets in new sheet while discarding duplicate entries AND then only keep the new ones, which haven't been in the note-taking df before
# 22-11-18; 12:30
# assumptions: all files in the same current directory

import pandas as pd
from sys import argv
from datetime import date
from pathlib import Path


script, df_notes_name, df2_new_name = argv  # df_notes_name must stay unedited! This is the csv where you take notes about calls

# source (selecting columns) https://stackoverflow.com/a/22394655
df1 = pd.read_csv(f"{df_notes_name}")#, usecols=['link_link'])
df2 = pd.read_csv(f"{df2_new_name}")#, usecols=['link_link'])

df_drop = pd.concat([df1,df2]).drop_duplicates('link_link')#.reset_index(drop=True)     # source: https://stackoverflow.com/a/21317570

df_unique_new = df_drop[~df_drop['link_link'].isin(df1['link_link'])] # source: https://stackoverflow.com/a/64212853 (all df2['link_link'] which not in df1['link_link'], after dropping duplicates)

df_notes_stem = Path(df_notes_name).stem
df2_new_stem = Path(df2_new_name).stem

short_date_today = str(date.today())[2:] # create today's date with format YY-MM-DD as string
df_date_name = f"{short_date_today}_uniqueNew_{df_notes_stem}+{df2_new_stem}.csv"
df_unique_new.to_csv(
    df_date_name,
    index=False # turn to True if you want pandas index numbers in first column
    )

print(f"\nYour output file is called:", end=f"\n{df_date_name}\n")
print(f"\nFind it in the following directory:", end=f"\n{Path.cwd()}")
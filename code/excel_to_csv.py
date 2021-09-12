import pandas as pd
import os
import glob

DATAPATH = "/home/lkh256/data/breast_cancer" # Set Data Path 

df_data = pd.concat([pd.read_excel(file_nm) for file_nm in glob.glob(DATAPATH + "/MAMMO*.xlsx")], axis=0)

print(len(df_data))

df_data.to_csv(os.path.join(DATAPATH, 'dataset.tsv'), encoding='utf-8-sig', index=False, sep='\t')
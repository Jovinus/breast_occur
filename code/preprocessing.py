# %% 
import pandas as pd
from IPython.display import display
import numpy as np
import os
import glob
pd.set_option('display.max_columns', None)
# %%

DATAPATH = "/home/lkh256/data/breast_cancer" # Set Data Path 

# %%

df_var_quest = pd.read_excel("./DR.H활용변수.xlsx", header=1, sheet_name='Questionnare')

question_var = df_var_quest.query("DR_ANSWER적용 == 'Y'", engine='python')\
                           .filter(items=['Variable name ', 'Description', 'Description in Korean '])

# %%

df_var_lab = pd.read_excel("./DR.H활용변수.xlsx", header=1, sheet_name='Exam Info')

lab_var = df_var_lab.query("CODE_NM.notnull()", engine='python')\
                    .filter(['CODE', 'CODE_NM'])

# %%

df_data = pd.concat([pd.read_excel(file_nm) for file_nm in glob.glob(DATAPATH + "/MAMMO*.xlsx")], axis=0)

# df_data = pd.read_excel("./MAMMO_LAB_QUEST 2009.xlsx")
display(df_data.head())
print(len(df_data))

# %%
var_list = list(df_data.columns[:15]) + list(lab_var['CODE']) + list(question_var['Variable name '])
code_to_name_dict = dict(zip(df_var_lab['CODE'].values, df_var_lab['CODE_NM'].values))
df_data.filter(items=var_list).rename(code_to_name_dict, axis=1).drop(columns=['검사코드5', '검사명6', '검사결과내용7', '결론진단내용8', 'DATASET', '진료과코드2'])

# %%
9999, . -> 0

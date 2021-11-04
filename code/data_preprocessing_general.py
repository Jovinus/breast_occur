# %% 
import pandas as pd
from IPython.display import display
import numpy as np
import os
import glob
from tqdm import tqdm
pd.set_option('display.max_columns', None)
tqdm.pandas()
# %%
DATAPATH = "/home/lkh256/Studio/data/breast_cancer" # Set Data Path 

# %%
## Load questionnare information
df_var_quest = pd.read_excel("../variable_info/DR.H활용변수.xlsx", header=1, sheet_name='Questionnare')

question_var = df_var_quest.query("DR_ANSWER적용 == 'Y'", engine='python')\
                           .filter(items=['Variable name ', 'Description', 'Description in Korean '])

## Load variable type informations
df_var_lab = pd.read_excel("../variable_info/DR.H활용변수.xlsx", header=1, sheet_name='Exam Info')

lab_var = df_var_lab.query("CODE_NM.notnull()", engine='python')\
                    .filter(['CODE', 'CODE_NM'])

## Load breast cancer dataset
df_data = pd.read_csv(os.path.join(DATAPATH, 'dataset.tsv'), encoding='utf-8-sig', sep='\t')
df_data['처방일자3'] = pd.to_datetime(df_data['처방일자3'], utc=True)
display(df_data.head())

## Convert numeric variable to float type
var_list = list(df_data.columns[:15]) + list(lab_var['CODE']) + list(question_var['Variable name '])
code_to_name_dict = dict(zip(df_var_lab['CODE'].values, df_var_lab['CODE_NM'].values))

df_data = df_data.filter(items=var_list)\
    .rename(code_to_name_dict, axis=1)\
    .drop(columns=['검사코드5', '검사명6', '검사결과내용7', '결론진단내용8', 'DATASET', '진료과코드2'])\
    .replace({'.':np.nan, 9999:np.nan})

object_columns = list(df_data.select_dtypes('object').columns[4:])
df_data[object_columns] = df_data[object_columns].astype('float').values

## make outcome date
df_outcome = pd.read_csv(os.path.join(DATAPATH, 'outcome_20190827.csv'))
df_outcome['처방일자3'] = pd.to_datetime(df_outcome['처방일자3'], utc=True)
df_outcome = df_outcome[['환자번호1', '처방일자3', 'last_fu_date', 'cancer_date']].copy()
df_outcome = df_outcome.assign(outcome_date = np.where(df_outcome['cancer_date'].notnull(), df_outcome['cancer_date'], df_outcome['last_fu_date']),
                               outcome=np.where(df_outcome['cancer_date'].notnull(), 1, 0))
df_outcome['outcome_date'] = pd.to_datetime(df_outcome['outcome_date'], utc=True)

## Merge outcome with cancer dataset
df_data = pd.merge(df_data, df_outcome[['환자번호1', '처방일자3', 'outcome_date', 'outcome']].drop_duplicates(), 
                   how='left', left_on=['환자번호1', '처방일자3'], right_on=['환자번호1', '처방일자3'])
df_data['surv_month'] = (df_data['outcome_date'] - df_data['처방일자3']) / np.timedelta64(1, 'M')

df_data = df_data.loc[:, ~df_data.columns.duplicated()]

# %%
df_cancer_data = df_data.query("outcome_date > 처방일자3")
df_cancer_data.to_csv(os.path.join(DATAPATH, 'breast_cancer_data.csv'), 
                      index=False, 
                      encoding='utf-8-sig')
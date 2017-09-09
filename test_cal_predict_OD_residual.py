import pandas as pd
from scipy import stats as st
dis_args=-2.3
OD_args=0.8
dataframe1=pd.read_csv("D:\\OD.csv")
dataframe2=pd.read_csv('D:\\wangjy\\data\\all_ln_all2.csv')
dataframe2['pre_flux']=dataframe2["Dis"]*dis_args+dataframe2['O_N']*OD_args+dataframe2['D_N']*OD_args
print 'Ok'
p=st.pearsonr(x=dataframe2['flux'],y=dataframe2['pre_flux'])

##cal simulate pearson
dataframe1['flux']=0
for ix,row in dataframe2.iterrows():
    O=row[0]
    D=row[1]
    dataframe1.ix[(O,D),'flux']=row["flux"]
print p

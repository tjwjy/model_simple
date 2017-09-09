import numpy as np
import IO
import Cal
import pandas
def get_OD_matrix(dic,noRepeatPoint):
    for i in range(0,len(noRepeatPoint)-1):
        point1=noRepeatPoint[i]
        point2=noRepeatPoint[i+1]
        if(dic.has_key((point1.ID,point2.ID))):
            dic[(point1.ID,point2.ID )]+=1
        else:
            dic[(point1.ID,point2.ID)]=1
    return dic

read=IO.IO()
Envir,offset=read.read_Envr('D:\\temp_home.txt')
dic={}
##establish an empty dic to store the odlist---------------------
for i in range(len(Envir.PointList)):
    for g in range(len(Envir.PointList)):
        dic[(i,g)]=0

###read the file and cal the pool OD------------------------
data_mid=1
ODlist=[]
data_mid, offset = read.read_txt_step('D:\\temp_home.txt', offset)
while(data_mid):
    cal = Cal.Cal_agent(data_mid.route,Envir)
    PointList = cal.del_norepeat_PointList()
    OD_dic=get_OD_matrix(dic,PointList)
    data_mid,offset=read.read_txt_step('D:\\temp_home.txt',offset)

###change the dic to multiIndex Dataframe
index_out=[]
index_inter=[]
key= dic.keys()
value=dic.values()
for item in key:
    index_inter.append(item[1])
    index_out.append(item[0])
dataframe=pandas.DataFrame(data=value,index=[index_out,index_inter],columns=["value"])
dataframe.index.names=["O","D"]
dataframe.to_csv("D:\\OD.csv")
print dataframe
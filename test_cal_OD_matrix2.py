import numpy as np
import IO
import Cal
import pandas
def get_OD_matrix(list1,noRepeatPoint):
    for i in range(0,len(noRepeatPoint)-1):
        point1=noRepeatPoint[i]
        point2=noRepeatPoint[i+1]
        list1[point1.ID][point2.ID]+=1
    return list1

read=IO.IO()
Envir,offset=read.read_Envr('D:\\temp_home.txt')
length=len(Envir.PointList)

##establish an empty dic to store the odlist---------------------
list1=[[0]*length for i in range(length)]
###read the file and cal the pool OD------------------------
data_mid=1
ODlist=[]
data_mid, offset = read.read_txt_step('D:\\temp_home.txt', Envir,offset)
while(data_mid):
    cal = Cal.Cal_agent(data_mid.route,Envir)
    PointList = cal.del_norepeat_PointList()
    OD_dic=get_OD_matrix(list1,PointList)
    data_mid,offset=read.read_txt_step('D:\\temp_home.txt',Envir,offset)

index_out=[]
index_inter=[]
value=[]
###change the dic to multiIndex Dataframe
for i in range(length):
    for j in range(length):
        if(i!=j):
            index_out.append(i)
            index_inter.append(j)
            value.append(list1[i][j])

dataframe=pandas.DataFrame(data=value,index=[index_out,index_inter],columns=["value"])
dataframe.index.names=["O","D"]
dataframe.to_csv("D:\\OD.csv")
print dataframe
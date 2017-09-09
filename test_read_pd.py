import powerlaw
import IO
import matplotlib.pyplot as plt
import seaborn as sbn
import Cal
read=IO.IO()
Envir,offset=read.read_Envr('D:\\temp_home.txt')
data_mid=1
ODlist=[]
data_mid, offset = read.read_txt_step('D:\\temp_home.txt', offset)
while(data_mid):
    cal = Cal.Cal_agent(data_mid.route,Envir)
    PointList = cal.del_norepeat_PointList()
    OD_list = cal.cal_OD(point1=1, point2=2, PointList=PointList)
    for i,item in OD_list:
        ODlist.extend(OD_list)
    data_mid,offset=read.read_txt_step('D:\\temp_home.txt',offset)
disput=cal.cal_OD_24hours_disput(ODlist)
print disput
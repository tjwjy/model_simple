import IO
import matplotlib.pyplot as plt
import Cal
read=IO.IO()
data_mid=read.read_txt('D:\\temp_home.txt')
route=[]
for datamid in data_mid:
    route.extend(datamid.route)
cal=Cal.Cal_agent(route,data_mid[1].Envir)
PointList=cal.del_norepeat_PointList()
OD_list=cal.cal_OD(point1=1,point2=2,PointList=PointList)
time_disput=cal.cal_OD_24hours_disput(ODlist=OD_list)
figure=plt.figure(1)
x=[i for i in range(25)]
plt.plot(x,time_disput)
plt.show()
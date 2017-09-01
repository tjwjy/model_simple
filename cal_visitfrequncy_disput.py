import Environment
import powerlaw
import IO
import matplotlib.pyplot as plt
import math
import numpy as np
import Cal
read=IO.IO()
data_mid=read.read_txt('D:\\temp_home.txt')
route=[]
frequency_list=[]
for i,item in enumerate(data_mid):
    cal = Cal.Cal_agent(item.route, data_mid[1].Envir)
    PointList = cal.del_norepeat_PointList()
    frequncy=cal.get_visitfrequency_points(PointList)
    frequency_list.append(frequncy)
temp_length=[]
for item in frequency_list:
    temp_length.append(len(item))
sum=np.array(temp_length).sum()
mean1=sum/len(temp_length)
for item in frequency_list:
    if(len(item)<mean1):
        frequency_list.remove(item)
if(frequency_list):
    list=[0]*mean1
    for item in frequency_list:
        for i,item2 in enumerate(item):
            if(i<mean1):
                list[i]=list[i]+item2
    list2=[it/len(frequency_list) for it in list]
    print list2
powerlaw_format=[]
for i,item in enumerate(list2):
    for j in range(item):
        powerlaw_format.append(i+1)
fit=powerlaw.Fit(powerlaw_format,xmin=1,xmax=mean1)
fig2=fit.plot_ccdf(color='r')
fit.power_law.plot_ccdf(color="b",ax=fig2)
print fit.alpha
plt.show()


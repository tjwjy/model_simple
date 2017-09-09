import powerlaw
import IO
import matplotlib.pyplot as plt
import numpy as np
import Cal
read=IO.IO()
data_mid=read.read_txt('D:\\temp0.8\'.txt')
route=[]
rog_list=[]#store the rog
for i,item in enumerate(data_mid):
    cal = Cal.Cal_agent(item.route, data_mid[1].Envir)
    PointList = cal.del_norepeat_PointList()
    rog=cal.get_Rog(PointList)
    rog_list.append(rog)
fit=powerlaw.Fit(rog_list,xmin=1)
fig2=fit.plot_ccdf(color='r')
fit.power_law.plot_ccdf(color="b",ax=fig2)
print fit.alpha
plt.show()
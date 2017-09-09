import powerlaw
import IO
import matplotlib.pyplot as plt
import seaborn as sbn
import Cal
read=IO.IO()
data_mid=read.read_txt('D:\\temp_home.txt')
route=[]
for datamid in data_mid:
    route.extend(datamid.route)
cal=Cal.Cal_agent(route,data_mid[1].Envir)
PointList=cal.del_norepeat_PointList()
frequency=cal.get_visitfrequency_points(PointList)
x=[i for i in range(len(frequency))]
# plt.plot(x,frequency,color="r")

# powerlaw_list=cal.change_data2powerlaw_format(frequency)
# fit=powerlaw.Fit(powerlaw_list,xmin=1,xmax=9)
# fig2=fit.plot_ccdf(color='r')
# fit.power_law.plot_ccdf(color="b",ax=fig2)
# print fit.alpha
# plt.show()

step_dis=cal.get_step_dis_point(norepeat_PointList=PointList)
fit=powerlaw.Fit(step_dis,xmin=min(step_dis))
fig2=fit.plot_ccdf(color='r')
fit.power_law.plot_ccdf(color="b",ax=fig2)
print fit.alpha
plt.show()
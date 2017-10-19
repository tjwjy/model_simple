import powerlaw
import IO
import matplotlib.pyplot as plt
import Cal
read=IO.IO()
Envir,offset=read.read_Envr('D:\\temp_home.txt')
data_mid=1
ODlist=[]
data_mid, offset = read.read_txt_step('D:\\temp_home.txt',temp_envir=Envir, offset=offset)
step_dis_list=[]
while(data_mid):
    cal = Cal.Cal_agent(data_mid.route,Envir)
    PointList = cal.del_norepeat_PointList()
    step_dis = cal.get_step_dis_point(norepeat_PointList=PointList)
    step_dis_list.extend(step_dis)
fit=powerlaw.Fit(step_dis,xmin=min(step_dis))
fig2=fit.plot_ccdf(color='r')
fit.power_law.plot_ccdf(color="b",ax=fig2)
print fit.alpha
plt.show()
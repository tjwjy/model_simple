import numpy as np
import math
import Environment
class Cal_agent():
    def __init__(self,PointList,Envir):
        self.PointList=PointList
        self.Envir=Environment.Envronment([],10)
        self.Envir.copy_environment(Envir)
    #agent may stay at a position for many simulate time
    #we will del the position repeat
    #get the no repeat pointList as return
    def del_norepeat_PointList(self):
        temp_PointList=[]
        last_id=-1
        for point in self.PointList:
            if(last_id !=point.ID):
                temp_PointList.append(point)
                last_id=point.ID
        return temp_PointList

    def get_visitfrequency_points(self,norepeat_PointList):
        idlist=[]
        for point in norepeat_PointList:
            idlist.append(point.ID)
        id_array=np.array(idlist)
        id_array2=np.bincount(id_array)
        idlist2=id_array2.tolist()
        idlist3=sorted(idlist2,reverse=True)
        return idlist3

    def change_data2powerlaw_format(self,sorted_idlist):
        powerlaw_list=[]
        for i,item in enumerate(sorted_idlist):
            for j in range(int(item)):
                powerlaw_list.append(i+1)
        return powerlaw_list

    def get_step_dis_point(self,norepeat_PointList):
        disList=[]
        lastpoint=0
        for point in norepeat_PointList:
            if(lastpoint):
                tempi=min(point.ID,lastpoint.ID)
                tempj=max(point.ID,lastpoint.ID)
                dis=self.Envir.dis_dict[(tempi,tempj)]
                disList.append(dis)
            lastpoint=point
        return disList



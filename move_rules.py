#coding=gbk
from datetime import datetime
import random
import Environment
import data_mid
import powerlaw
import Point
import math
from matplotlib import pyplot as plt
class Model_base():
    def __init__(self,args_model,environment,homeposition,workposition,visited_Place=[]):
        self.Envir=Environment.Envronment([],1)
        self.args_model = args_model
        self.visited_Place = visited_Place
        self.HomePosition = homeposition
        self.WorkPosition = workposition
        self.Envir.copy_environment(environment)
        #time constrains
        self.args_t =[]
        self.t_now=-1
        self.t_end=-1
        #space constrains
        self.args_step=[]
        self.speed=-1

    def set_t_constraint(self,t_now,t_end,args_t):
        self.t_now=t_now
        self.t_end=t_end
        self.args_t=args_t
        self.set_t()

    def dis_func1(self,Point1, Point2):
        r2 = (Point1.x - Point2.x) * (Point1.x - Point2.x) + (Point1.y - Point2.y) * (Point1.y - Point2.y)
        return math.sqrt(r2)
    def set_t(self):
        if (self.args_t):
            theoretial_distribution = powerlaw.Power_Law(xmin=self.args_t[1],parameters=[self.args_t[0]])
            if(self.t_now>=0):
                tag=int((self.t_end-self.t_now)/self.args_t[1])+4
            else:
                tag=1000
            self.ts = theoretial_distribution.generate_random(tag)
    def set_space_constrain(self,speed,args_steps):
        self.speed=speed
        self.args_step=args_steps
    def get_route(self):
        mid=data_mid.data_mid(self.Envir,0)
        L_place = []
        L_tempPlace = self.visited_Place  # 访问的集合
        if (self.Envir.grid):
            for item in self.Envir.locations:
                if (item not in L_tempPlace):
                    L_place.append(item)  # 没有访问的集合
        else:
            exit()
        gama = self.args_model[1]
        r = self.args_model[0]
        # 随机选择起始点，并初始化所要用到的循环数据
        postion=random.choice(L_place)
        if(postion in L_place):
            L_place.remove(postion)
        L_tempPlace.append(postion)
        L_tempPlace.append(postion)
        temp_point = Point.Point(postion.location, postion.gridID, postion.ID, t=self.t_now, state=3,
                                 weight=postion.weight)
        temp_point.t = self.t_now
        mid.route.append(temp_point)
        self.start_position = postion
        S = self.get_count(L_tempPlace)
        index = 1
        while ((self.t_now < self.t_end) & (index < len(self.ts)-1)):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # 这时候去探索新的场所代码
                next_postion = self.get_next_position(L_place,postion)
                if (next_postion == 0):
                    continue
                postion = next_postion
                ##更新当前坐标
                L_tempPlace.append(postion)
                L_place.remove(postion)
                S = S + 1
                index = index + 1
            else:
                postion = random.choice(L_tempPlace)
                L_tempPlace.append(postion)
                index = index + 1
            temp_point=Point.Point(postion.location,postion.gridID,postion.ID,t=self.t_now,state=0,weight=postion.weight)
            temp_point.t = self.t_now
            mid.route.append(temp_point)
            self.t_now = self.t_now + self.ts[index]
        # for tempPlace in L_tempPlace:
            # self.ids.append(tempPlace.ID)

        return L_tempPlace,mid
    def get_next_position(self,L_place,postion):
        pass
    def get_count(self,temp_list):
        if(temp_list):
            return len(set(temp_list))
        else:
            return 0

class HomeOrWork_Model(Model_base):
    def get_next_position(self,L_place,postion,t):
        #choose probality is correlated to the d as
        #p = size / pow(d.beta)
        #size is the point weight
        #d equal to distance from position and next position
        beta=self.args_step[0]

        #temp value to store the probability of next point
        psum = []
        temp_sum = 0
        temp_position=[]
        max_dis=t*self.speed
        for p in L_place:
            i=min(p.ID,postion.ID)
            j=max(p.ID,postion.ID)
            if(i-j==0):
                continue
            if(self.Envir.dis_dict[(i,j)]<=max_dis):
                temp_position.append([p,self.Envir.dis_dict[(i,j)]])
            # temp_dis=self.dis_func1(p,postion)
            # if(temp_dis<max_dis):
            #     temp_position.append([p,temp_dis])
        for t_p in temp_position:
            if(t_p[1]>0):
                p=t_p[0].weight/math.pow(t_p[1],beta)
                temp_sum=temp_sum+p
                psum.append(temp_sum)
        if(psum):
            ptemp=random.uniform(0,psum[-1])
            nextstep=None
            for index,temp in enumerate(psum):
                if(ptemp<=temp):
                    nextstep=temp_position[index]
                    break
            return nextstep[0]
        else:
            return 0

    def get_route(self,temp_position):
        a=datetime.now()
        mid=data_mid.data_mid(self.Envir,0)
        L_place = []
        L_tempPlace = self.visited_Place  # 访问的集合

        if (self.Envir.grid != 0):
            aSET=set(self.Envir.PointList)
            bSET=set(self.visited_Place)
            L_place=aSET-bSET
        else:
            exit()
        gama = self.args_model[1]
        r = self.args_model[0]
        # 随机选择起始点，并初始化所要用到的循环数据
        position=temp_position
        if(position in L_place):
            L_place.remove(position)
        L_tempPlace.append(position)
        temp_point = Point.Point(position.x, position.y, gridid=position.gridID,ID=position.ID,state=3,weight=position.weight)
        temp_point.t = self.t_now
        mid.route.append(temp_point)
        S = self.get_count(L_tempPlace)
        index = 1

        while ((self.t_now < self.t_end) & (index < len(self.ts)-1 )):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # c=0
                # 这时候去探索新的场所代码
                next_postion = self.get_next_position(L_place,postion=temp_position,t=self.ts[index])
                if (next_postion == 0):
                    continue
                position = next_postion
                #更新当前坐标
                L_tempPlace.append(position)
                L_place.remove(position)
                S = S + 1
                index = index + 1
            else:
                position = random.choice(L_tempPlace)
                L_tempPlace.append(position)
                index = index + 1
            temp_point = Point.Point(position.x, position.y, gridid=position.gridID, ID=position.ID, state=3,
                                     weight=position.weight)
            temp_point.t = self.t_now
            mid.route.append(temp_point)
            self.t_now = self.t_now + self.ts[index]
        # for tempPlace in L_tempPlace:
            # self.ids.append(tempPlace.ID)
        # print (datetime.now()-a)
        # print (001)
        return L_tempPlace,mid

class Commute_Model(Model_base):
    def get_next_position(self,L_place,position1,position2,t):
        #choose probality is correlated to the d as
        #p = size / pow(d.beta)
        #size is the point weight
        #d equal to distance from position1 and next position + position2 and next position
        # 概率p=size/pow(d.beta)
        beta = self.args_step[0]

        psum = []
        temp_sum = 0
        temp_position = []
        #t is the next 2 t sum
        max_dis = t * self.speed
        # 在半径内的所有满足条件的x，y之差
        for p in L_place:
            #cal the ellipse radius and cal the min,
            i = min(p.ID, position1.ID)
            j = max(p.ID, position1.ID)
            if(i-j==0):
                continue
            dis1=self.Envir.dis_dict[(i, j)]
            i=min(p.ID, position2.ID)
            k=max(p.ID, position2.ID)
            if(i-k==0):
                continue
            dis2=self.Envir.dis_dict[(i, k)]
            temp_dis=dis1*dis1+dis2*dis2
            if ( temp_dis<= max_dis*max_dis):
                temp_position.append([p, temp_dis])
        for t_p in temp_position:
            if (t_p[1] > 0):
                p = t_p[0].weight/math.pow(t_p[1], beta)
                temp_sum = temp_sum + p
                psum.append(temp_sum)
        if (len(psum) > 0):
            ptemp = random.uniform(0, psum[len(psum) - 1])
            nextstep = None
            for index, temp in enumerate(psum):
                if (ptemp <=temp):
                    nextstep = temp_position[index]
                    break
            return nextstep[0]
        else:
            return 0
    def get_route(self,temp_position):
        a=datetime.now()
        mid=data_mid.data_mid(self.Envir,0)
        L_place = []
        L_tempPlace = self.visited_Place  # 访问的集合
        if (self.Envir.grid != 0):
            aSET = set(self.Envir.PointList)
            bSET = set(self.visited_Place)
            L_place = aSET - bSET  # 没有访问的集合
        else:
            exit()
        gama = self.args_model[1]
        r = self.args_model[0]
        # 随机选择起始点，并初始化所要用到的循环数据
        position=temp_position
        if(position in L_place):
            L_place.remove(position)
        L_tempPlace.append(position)
        temp_point = Point.Point(position.x, position.y, gridid=position.gridID,ID=position.ID,state=3,weight=position.weight)
        temp_point.t = self.t_now
        mid.route.append(temp_point)
        S = self.get_count(L_tempPlace)
        index = 1
        while ((self.t_now < self.t_end) & (index < len(self.ts)-1)):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # 这时候去探索新的场所代码
                next_postion = self.get_next_position(L_place,position1=self.HomePosition,position2=self.WorkPosition,t=self.ts[index])
                if (next_postion == 0):
                    continue
                position = next_postion
                ##更新当前坐标
                L_tempPlace.append(position)
                L_place.remove(position)
                S = S + 1
                index = index + 1
            else:
                position = random.choice(L_tempPlace)
                L_tempPlace.append(position)
                index = index + 1
            temp_point = Point.Point(position.x, position.y, gridid=position.gridID, ID=position.ID, state=2,
                                     weight=position.weight)
            temp_point.t = self.t_now
            mid.route.append(temp_point)
            self.t_now = self.t_now + self.ts[index]
        # for tempPlace in L_tempPlace:
            # self.ids.append(tempPlace.ID)
        # print (datetime.now()-a)
        return L_tempPlace,mid
class HomeOrWork_Model_repeat(Model_base):
    # in this model ,L_place (store the place has not visit) is stable
    # equal to the Environment
    # so that the people can visit the place they visit before when in explore state
    # Commute_Model del the visited place in the L_place,making people can not visit visited place when exploring
    def get_next_position(self,L_place,postion,t):
        #choose pro is correlated to the d as
        #p = size / pow(d.beta)
        #size is the point weight
        #d equal to distance
        beta=self.args_step[0]

        #temp value to store the probability of next point
        psum = []
        temp_sum = 0
        temp_position=[]
        max_dis=t*self.speed
        for p in L_place:
            i=min(p.ID,postion.ID)
            j=max(p.ID,postion.ID)
            if(i-j==0):
                continue
            if(self.Envir.dis_dict[(i,j)]<=max_dis):
                temp_position.append([p,self.Envir.dis_dict[(i,j)]])
            # temp_dis=self.dis_func1(p,postion)
            # if(temp_dis<max_dis):
            #     temp_position.append([p,temp_dis])
        for t_p in temp_position:
            if(t_p[1]>0):
                p=t_p[0].weight/math.pow(t_p[1],beta)
                temp_sum=temp_sum+p
                psum.append(temp_sum)
        if(psum):
            ptemp=random.uniform(0,psum[-1])
            nextstep=None
            for index,temp in enumerate(psum):
                if(ptemp<=temp):
                    nextstep=temp_position[index]
                    break
            return nextstep[0]
        else:
            return 0

    def get_route(self,temp_position):
        #temp_position choose the position starting states is home or work
        mid=data_mid.data_mid(self.Envir,0)
        L_place = self.Envir.PointList
        L_tempPlace = self.visited_Place  # 访问的集合

        gama = self.args_model[1]
        r = self.args_model[0]
        # 随机选择起始点，并初始化所要用到的循环数据
        position=temp_position
        L_tempPlace.append(position)
        temp_point = Point.Point(position.x, position.y, gridid=position.gridID,ID=position.ID,state=3,weight=position.weight)
        temp_point.t = self.t_now
        mid.route.append(temp_point)
        S = self.get_count(L_tempPlace)
        index = 1

        while ((self.t_now < self.t_end) & (index < len(self.ts)-1 )):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # c=0
                # 这时候去探索新的场所代码
                next_postion = self.get_next_position(L_place,postion=temp_position,t=self.ts[index])
                if (next_postion == 0):
                    continue
                position = next_postion
                #更新当前坐标
                L_tempPlace.append(position)
                S = S + 1
                index = index + 1
            else:
                position = random.choice(L_tempPlace)
                L_tempPlace.append(position)
                index = index + 1
            temp_point = Point.Point(position.x, position.y, gridid=position.gridID, ID=position.ID, state=3,
                                     weight=position.weight)
            temp_point.t = self.t_now
            mid.route.append(temp_point)
            self.t_now = self.t_now + self.ts[index]
        return L_tempPlace,mid

class Commute_Model_repeat(Model_base):
    # in this model ,L_place (store the place has not visit) is stable
    # equal to the Environment
    # so that the people can visit the place they visit before when in explore state
    # Commute_Model del the visited place in the L_place,making people can not visit visited place when exploring
    def get_next_position(self,L_place,position1,position2,t):
        # 概率p=size/pow(d.beta)
        beta = self.args_step[0]

        psum = []
        temp_sum = 0
        temp_position = []
        #t is the next 2 t sum
        max_dis = t * self.speed
        # 在半径内的所有满足条件的x，y之差
        for p in L_place:
            #cal the ellipse radius and cal the min,
            i = min(p.ID, position1.ID)
            j = max(p.ID, position1.ID)
            if(i-j==0):
                continue
            dis1=self.Envir.dis_dict[(i, j)]
            i=min(p.ID, position2.ID)
            k=max(p.ID, position2.ID)
            if(i-k==0):
                continue
            dis2=self.Envir.dis_dict[(i, k)]
            temp_dis=dis1*dis1+dis2*dis2
            if ( temp_dis<= max_dis*max_dis):
                temp_position.append([p, temp_dis])
        for t_p in temp_position:
            if (t_p[1] > 0):
                p = t_p[0].weight/math.pow(t_p[1], beta)
                temp_sum = temp_sum + p
                psum.append(temp_sum)
        if (len(psum) > 0):
            ptemp = random.uniform(0, psum[len(psum) - 1])
            nextstep = None
            for index, temp in enumerate(psum):
                if (ptemp <=temp):
                    nextstep = temp_position[index]
                    break
            return nextstep[0]
        else:
            return 0
    def get_route(self,temp_position):
        a=datetime.now()
        mid=data_mid.data_mid(self.Envir,0)
        L_place = self.Envir.PointList
        L_tempPlace = self.visited_Place  # 访问的集合

        gama = self.args_model[1]
        r = self.args_model[0]
        # 随机选择起始点，并初始化所要用到的循环数据
        position=temp_position
        L_tempPlace.append(position)
        temp_point = Point.Point(position.x, position.y, gridid=position.gridID,ID=position.ID,state=3,weight=position.weight)
        temp_point.t = self.t_now
        mid.route.append(temp_point)
        S = self.get_count(L_tempPlace)
        index = 1
        while ((self.t_now < self.t_end) & (index < len(self.ts)-1)):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # 这时候去探索新的场所代码
                next_postion = self.get_next_position(L_place,position1=self.HomePosition,position2=self.WorkPosition,t=self.ts[index])
                if (next_postion == 0):
                    continue
                position = next_postion
                ##更新当前坐标
                L_tempPlace.append(position)
                S = S + 1
                index = index + 1
            else:
                position = random.choice(L_tempPlace)
                L_tempPlace.append(position)
                index = index + 1
            temp_point = Point.Point(position.x, position.y, gridid=position.gridID, ID=position.ID, state=2,
                                     weight=position.weight)
            temp_point.t = self.t_now
            mid.route.append(temp_point)
        return L_tempPlace,mid

class HomeOrWork_Model_repeat2(HomeOrWork_Model_repeat):
    # change the distance cal method
    # choose the position people stand and the next postion as the distance cal target
    # HomeOrWork_Model_repeat choose home/work place and next positon as the cal target
    def get_route(self,temp_position):
        mid=data_mid.data_mid(self.Envir,0)
        L_place = self.Envir.PointList
        L_tempPlace = self.visited_Place  # 访问的集合

        gama = self.args_model[1]
        r = self.args_model[0]
        # 随机选择起始点，并初始化所要用到的循环数据
        position=temp_position
        L_tempPlace.append(position)
        temp_point = Point.Point(position.x, position.y, gridid=position.gridID,ID=position.ID,state=3,weight=position.weight)
        temp_point.t = self.t_now
        mid.route.append(temp_point)
        S = self.get_count(L_tempPlace)
        index = 1

        while ((self.t_now < self.t_end) & (index < len(self.ts)-1 )):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # c=0
                # 这时候去探索新的场所代码
                next_postion = self.get_next_position(L_place,postion=position,t=self.ts[index])
                if (next_postion == 0):
                    continue
                position = next_postion
                #更新当前坐标
                L_tempPlace.append(position)
                S = S + 1
                index = index + 1
            else:
                position = random.choice(L_tempPlace)
                L_tempPlace.append(position)
                index = index + 1
            temp_point = Point.Point(position.x, position.y, gridid=position.gridID, ID=position.ID, state=3,
                                     weight=position.weight)
            temp_point.t = self.t_now
            mid.route.append(temp_point)
            self.t_now = self.t_now + self.ts[index]
        # for tempPlace in L_tempPlace:
            # self.ids.append(tempPlace.ID)
        # print (datetime.now()-a)
        # print (001)
        return L_tempPlace,mid

class Commute_Model_repeat2(Commute_Model_repeat):
    # change the distance cal method
    # choose the position people stand ,home/work place
    # and the next postion as the distance cal target
    # Commute_Model_repeat choose both home and work place and next positon as the cal target
    def get_route(self,temp_position):
        a=datetime.now()
        mid=data_mid.data_mid(self.Envir,0)
        L_place = self.Envir.PointList
        L_tempPlace = self.visited_Place  # 访问的集合

        gama = self.args_model[1]
        r = self.args_model[0]
        # 随机选择起始点，并初始化所要用到的循环数据
        position=temp_position
        L_tempPlace.append(position)
        temp_point = Point.Point(position.x, position.y, gridid=position.gridID,ID=position.ID,state=3,weight=position.weight)
        temp_point.t = self.t_now
        mid.route.append(temp_point)
        S = self.get_count(L_tempPlace)
        index = 1
        while ((self.t_now < self.t_end) & (index < len(self.ts)-1)):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # 这时候去探索新的场所代码
                if(temp_position==self.HomePosition):
                    next_postion = self.get_next_position(L_place,position1=position,position2=self.WorkPosition,t=self.ts[index])
                else:
                    next_postion = self.get_next_position(L_place, position1=position, position2=self.HomePosition,
                                                          t=self.ts[index])
                if (next_postion == 0):
                    continue
                position = next_postion
                ##更新当前坐标
                L_tempPlace.append(position)
                S = S + 1
                index = index + 1
            else:
                position = random.choice(L_tempPlace)
                L_tempPlace.append(position)
                index = index + 1
            temp_point = Point.Point(position.x, position.y, gridid=position.gridID, ID=position.ID, state=2,
                                     weight=position.weight)
            temp_point.t=self.t_now
            mid.route.append(temp_point)
            self.t_now = self.t_now + self.ts[index]
        # for tempPlace in L_tempPlace:
            # self.ids.append(tempPlace.ID)
        # print (datetime.now()-a)
        return L_tempPlace,mid
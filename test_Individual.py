import Environment
import agent
import math
import Point
import IO
import time
args_model=[0.6,-0.21]
args_time=[2,1]
args_steps=[2.3]

def dis_func1(Point1,Point2):
    r2=(Point1.x-Point2.x)*(Point1.x-Point2.x)+(Point1.y-Point2.y)*(Point1.y-Point2.y)
    return math.sqrt(r2)
path="E:/data/shenzhen/shenzhen.mdb"
name="shenzhen_random_split"
field=["PN_INHABIT"]
io_dealer=IO.IO()
xy_list=io_dealer.read_shp(path=path,name=name,fied_list=field)
Point_List=[]

for i,xy in enumerate(xy_list):
    temp_Point=Point.Point(xy[1][0],xy[1][1],gridid=-1,ID=i,weight=xy[0])
    Point_List.append(temp_Point)
Envir=Environment.Envronment(Point_List=Point_List,dimension_x=10)
Envir.cal_dis_dict(dis_function=dis_func1)


simulate_time=400
temp_routeList=[]
for i in range(0,10):
#model=Model5.HomeOrWork_Model(args_model=args_model,args_t=args_time,args_steps=args_steps,environment=Envir,visited_Place=[],homeposition=random.choice(Envir.locations),workposition=random.choice(Envir.locations))
    model=agent.Nomal_Individual(args_model=args_model,args_t=args_time,args_step=args_steps,simulate_time=simulate_time,environment=Envir)
    model.simulate()
    mid=model.data_mid
    mid.person_tag = i
    write = IO.IO(mid)
    write.write_txt('D:\\' +"temp.txt", i)
    print (i)
    print time.localtime()
print (00)

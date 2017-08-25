import Environment
import Point
import IO
import math
def dis_func1(Point1,Point2):
    r2=(Point1.x-Point2.x)*(Point1.x-Point2.x)+(Point1.y-Point2.y)*(Point1.y-Point2.y)
    return math.sqrt(r2)
path="E:/data/shenzhen/shenzhen.mdb"
name="shenzhen_random_split"
field=[]
io_dealer=IO.IO()
xy_list=io_dealer.read_shp(path=path,name=name,fied_list=field)
Point_List=[]
for i,xy in enumerate(xy_list):
    temp_Point=Point.Point(xy[0][0],xy[0][1],gridid=-1,ID=i)
    Point_List.append(temp_Point)
Envir=Environment.Envronment(Point_List=Point_List,dimension_x=10)
Envir.cal_dis_dict(Envir.dis_func1)
print (0)

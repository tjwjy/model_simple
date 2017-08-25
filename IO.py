import Environment
import Point
from arcpy import env
import arcpy
import data_mid

class IO():
    def read_shp(self,path,name,fied_list=[]):
        env.workspace=path
        fiedlist=fied_list
        fiedlist.append("SHAPE@XY")
        answer_list=[]
        with arcpy.da.SearchCursor(name,fiedlist)as curse:
            for row in curse:
                temp_list=[]
                for item in row:
                    temp_list.append(item)
                answer_list.append(temp_list)
        return answer_list
    def __init__(self,mid=None):
        self.mid=mid
    def write_txt(self,path,flag):
            #write into the document the Environment first
            #when write the txt twice,begin with the route,ignore the envrionment
        if (flag == 0):
            with (open(path, 'w')) as f:
                temp_str='Environment'+'\n'
                f.write(temp_str)
                if(self.mid.Envir.grid.dimension_x*self.mid.Envir.grid.dimension_y==0):
                    temp_str=0
                else:
                    temp_str=str(self.mid.Envir.grid.dimension_x)+' '+str(self.mid.Envir.grid.dimension_y)+'\n'
                f.writelines(temp_str)
                lg = len(self.mid.Envir.PointList)
                if (lg):
                    for i, item in enumerate(self.mid.Envir.PointList):
                        temp_str = str(item.x) + " " + str(item.y) + " " + str(
                            item.ID) + " " + str(item.state) + " " + str(item.weight) + " "+str(item.gridID[0])+" "+str(item.gridID[1])+"\n"
                        f.writelines(temp_str)
                f.writelines('0\n')
        with (open(path, 'a+')) as f:
            temp_str = 'People' + '\n'
            f.write(temp_str)
            temp_str = str(self.mid.person_tag) + '\n'
            f.write(temp_str)
            if(self.mid.important_loc):
                temp_str=''
                for item in self.mid.important_loc:
                    temp_str = temp_str+str(item.ID)+' '
                temp_str=temp_str[0:len(temp_str)-1]+'\n'
                f.write(temp_str)
            else:
                temp_str='0'+'\n'
                f.writelines(temp_str)
            lg=len(self.mid.route)
            if(lg):
                for i,item in enumerate(self.mid.route):
                    temp_str = str(item.x) + " " + str(item.y) + " " + str(
                        item.ID) + " " + str(item.state) + " " + str(item.weight) + " " + str(
                        item.gridID[0]) + " " + str(item.gridID[1]) + "\n"
                    f.writelines(temp_str)
            f.writelines('0\n')

        return 0
    def read_txt(self,path):
        if self.mid:
            self.mid=None

        temp_route=[]
        dimension_x=0
        dimension_y=0
        with open(path,'r') as f:
            temp_str=f.readline()
            temp_str=temp_str.rstrip('\n')
            if(temp_str=='Environment'):
                temp_str=f.readline()
                temp_str=temp_str.rstrip('\n')
                temp_str=temp_str.split(' ')
                temp_int=[int(temp_str[0]),int(temp_str[1])]
                dimension_x,dimmension_y=temp_int[0],temp_int[1]
            tag=True
            while(tag):
                temp_str = f.readline()
                temp_str = temp_str.rstrip('\n')
                if(temp_str!=str(0)):
                    temp_str = temp_str.split(' ')
                    tempx = float(temp_str[0])
                    tempy = float(temp_str[1])
                    ID=int(temp_str[2])
                    state=int(temp_str[3])
                    weight=float(temp_str[4])
                    gridID1=int(temp_str[5])
                    gridID2=int(temp_str[6])
                    #t=float(temp_str[6])
                    point=Point.Point(tempx,tempy,ID=ID,state=state,weight=weight,gridid=(gridID1,gridID2))
                    temp_route.append(point)
                else:
                    break
            temp_envir=Environment.Envronment(temp_route,dimension_x=dimension_x,dimmension_y=dimension_y)
            temp_envir.cal_dis_dict(temp_envir.dis_func1)

            data_mid_list=[]
            temp_str = f.readline()
            while(temp_str):
                temp_route2 = []
                person_tag = 0
                temp_str = temp_str.rstrip('\n')
                if (temp_str == 'People'):
                    person_tag= int(f.readline().rstrip('\n'))
                temp_str = f.readline()
                important_loc=[]
                temp = temp_str.rstrip('\n')
                if not(temp=='0'):
                    temp = temp.split(" ")
                    for i in range(int(len(temp))):
                        index=int(temp[i])
                        point=temp_envir.PointList[index]
                        important_loc.append(point)
                while (True):
                    temp_str = f.readline()
                    temp_str = temp_str.rstrip('\n')
                    if (temp_str != str(0)):
                        temp_str = temp_str.split(' ')
                        tempx = float(temp_str[0])
                        tempy = float(temp_str[1])
                        ID = int(temp_str[2])
                        state = int(temp_str[3])
                        weight = float(temp_str[4])
                        gridID1 = int(temp_str[5])
                        gridID2=int(temp_str[6])
                       # t=float(temp_str[6])
                        point = Point.Point(tempx, tempy, gridid=(gridID1,gridID2), ID=ID, state=state, weight=weight)
                        temp_route2.append(point)
                    else:
                        break
                temp_mid=data_mid.data_mid(temp_envir,person_tag=person_tag,important_loc=important_loc)
                temp_mid.add_location(temp_route2)
                data_mid_list.append(temp_mid)
                temp_str = f.readline()
            return data_mid_list


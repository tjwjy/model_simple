import Point
import Environment
class data_mid():
    # this class is used to data IO
    def __init__(self,envrionment,person_tag=0,important_loc=[]):
        self.person_tag=person_tag
        self.Envir=envrionment
        # Environment.Envronment([],1)
        #self.Envir.copy_environment(envrionment)
        self.route=[]
        self.important_loc=important_loc

    def add_location(self, pointList):
        for item in pointList:
            self.route.append(item)
    def set_data_from_data(self, data_mid):
        self.route=data_mid.route
        self.person_tag=data_mid.person_tag
        self.environment=data_mid.environment

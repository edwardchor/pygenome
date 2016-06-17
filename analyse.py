import demjson
import operator

class Analysor:

    plate={}
    distance = []

    ERROR_RATE=''
    COVERAGE=''
    SV_MAX_LENGTH=''
    SV_MIN_LENGTH=''
    PAIR_DISTANCE=''
    STANDARD_DEVIATION=''
    READ_LENGTH=''
    NUM_OF_PAIRS=''
    LEN_OF_SEQ=''

    DEL_THRESHOLD=0
    INV_THRESHOLD=0
    DUP_THRESHOLD=0

    DUPList=[]
    INVList=[]
    DELList=[]


    def __init__(self,p,seq,plate):
        para=demjson.decode(p)

        self.seq=seq
        self.plate=plate
        self.ERROR_RATE = para['error_rate']
        self.COVERAGE = para['coverage']
        self.SV_MAX_LENGTH = para['sv_max_length']
        self.SV_MIN_LENGTH = para['sv_min_length']
        self.PAIR_DISTANCE = para['pair_distance']
        self.STANDARD_DEVIATION = para['standard_deviation']
        self.READ_LENGTH = para['read_length']
        self.NUM_OF_PAIRS=para['num_of_pairs']
        self.LEN_OF_SEQ=para['len_of_seq']



    def calcDistance(self,flag):
        for index in self.plate:
            self.distance.append((index, self.plate[index]['dis']))
        #sorted(self.plate, key=self.plate.get)
        self.distance.sort(key=lambda tuple:tuple[1])

        if flag:
            for each in self.distance:
                print(each)

    def setWatershed(self):
        self.DEL_THRESHOLD=self.SV_MIN_LENGTH+(self.SV_MAX_LENGTH-self.SV_MIN_LENGTH)/6
        self.INV_THRESHOLD=self.SV_MIN_LENGTH+(self.SV_MAX_LENGTH-self.SV_MIN_LENGTH)*3/6
        self.DUP_THRESHOLD=self.SV_MIN_LENGTH+(self.SV_MAX_LENGTH-self.SV_MIN_LENGTH)*5/6

    def analyse(self):
        self.setWatershed()

        self.findDUP()
        self.findDEL()
        # self.findINV()

        for each in self.DUPList:
            print('DUP '+str(each[0])+' '+str(each[1]))

        for each in self.DELList:
            print('DEL '+str(each[0])+' '+str(each[1]))



    def filter(self):

        return 0

    def findDUP(self):
        for each in self.distance:
            if each[1]>self.DUP_THRESHOLD:
                line=self.plate[each[0]]
                self.DUPList.append((line['1pos'],line['2pos']))
        if self.DUPList.__len__()>5:
            sorted(self.DUPList,key=lambda value:abs(value[0]-value[1]))
            self.DUPLIST=self.DUPList.__getslice__(0,4)


    def findDEL(self):
        for each in self.distance:
            if each[1]<self.DEL_THRESHOLD:
                line = self.plate[each[0]]
                self.DELList.append((line['1pos'],line['2pos']))

            if self.DELList.__len__() > 5:
                sorted(self.DUPList, key=lambda value: abs(value[0] - value[1]))
                self.DELList=self.DELList.__getslice__(self.DELList.__len__()-5,self.DELList.__len__()-1)

    def findINV(self):
        return ' '


    def dump_plate(self):
        for key, value in self.plate.iteritems():
            print(key,value)



            # if value.has_key('1pos') and value.has_key('2pos'):
            #     # print(value[1],value['1pos'],value[2],value['2pos'])
            #     res = analyse(value[1], value['1pos'], value[2], value['2pos'], seq, para)
            #

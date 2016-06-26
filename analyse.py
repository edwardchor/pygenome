import demjson
import operator

class Analysor:

    plate={}
    invplate={}
    distance = []

    ERROR_RATE=''
    COVERAGE=''
    SV_MAX_LENGTH=''
    SV_MIN_LENGTH=''
    PAIR_DISTANCE=''
    STANDARD_DEVIATION=''
    READ_LENGTH=''
    LEN_OF_SEQ=''

    DEL_THRESHOLD=0
    INV_THRESHOLD=0
    DUP_THRESHOLD=0


    DUP_TAG=0
    DEL_TAG=1
    INV_TAG=2

    DUPList=[]
    INVList=[]
    DELList=[]

    INV_FIND_BIAS_FACTOR=(float,float)
    INV_MERGE_BIAS_FACTOR=(float,float)
    DUP_FIND_BIAS_FACTOR=(float,float)
    DUP_MERGE_BIAS_FACTOR=(float,float)
    DEL_FIND_BIAS_FACTOR=(float,float)
    DEL_MERGE_BIAS_FACTOR=(float,float)

    def __init__(self,p,seq,plate,invplate):
        para=demjson.decode(p)

        self.seq=seq
        self.plate=plate
        self.invplate=invplate
        self.ERROR_RATE = para['error_rate']
        self.COVERAGE = para['coverage']
        self.SV_MAX_LENGTH = para['sv_max_length']
        self.SV_MIN_LENGTH = para['sv_min_length']
        self.PAIR_DISTANCE = para['pair_distance']
        self.STANDARD_DEVIATION = para['standard_deviation']
        self.READ_LENGTH = para['read_length']
        self.LEN_OF_SEQ=para['len_of_seq']
        self.DIR=para['dir']
        self.NAME=para['name']


    def calcDistance(self,flag):
        for index in self.plate:
            self.distance.append((index, self.plate[index]['dis']))
        #sorted(self.plate, key=self.plate.get)
        self.distance.sort(key=lambda tuple:tuple[1])

        if flag:
            for each in self.distance:
                print(each)

    def setWatershed(self):
        self.DEL_THRESHOLD=self.PAIR_DISTANCE+(self.SV_MAX_LENGTH-self.SV_MIN_LENGTH)
        self.INV_THRESHOLD=self.SV_MIN_LENGTH+(self.SV_MAX_LENGTH-self.SV_MIN_LENGTH)*3/6
        self.DUP_THRESHOLD=self.SV_MIN_LENGTH+(self.SV_MAX_LENGTH-self.SV_MIN_LENGTH)/6

    def setFactor(self):
        if self.ERROR_RATE == 0 or self.ERROR_RATE==0.0:
            self.INV_FIND_BIAS_FACTOR =(5.0/12.0,5.0/12.0)
            self.DEL_FIND_BIAS_FACTOR = (0.0,0.0)
            self.DUP_FIND_BIAS_FACTOR = (-2.9/12,0.0)

            self.INV_MERGE_BIAS_FACTOR = (0.0,0.0)
            self.DEL_MERGE_BIAS_FACTOR = (0.0,0.0)
            self.DUP_MERGE_BIAS_FACTOR = (0.0,0.0)

        elif self.ERROR_RATE == 0.001:  # bigger factor

            self.INV_FIND_BIAS_FACTOR = (5.4/12.0, 9.05/12.0)
            self.DEL_FIND_BIAS_FACTOR = (0.01/48, 1.0/12)
            self.DUP_FIND_BIAS_FACTOR = (-4.5/12.0, 0.0)

            self.INV_MERGE_BIAS_FACTOR = (0.0, 0.0)
            self.DEL_MERGE_BIAS_FACTOR = (0.0, 0.0)
            self.DUP_MERGE_BIAS_FACTOR = (0.0, 0.0)

        else:
            return ''



    def analyse(self):
        res=open(self.DIR+self.NAME+'.res','w')

        self.setWatershed()
        self.setFactor()

        self.findDUP()
        self.findDEL()
        self.findINV()

        self.DUPList = self.merge(self.DUPList,self.DUP_TAG)
        self.DELList=self.merge(self.DELList,self.DEL_TAG)
        self.INVList=self.merge(self.INVList,self.INV_TAG)

        for each in self.DUPList:
            line='DUP '+str(each[0])+' '+str(each[1])
            res.write(line+'\n')
            print(line)


        for each in self.DELList:
            line='DEL '+str(each[0])+' '+str(each[1])
            res.write(line+'\n')
            print(line)

        for each in self.INVList:
            line='INV ' + str(each[0]) + ' ' + str(each[1])
            res.write(line+'\n')
            print(line)

        res.close()



    def merge(self,list,kind):
        if list.__len__() == 0:
            return []

        list.sort(key=lambda tuple: tuple[0])
        low = 1
        high = list.__len__()
        res = []
        res.append(list[0])
        resH = 0

        if kind==self.DUP_TAG:
            while(low<high):
                if abs(list[low][0]-res[resH][0])>self.SV_MAX_LENGTH and abs(list[low][1]-res[resH][1])>self.SV_MAX_LENGTH:
                    res.append(list[low])
                    low+=1
                    resH += 1
                else:
                    res[resH]=(min(list[low][0],res[resH][0]),max(list[low][1],res[resH][1]))
                    low+=1


        elif kind==self.DEL_TAG:
            while (low < high):
                if abs(list[low][0] - res[resH][0]) > self.SV_MIN_LENGTH and abs(list[low][1] - res[resH][1]) > self.SV_MIN_LENGTH:
                    res.append(list[low])
                    low += 1
                    resH += 1
                else:
                    res[resH] = (max(list[low][0],res[resH][0]),min(list[low][1],res[resH][1]))
                    low += 1


        elif kind==self.INV_TAG:
            while (low < high):
                if abs(list[low][0] - res[resH][0]) > self.PAIR_DISTANCE and abs(list[low][1] - res[resH][1]) > self.PAIR_DISTANCE:
                    res.append(list[low])
                    low += 1
                    resH += 1
                else:
                    res[resH] = (min(list[low][0],res[resH][0]),max(list[low][1],res[resH][1]))
                    low += 1

        return res

    def findDUP(self):
        for each in self.distance:
            if each[1]>-self.READ_LENGTH*3.0/2.0:
                line=self.plate[each[0]]
                former=min(line['1pos'],line['2pos'])
                latter=max(line['1pos'],line['2pos'])
                div=latter-former
                fbias = div * self.DUP_FIND_BIAS_FACTOR[0]
                lbias = div * self.DUP_FIND_BIAS_FACTOR[1]
                self.DUPList.append((int(former + fbias), int(latter - lbias)))
        return ''


    def findDEL(self):
        for each in self.distance:
            if abs(each[1])>self.DEL_THRESHOLD:
                line = self.plate[each[0]]
                former = min(line['1pos'], line['2pos'])
                latter = max(line['1pos'], line['2pos'])
                div = latter - former
                fbias = div * self.DEL_FIND_BIAS_FACTOR[0]
                lbias = div * self.DEL_FIND_BIAS_FACTOR[1]
                self.DELList.append((int(former+fbias), int(latter-lbias)))

            # if self.DELList.__len__() > 5:
            #     sorted(self.DUPList, key=lambda value: abs(value[0] - value[1]))
            #     self.DELList=self.DELList.__getslice__(self.DELList.__len__()-5,self.DELList.__len__()-1)
        return ''


    def findINV(self):
        for each in self.invplate:
            line = self.invplate[each]
            former = min(line['1pos'], line['2pos'])
            latter = max(line['1pos'], line['2pos'])
            div = latter - former
            fbias=div*self.INV_FIND_BIAS_FACTOR[0]
            lbias=div*self.INV_FIND_BIAS_FACTOR[1]
            self.INVList.append((int(former+fbias), int(latter-lbias)))
        return ' '


    def dump_plate(self):
        for key, value in self.plate.iteritems():
            print(key,value)



            # if value.has_key('1pos') and value.has_key('2pos'):
            #     # print(value[1],value['1pos'],value[2],value['2pos'])
            #     res = analyse(value[1], value['1pos'], value[2], value['2pos'], seq, para)
            #

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

    def analyse(self):
        self.setWatershed()

        self.findDUP()
        self.findDEL()
        self.findINV()

        self.DUPList = self.merge(self.DUPList,self.DUP_TAG)
        self.DELList=self.merge(self.DELList,self.DEL_TAG)
        self.INVList=self.merge(self.INVList,self.INV_TAG)

        for each in self.DUPList:
            print('DUP '+str(each[0])+' '+str(each[1]))

        for each in self.DELList:
            print('DEL '+str(each[0])+' '+str(each[1]))

        for each in self.INVList:
            print('INV ' + str(each[0]) + ' ' + str(each[1]))



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
                    res[resH]=((list[low][0]+res[resH][0])/2,(list[low][1]+res[resH][1])/2)
                    low+=1


        elif kind==self.DEL_TAG:
            while (low < high):
                if abs(list[low][0] - res[resH][0]) > self.SV_MIN_LENGTH and abs(list[low][1] - res[resH][1]) > self.SV_MIN_LENGTH:
                    res.append(list[low])
                    low += 1
                    resH += 1
                else:
                    res[resH] = ((min(list[low][0], list[low][1]) + min(res[resH][0], res[resH][1])) / 2,
                                 (max(list[low][0], list[low][1]) + max(res[resH][0], res[resH][1])) / 2)
                    low += 1


        else:
            while (low < high):
                if abs(list[low][0] - res[resH][0]) > self.PAIR_DISTANCE and abs(list[low][1] - res[resH][1]) > self.PAIR_DISTANCE:
                    res.append(list[low])
                    low += 1
                    resH += 1
                else:
                    res[resH] = ((min(list[low][0], list[low][1]) + min(res[resH][0], res[resH][1])) / 2,
                                 (max(list[low][0], list[low][1]) + max(res[resH][0], res[resH][1])) / 2)
                    low += 1

        return res

    def findDUP(self):
        for each in self.distance:
            if each[1]>0:
                line=self.plate[each[0]]
                former=min(line['1pos'],line['2pos'])
                latter=max(line['1pos'],line['2pos'])
                div=latter-former
                self.DUPList.append((former-div/2,latter+div/2))
        return ''


    def findDEL(self):
        for each in self.distance:
            if abs(each[1])>self.DEL_THRESHOLD:
                line = self.plate[each[0]]
                self.DELList.append((min((line['1pos'],line['2pos'])),max((line['1pos'],line['2pos']))))

            if self.DELList.__len__() > 5:
                sorted(self.DUPList, key=lambda value: abs(value[0] - value[1]))
                self.DELList=self.DELList.__getslice__(self.DELList.__len__()-5,self.DELList.__len__()-1)
        return ''

    def findINV(self):
        for each in self.invplate:
            line = self.invplate[each]
            self.INVList.append((min((line['1pos'], line['2pos'])), max((line['1pos'], line['2pos']))))
        return ' '


    def dump_plate(self):
        for key, value in self.plate.iteritems():
            print(key,value)



            # if value.has_key('1pos') and value.has_key('2pos'):
            #     # print(value[1],value['1pos'],value[2],value['2pos'])
            #     res = analyse(value[1], value['1pos'], value[2], value['2pos'], seq, para)
            #
